"""
semantics.py
============
The semantic layer for the Amazon Sales dataset, as a structured, importable
Python module -- meant to sit alongside data.py / state.py / orchestrator.py
/ parser_agent.py / data_agent.py in the agentic-orchestrator pipeline.

Typical usage inside the pipeline:

    from semantics import SEMANTIC_LAYER, get_field, normalize_state, STATUS_GROUPS

    # in parser_agent.py: give the LLM the schema to plan against
    system_prompt = build_planning_prompt(SEMANTIC_LAYER)

    # in data_agent.py: clean/normalize before executing the plan
    df["ship-state_clean"] = df["ship-state"].map(normalize_state)

    # metric layer: resolve a named metric instead of hand-rolling formulas
    from semantics import get_metric, resolve_metric_synonym
    m = get_metric("revenue")               # -> MetricSpec
    m2 = get_metric(resolve_metric_synonym("gmv"))

    # query schema layer: validate/describe the shape of a parsed query plan
    from semantics import QUERY_SCHEMA, validate_query_plan

    # time intelligence layer: bucket dates / build period comparisons
    from semantics import bucket_date, previous_period, TIME_GRAINS

No pandas/anthropic imports here on purpose -- this module is pure metadata
+ small pure-Python helpers, so any agent can import it without pulling in
heavy or conflicting dependencies.
"""

from dataclasses import dataclass, field as dc_field
from datetime import date, timedelta
from typing import Any, Optional



# --------------------------------------------------------------------------
# Field definitions
# --------------------------------------------------------------------------



@dataclass
class FieldSpec:
    name: str                      # actual column name in the CSV
    dtype: str                     # "string" | "integer" | "float" | "categorical" | "boolean" | "date"
    role: str                      # "dimension" | "measure" | "dimension_id" | "time_dimension" | "ignore"
    description: str
    synonyms: list[str] = dc_field(default_factory=list)
    values: Optional[Any] = None   # list of allowed values, or dict of value->meaning
    notes: Optional[str] = None


FIELDS: dict[str, FieldSpec] = {
    "Order_ID": FieldSpec(
        name="Order_ID", dtype="string", role="dimension_id",
        description="Amazon order identifier. One order can span several rows (one per SKU/item).",
        synonyms=[
    "order id",
    "order number",
    "Order ID",
]
    ),
    "Date": FieldSpec(
        name="Date", dtype="date", role="time_dimension",
        description="Order date (MM-DD-YY). Dataset covers 2022-03-31 to 2022-06-29.",
        synonyms=["order date", "date", "when the order was placed"],
    ),
    "Status": FieldSpec(
        name="Status", dtype="categorical", role="dimension",
        description="Detailed order/shipment status.",
       synonyms=[
    "status",
    "order status",
    "shipment status",
    "delivery status",
],
        values=[
            "Shipped", "Shipped - Delivered to Buyer", "Cancelled",
            "Shipped - Returned to Seller", "Shipped - Picked Up", "Pending",
            "Pending - Waiting for Pick Up", "Shipped - Returning to Seller",
            "Shipped - Out for Delivery", "Shipped - Rejected by Buyer",
            "Shipping", "Shipped - Lost in Transit", "Shipped - Damaged",
        ],
        
    ),
    "Fulfilment": FieldSpec(
        name="Fulfilment", dtype="categorical", role="dimension",
        description="Who fulfilled the order.",
        synonyms=[
    "fulfillment",
    "fulfillment type",
    "fulfilled by",
    "FBA",
    "FBM",
    "FBA or merchant",
],
        values={"Amazon": "Fulfilled by Amazon (FBA)", "Merchant": "Fulfilled by seller (FBM)"},
    ),
  "Sales_Channel": FieldSpec(
    name="Sales_Channel",
    dtype="categorical",
    role="dimension",
    description="Platform the order came through.",
    synonyms=[
        "channel",
        "sales channel",
        "platform",
    ],
    values=["Amazon.in", "Non-Amazon"],
),
    "ship_service_level": FieldSpec(
        name="ship_service_level", dtype="categorical", role="dimension",
        description="Shipping speed tier.",
        synonyms=["shipping speed", "expedited or standard"],
        values=["Expedited", "Standard"],
    ),
    "Style": FieldSpec(
        name="Style", dtype="string", role="dimension_id",
        description="Style/design code, shared across sizes and color variants.",
        synonyms=["style code", "design code"],
    ),
    "SKU": FieldSpec(
        name="SKU", dtype="string", role="dimension_id",
        description="Stock keeping unit; encodes style + variant + size.",
        synonyms=["sku", "product code", "item code"],
    ),
    "Category": FieldSpec(
        name="Category", dtype="categorical", role="dimension",
        description="Product category/garment type.",
      synonyms=[
        "category",
        "categories",
        "product category",
        "product categories",
        "garment type",
        "product type",
    ],
       values=[
    "Set",
    "Kurta",
    "Western Dress",
    "Top",
    "Ethnic Dress",
    "Blouse",
    "Bottom",
    "Saree",
    "Dupatta",
],
        notes="Case-sensitive as stored ('kurta' lowercase); match case-insensitively.",
    ),
    "Size": FieldSpec(
        name="Size", dtype="categorical", role="dimension",
        description="Garment size.",
        synonyms=["size"],
        values=[
    "Xs",
    "S",
    "M",
    "L",
    "Xl",
    "Xxl",
    "3xl",
    "4xl",
    "5xl",
    "6xl",
    "Free",
],
    ),
    "ASIN": FieldSpec(
        name="ASIN", dtype="string", role="dimension_id",
        description="Amazon-wide product identifier.",
        synonyms=["asin", "amazon product id"],
    ),
    "Courier_Status": FieldSpec(
        name="Courier_Status", dtype="categorical", role="dimension",
        description="Status from the courier/logistics side (distinct from order Status).",
        synonyms=["courier status", "carrier status"],
        values=["Shipped", "Unshipped", "Cancelled", None],
    ),
    "Qty": FieldSpec(
        name="Qty", dtype="integer", role="measure",
        description="Units ordered on this line. 0 typically corresponds to Cancelled orders.",
        synonyms=[
    "qty",
    "quantity",
    "units",
    "units sold",
    "items sold",
],
    ),
    "currency": FieldSpec(
        name="currency", dtype="categorical", role="dimension",
        description="Currency of Amount. Effectively always INR when present.",
        synonyms=["currency"], values=["INR", None],
    ),
    "Amount": FieldSpec(
        name="Amount", dtype="float", role="measure",
        description="Order line value in INR. Null for many cancelled orders.",
        synonyms=[
    "amount",
    "sales",
    "revenue",
    "gmv",
    "price",
    "income",
    "sale amount",
    "order value",
],
        notes="SUM(Amount) is the default 'revenue' metric; see BUSINESS_RULES for cancelled-order handling.",
    ),
    "ship_city": FieldSpec(
        name="ship_city", dtype="string", role="dimension",
        description="Buyer's shipping city (free text, inconsistent casing).",
        synonyms=["city","cities", "shipping city", "delivery city"],
    ),
    "ship_state": FieldSpec(
        name="ship_state", dtype="string", role="dimension",
        description="Buyer's shipping state. Messy: mixed case, abbreviations, misspellings, old names.",
        synonyms=["state","states", "shipping state", "region"],
        notes="Use normalize_state() before grouping/filtering -- see STATE_NORMALIZATION below.",
    ),
    "ship_postal_code": FieldSpec(
        name="ship_postal_code", dtype="float", role="dimension",
        description="Buyer's shipping postal/PIN code.",
        synonyms=["postal code", "pincode", "zip code"],
    ),
    "ship_country": FieldSpec(
        name="ship_country", dtype="categorical", role="dimension",
        description="Almost always 'IN' (India) when present.",
        synonyms=["country"], values=["IN", None],
    ),
    "promotion_ids": FieldSpec(
        name="promotion_ids", dtype="string", role="dimension",
        description="Raw promotion/discount identifiers; null if none applied (~62% of rows have one).",
        synonyms=[
    "promotion",
    "promotion ids",
    "promotion-ids",
    "promo",
    "promo code",
    "discount",
],
        notes="Derive boolean has_promotion = promotion_ids is not null.",
    ),
    "B2B": FieldSpec(
        name="B2B", dtype="boolean", role="dimension",
        description="Whether the order was business-to-business (rare, ~0.7% of rows).",
        synonyms=["b2b", "business order", "wholesale"],
    ),
    "fulfilled_by": FieldSpec(
        name="fulfilled_by", dtype="categorical", role="dimension",
        description="Populated only for Merchant-fulfilled orders using Amazon's Easy Ship.",
        synonyms=[
    "fulfilled by",
    "fulfilled-by",
    "easy ship",
],
values=[
    "Easy Ship",
    "Unknown",
]
    ),
}


# --------------------------------------------------------------------------
# Status groupings (broad buckets a user actually asks about)
# --------------------------------------------------------------------------

STATUS_GROUPS: dict[str, list[str]] = {
    "cancelled": ["Cancelled"],
    "successfully_delivered": ["Shipped - Delivered to Buyer"],
    "in_transit_or_shipped_generic": ["Shipped", "Shipped - Picked Up", "Shipped - Out for Delivery", "Shipping"],
    "returned": ["Shipped - Returned to Seller", "Shipped - Returning to Seller"],
    "pending": ["Pending", "Pending - Waiting for Pick Up"],
    "failed_delivery": ["Shipped - Rejected by Buyer", "Shipped - Lost in Transit", "Shipped - Damaged"],
}


# --------------------------------------------------------------------------
# State-name normalization
# --------------------------------------------------------------------------

STATE_NORMALIZATION: dict[str, str] = {
    "RJ": "Rajasthan", "RAJSHTHAN": "Rajasthan", "RAJSTHAN": "Rajasthan",
    "PB": "Punjab", "NL": "Nagaland", "AR": "Arunachal Pradesh",
    "ORISSA": "Odisha", "PONDICHERRY": "Puducherry", "NEW DELHI": "Delhi",
    "mh": "Maharashtra", "MH": "Maharashtra", "TN": "Tamil Nadu",
    "maharashtra": "Maharashtra", "tamil nadu": "Tamil Nadu",
    "gj": "Gujarat", "gujarat": "Gujarat", "WB": "West Bengal", "west bengal": "West Bengal",
}


def normalize_state(raw: Optional[str]) -> Optional[str]:
    """Collapse messy ship-state variants (casing, abbreviations, old names) to one canonical name."""
    if raw is None or (isinstance(raw, float)):  # covers NaN
        return None
    v = str(raw).strip().upper()
    if v == "":
        return None
    return STATE_NORMALIZATION.get(v, v.title())


# --------------------------------------------------------------------------
# Business rules (as data, so an agent can quote/apply them, not just read them)
# --------------------------------------------------------------------------

BUSINESS_RULES: dict[str, str] = {
    "revenue_definition": (
        "Default 'revenue'/'sales' = SUM(Amount) WHERE Status != 'Cancelled'. "
        "Only sum all rows including cancelled if the user explicitly asks for gross/booked revenue."
    ),
    "unit_sales_definition": "'Units sold' = SUM(Qty); Qty is 0 for most cancelled rows already.",
    "order_count_vs_line_count": (
        "COUNT(DISTINCT 'Order ID') = number of orders. Row count = number of order lines/items. "
        "Always clarify which is meant."
    ),
    "cancellation_rate": (
        "COUNT(DISTINCT 'Order ID' WHERE Status == 'Cancelled') / COUNT(DISTINCT 'Order ID')."
    ),
    "return_rate": (
        "COUNT(DISTINCT 'Order ID' WHERE Status in returned group) / "
        "COUNT(DISTINCT 'Order ID' WHERE Status starts with 'Shipped')."
    ),
    "average_order_value": "SUM(Amount) / COUNT(DISTINCT 'Order ID'), over non-cancelled orders by default.",
    "missing_amount_currency": (
        "Amount/currency are null on ~7,795 rows, overwhelmingly cancelled orders. "
        "Treat as missing, not zero, when averaging."
    ),
    "state_field_quality": "Always normalize_state() before any state-level aggregation.",
    "date_scope": "Data only covers 2022-03-31 to 2022-06-29. Say so if asked about other periods.",
}


DERIVED_FLAGS: dict[str, str] = {
    "is_cancelled": "Status == 'Cancelled'",
    "is_delivered": "Status == 'Shipped - Delivered to Buyer'",
    "is_returned": "Status in STATUS_GROUPS['returned']",
    "has_promotion": "promotion-ids is not null",
    "is_fba": "Fulfilment == 'Amazon'",
    "is_b2b": "B2B == True",
}


RESPONSE_GUIDELINES: dict[str, str] = {
    "always_state_scope": "Mention the Mar 31-Jun 29 2022 window if the question could imply a longer period.",
    "clarify_orders_vs_lines": "Default to distinct Order ID for counts; clarify Amount/Qty are line-level sums.",
    "clarify_cancelled_handling": "Note briefly whether cancelled orders were excluded from a revenue/sales figure.",
    "no_pii_beyond_dataset": "Only ship-city/state/postal-code/country exist; no names, emails, or payment data.",
}


UNANSWERABLE_TOPICS: list[str] = [
    "Profit margin or cost data (not in dataset)",
    "Customer identity / repeat-customer analysis (no customer ID field)",
    "Any date outside 2022-03-31 to 2022-06-29",
]


# --------------------------------------------------------------------------
# Metric layer -- named, reusable business metrics
# --------------------------------------------------------------------------
# Each MetricSpec is a declarative definition of a KPI: what it's built from,
# how to compute it, and any filters baked into its default meaning. Agents
# should resolve a metric by name/synonym here rather than hand-rolling
# formulas inline, so "revenue" always means the same thing everywhere.
# ============================================================
# Metric Specification
# ============================================================

@dataclass
class MetricSpec:
    name: str
    label: str
    description: str
    formula: str
    base_fields: list[str]

    table: str
    schema: str
    catalog: str

    default_filters: Optional[list[str]] = None
    synonyms: Optional[list[str]] = None
    unit: Optional[str] = None
    related_business_rule: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        if self.default_filters is None:
            self.default_filters = []

        if self.synonyms is None:
            self.synonyms = []


# ============================================================
# Metrics
# ============================================================

METRICS: dict[str, MetricSpec] = {

    "revenue": MetricSpec(
        name="revenue",
        label="Revenue",
        description="Total sales value excluding cancelled orders.",
        formula="SUM(Amount)",
        base_fields=["Amount", "Status"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        default_filters=["Status != 'Cancelled'"],
        unit="INR",
        synonyms=["sales", "gmv", "total sales", "revenue", "net revenue","order value"],
        related_business_rule="revenue_definition",
    ),

    "gross_revenue": MetricSpec(
        name="gross_revenue",
        label="Gross Revenue",
        description="Total sales including cancelled orders.",
        formula="SUM(Amount)",
        base_fields=["Amount"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="INR",
        synonyms=["gross sales", "booked revenue", "total booked amount"],
        related_business_rule="revenue_definition",
        notes="Only use when user explicitly asks to include cancelled orders.",
    ),

    "units_sold": MetricSpec(
        name="units_sold",
        label="Units Sold",
        description="Total quantity sold.",
        formula="SUM(Qty)",
        base_fields=["Qty"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="count",
        synonyms=["units", "quantity sold", "items sold", "volume"],
        related_business_rule="unit_sales_definition",
    ),

    "order_count": MetricSpec(
        name="order_count",
        label="Order Count",
        description="Number of distinct orders.",
        formula="COUNT(DISTINCT Order_ID)",
        base_fields=["Order_ID"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="count",
        synonyms=["orders", "number of orders", "order volume"],
        related_business_rule="order_count_vs_line_count",
    ),

    "line_item_count": MetricSpec(
        name="line_item_count",
        label="Line Item Count",
        description="Number of rows in the dataset.",
        formula="COUNT(*)",
        base_fields=["Order_ID"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="count",
        synonyms=["rows", "line items", "order lines"],
        related_business_rule="order_count_vs_line_count",
    ),

    "average_order_value": MetricSpec(
        name="average_order_value",
        label="Average Order Value",
        description="Average revenue per order.",
        formula="SUM(Amount) / COUNT(DISTINCT Order_ID)",
        base_fields=["Amount", "Order_ID", "Status"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        default_filters=["Status != 'Cancelled'"],
        unit="INR",
        synonyms=["aov", "average order value", "avg order value"],
        related_business_rule="average_order_value",
    ),

    "cancellation_rate": MetricSpec(
        name="cancellation_rate",
        label="Cancellation Rate",
        description="Percentage of cancelled orders.",
        formula="""
COUNT(DISTINCT CASE
    WHEN Status='Cancelled'
    THEN Order_ID
END)
/
COUNT(DISTINCT Order_ID)
""",
        base_fields=["Order_ID", "Status"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="percent",
        synonyms=["cancel rate", "cancel percentage", "% cancelled"],
        related_business_rule="cancellation_rate",
    ),

    "return_rate": MetricSpec(
        name="return_rate",
        label="Return Rate",
        description="Percentage of returned shipped orders.",
        formula="""
COUNT(DISTINCT CASE
    WHEN Status IN (
        'Shipped - Returned to Seller',
        'Shipped - Returning to Seller'
    )
    THEN Order_ID
END)
/
COUNT(DISTINCT CASE
    WHEN Status LIKE 'Shipped%'
    THEN Order_ID
END)
""",
        base_fields=["Order_ID", "Status"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="percent",
        synonyms=["return rate", "% returned"],
        related_business_rule="return_rate",
    ),

    "promotion_penetration": MetricSpec(
        name="promotion_penetration",
        label="Promotion Penetration",
        description="Percentage of orders having promotions.",
        formula="""
COUNT(CASE
    WHEN promotion_ids IS NOT NULL
         AND promotion_ids <> 'Unknown'
    THEN 1
END)
/ COUNT(*)
""",
        base_fields=["promotion_ids"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="percent",
        synonyms=["promo rate", "promotion rate", "discount penetration"],
    ),

    "b2b_share": MetricSpec(
        name="b2b_share",
        label="B2B Share",
        description="Percentage of B2B orders.",
        formula="""
COUNT(CASE
    WHEN B2B = TRUE
    THEN 1
END)
/ COUNT(*)
""",
        base_fields=["B2B"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="percent",
        synonyms=["b2b percentage", "wholesale share"],
    ),

    "fba_share": MetricSpec(
        name="fba_share",
        label="Fulfilled by Amazon Share",
        description="Percentage of Amazon fulfilled orders.",
        formula="""
COUNT(CASE
    WHEN Fulfilment='Amazon'
    THEN 1
END)
/ COUNT(*)
""",
        base_fields=["Fulfilment"],
        table="amazon_sales_clean",
        schema="default",
        catalog="",
        unit="percent",
        synonyms=["fba percentage", "fba rate"],
    ),
}
def get_metric(name: str) -> Optional[MetricSpec]:
    """Look up a MetricSpec by its canonical key."""
    return METRICS.get(name)


def resolve_metric_synonym(text: str) -> Optional[str]:
    """
    Return the metric whose name/label/synonym appears anywhere
    in the user's question.
    """

    text = text.lower()

    for key, spec in METRICS.items():

        candidates = [
            key,
            spec.label,
            *spec.synonyms,
        ]

        for candidate in candidates:

            if candidate.lower() in text:
                return key

    return None


# --------------------------------------------------------------------------
# Query schema layer -- the structured shape a parser_agent should emit
# --------------------------------------------------------------------------
# This is a declarative contract for "what a valid query plan looks like."
# parser_agent.py should aim to produce a dict matching this shape; other
# agents (data_agent.py, orchestrator.py) can validate/consume it uniformly
# instead of each guessing at the JSON structure the LLM returns.

QUERY_SCHEMA: dict[str, Any] = {
    "description": (
        "Structured representation of a natural-language analytics question, "
        "produced by parser_agent.py and consumed by data_agent.py."
    ),
    "fields": {
        "metrics": {
            "type": "list[str]",
            "required": True,
            "description": "One or more metric keys from METRICS, e.g. ['revenue', 'order_count'].",
        },
        "dimensions": {
            "type": "list[str]",
            "required": False,
            "description": (
                "Zero or more group-by columns from FIELDS (role in "
                "{'dimension', 'dimension_id', 'time_dimension'}), e.g. ['Category', 'ship-state']."
            ),
        },
        "filters": {
            "type": "list[dict]",
            "required": False,
            "description": (
                "Each filter: {'field': <FIELDS key>, 'op': <'=' | '!=' | 'in' | 'not in' | "
                "'>' | '>=' | '<' | '<=' | 'between' | 'contains'>, 'value': <scalar | list>}."
            ),
        },
        "time_range": {
            "type": "dict | null",
            "required": False,
            "description": (
                "{'start': 'YYYY-MM-DD', 'end': 'YYYY-MM-DD'} or a TIME_GRAINS-relative shorthand "
                "like {'relative': 'last_7_days'}. Must fall within the dataset's date_range."
            ),
        },
        "granularity": {
            "type": "str | null",
            "required": False,
            "description": "One of TIME_GRAINS keys ('day','week','month') for time-bucketed results.",
        },
        "compare_to_previous_period": {
            "type": "bool",
            "required": False,
            "description": "If true, also compute the same metrics for the prior period of equal length.",
        },
        "sort": {
            "type": "dict | null",
            "required": False,
            "description": "{'by': <metric or dimension key>, 'direction': 'asc' | 'desc'}.",
        },
        "limit": {
            "type": "int | null",
            "required": False,
            "description": "Row limit for the result set (e.g. top-N queries).",
        },
    },
    "example": {
        "metrics": ["revenue", "order_count"],
        "dimensions": ["Category"],
        "filters": [{"field": "Status", "op": "!=", "value": "Cancelled"}],
        "time_range": {"start": "2022-04-01", "end": "2022-04-30"},
        "granularity": None,
        "compare_to_previous_period": True,
        "sort": {"by": "revenue", "direction": "desc"},
        "limit": 10,
    },
}


def validate_query_plan(plan: dict) -> list[str]:
    """
    Validate a parsed query plan dict against QUERY_SCHEMA + METRICS/FIELDS.
    Returns a list of human-readable error strings; empty list means valid.
    Pure structural/reference validation only -- does not touch the dataframe.
    """
    errors: list[str] = []

    metrics = plan.get("metrics")
    if not metrics:
        errors.append("plan.metrics is required and must be a non-empty list.")
    else:
        for m in metrics:
            if m not in METRICS:
                errors.append(f"Unknown metric '{m}'. Try resolve_metric_synonym() first.")

    for d in plan.get("dimensions", []) or []:
        spec = FIELDS.get(d)
        if spec is None:
            errors.append(f"Unknown dimension field '{d}'.")
        elif spec.role not in ("dimension", "dimension_id", "time_dimension"):
            errors.append(f"Field '{d}' has role '{spec.role}', not usable as a dimension.")

    for f in plan.get("filters", []) or []:
        fname = f.get("field")
        if fname not in FIELDS:
            errors.append(f"Filter references unknown field '{fname}'.")
        if f.get("op") not in {"=", "!=", "in", "not in", ">", ">=", "<", "<=", "between", "contains"}:
            errors.append(f"Filter on '{fname}' has unsupported op '{f.get('op')}'.")

    tr = plan.get("time_range")
    if tr and "start" in tr and "end" in tr:
        try:
            start = date.fromisoformat(tr["start"])
            end = date.fromisoformat(tr["end"])
            if start > end:
                errors.append("time_range.start is after time_range.end.")
            if start < DATASET_DATE_RANGE[0] or end > DATASET_DATE_RANGE[1]:
                errors.append(
                    f"time_range must fall within dataset scope "
                    f"{DATASET_DATE_RANGE[0].isoformat()}..{DATASET_DATE_RANGE[1].isoformat()}."
                )
        except ValueError:
            errors.append("time_range.start/end must be ISO date strings 'YYYY-MM-DD'.")

    gran = plan.get("granularity")
    if gran is not None and gran not in TIME_GRAINS:
        errors.append(f"Unknown granularity '{gran}'. Valid options: {list(TIME_GRAINS)}.")

    sort = plan.get("sort")
    if sort:
        by = sort.get("by")
        if by not in METRICS and by not in FIELDS:
            errors.append(f"sort.by '{by}' is not a known metric or field.")
        if sort.get("direction") not in ("asc", "desc"):
            errors.append("sort.direction must be 'asc' or 'desc'.")

    return errors


# --------------------------------------------------------------------------
# Time intelligence layer -- date bucketing + period comparisons
# --------------------------------------------------------------------------
# The dataset covers a fixed, short window (2022-03-31 .. 2022-06-29), so
# these helpers are deliberately simple: bucket a date into day/week/month,
# and compute the "previous period" of equal length for period-over-period
# comparisons, clamped to what actually exists in the data.

DATASET_DATE_RANGE: tuple[date, date] = (date(2022, 3, 31), date(2022, 6, 29))

TIME_GRAINS: dict[str, str] = {
    "day": "Bucket by calendar date (YYYY-MM-DD).",
    "week": "Bucket by ISO week, labeled by the Monday of that week (YYYY-MM-DD).",
    "month": "Bucket by calendar month (YYYY-MM).",
}

RELATIVE_TIME_SHORTHANDS: dict[str, str] = {
    "last_7_days": "The 7 days ending at the dataset's max date (2022-06-29).",
    "last_30_days": "The 30 days ending at the dataset's max date (2022-06-29).",
    "first_week": "2022-03-31 through 2022-04-06.",
    "last_week": "The 7 days ending at the dataset's max date (2022-06-29).",
    "full_range": "The entire dataset date range.",
}


def bucket_date(d: date, grain: str) -> str:
    """
    Bucket a date into a label string at the given granularity.
    grain: one of TIME_GRAINS ('day' | 'week' | 'month').
    """
    if grain not in TIME_GRAINS:
        raise ValueError(f"Unknown time grain '{grain}'. Valid options: {list(TIME_GRAINS)}.")
    if grain == "day":
        return d.isoformat()
    if grain == "week":
        monday = d - timedelta(days=d.weekday())
        return monday.isoformat()
    if grain == "month":
        return f"{d.year:04d}-{d.month:02d}"
    raise AssertionError("unreachable")  # pragma: no cover


def resolve_relative_range(shorthand: str) -> tuple[date, date]:
    """Resolve a RELATIVE_TIME_SHORTHANDS key into a concrete (start, end) date tuple."""
    _, max_d = DATASET_DATE_RANGE
    min_d, _ = DATASET_DATE_RANGE
    if shorthand in ("last_7_days", "last_week"):
        return (max_d - timedelta(days=6), max_d)
    if shorthand == "last_30_days":
        start = max_d - timedelta(days=29)
        return (max(start, min_d), max_d)
    if shorthand == "first_week":
        return (min_d, min_d + timedelta(days=6))
    if shorthand == "full_range":
        return DATASET_DATE_RANGE
    raise ValueError(f"Unknown relative shorthand '{shorthand}'. Valid options: {list(RELATIVE_TIME_SHORTHANDS)}.")


def previous_period(start: date, end: date, clamp_to_dataset: bool = True) -> tuple[date, date]:
    """
    Given a (start, end) window, return the immediately preceding window of
    equal length (in days), for period-over-period comparisons.
    If clamp_to_dataset is True, the result is clamped to DATASET_DATE_RANGE
    and may be shorter than the original window (or invalid, i.e. prev_end <
    prev_start, if the requested window starts at/before the dataset's min date).
    """
    length = (end - start).days
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=length)
    if clamp_to_dataset:
        min_d, _max_d = DATASET_DATE_RANGE
        prev_start = max(prev_start, min_d)
    return (prev_start, prev_end)


def is_in_dataset_range(d: date) -> bool:
    """Whether a date falls within the dataset's known coverage window."""
    return DATASET_DATE_RANGE[0] <= d <= DATASET_DATE_RANGE[1]


TIME_INTELLIGENCE: dict[str, Any] = {
    "dataset_date_range": {"min": DATASET_DATE_RANGE[0].isoformat(), "max": DATASET_DATE_RANGE[1].isoformat()},
    "grains": TIME_GRAINS,
    "relative_shorthands": RELATIVE_TIME_SHORTHANDS,
    "notes": (
        "All comparisons should be clamped to the dataset's date range. "
        "'previous_period' comparisons near the start of the range may be shorter "
        "than the reference period or unavailable -- flag this to the user rather "
        "than silently truncating."
    ),
}


# --------------------------------------------------------------------------
# Top-level bundle -- pass this whole thing to an LLM planning prompt
# --------------------------------------------------------------------------

SEMANTIC_LAYER: dict[str, Any] = {
    "dataset": {
        "name": "amazon_sale_report",
        "description": (
            "Line-item level Amazon.in order records for a clothing/apparel seller. "
            "Each row is one SKU line within one order."
        ),
        "grain": "One row = one order line (one SKU within one Order ID).",
        "date_range": {"min": "2022-03-31", "max": "2022-06-29"},
    },
    "fields": {name: vars(spec) for name, spec in FIELDS.items()},
    "status_groups": STATUS_GROUPS,
    "business_rules": BUSINESS_RULES,
    "derived_flags": DERIVED_FLAGS,
    "response_guidelines": RESPONSE_GUIDELINES,
    "unanswerable_topics": UNANSWERABLE_TOPICS,
    "metrics": {name: vars(spec) for name, spec in METRICS.items()},
    "query_schema": QUERY_SCHEMA,
    "time_intelligence": TIME_INTELLIGENCE,
}


# --------------------------------------------------------------------------
# Small helpers other agents can call directly instead of re-parsing the dict
# --------------------------------------------------------------------------

def get_field(name: str) -> Optional[FieldSpec]:
    """Look up a FieldSpec by raw column name."""
    return FIELDS.get(name)


def resolve_synonym(term: str) -> Optional[str]:
    """Given a natural-language term (e.g. 'revenue'), return the matching column name, if any."""
    term_l = term.strip().lower()
    for col_name, spec in FIELDS.items():
        if term_l == col_name.strip().lower() or term_l in [s.lower() for s in spec.synonyms]:
            return col_name
    return None


def status_bucket(status: str) -> Optional[str]:
    """Given a raw Status value, return which STATUS_GROUPS bucket it falls in."""
    for bucket, members in STATUS_GROUPS.items():
        if status in members:
            return bucket
    return None


if __name__ == "__main__":
    # quick self-check when run directly: python3 semantics.py
    import json
    print(json.dumps(SEMANTIC_LAYER, indent=2, default=str)[:1500])
    print("...")
    print("resolve_synonym('revenue') ->", resolve_synonym("revenue"))
    print("resolve_synonym('shipping speed') ->", resolve_synonym("shipping speed"))
    print("normalize_state('RAJSHTHAN') ->", normalize_state("RAJSHTHAN"))
    print("normalize_state('  bihar ') ->", normalize_state("  bihar "))
    print("status_bucket('Shipped - Returned to Seller') ->", status_bucket("Shipped - Returned to Seller"))

    # metric layer
    print("get_metric('revenue') ->", get_metric("revenue"))
    print("resolve_metric_synonym('gmv') ->", resolve_metric_synonym("gmv"))

    # query schema layer
    sample_plan = dict(QUERY_SCHEMA["example"])
    print("validate_query_plan(example) ->", validate_query_plan(sample_plan))
    bad_plan = {"metrics": ["not_a_metric"], "dimensions": ["not_a_field"]}
    print("validate_query_plan(bad) ->", validate_query_plan(bad_plan))

    # time intelligence layer
    print("bucket_date(2022-04-15, 'week') ->", bucket_date(date(2022, 4, 15), "week"))
    print("bucket_date(2022-04-15, 'month') ->", bucket_date(date(2022, 4, 15), "month"))
    print("resolve_relative_range('last_7_days') ->", resolve_relative_range("last_7_days"))
    print("previous_period(2022-06-01, 2022-06-07) ->", previous_period(date(2022, 6, 1), date(2022, 6, 7)))
