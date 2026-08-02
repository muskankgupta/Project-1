# import re

# class ParserAgent:

#     def parse(self, question: str) -> dict:
#         question = question.lower()

#         intent = {
#             "aggregation": None,
#             "column": None,
#             "filters": {}
#         }


#         if any(word in question for word in ["total", "sum", "revenue"]):
#             intent["aggregation"] = "SUM"

#         elif any(word in question for word in ["average", "avg"]):
#             intent["aggregation"] = "AVG"

#         elif any(word in question for word in ["count", "number of", "how many"]):
#             intent["aggregation"] = "COUNT"

#         if "revenue" in question or "sales" in question:
#             intent["column"] = "amount"

#         elif "orders" in question:
#             intent["column"] = "order_id"

#         elif "units" in question or "quantity" in question:
#             intent["column"] = "quantity"

#         quarter_match = re.search(r'q([1-4])', question)
#         if quarter_match:
#             intent["filters"]["quarter"] = int(quarter_match.group(1))

#         year_match = re.search(r'(20\d{2})', question)
#         if year_match:
#             intent["filters"]["year"] = int(year_match.group(1))

#         if "state" in question:
#             # naive extraction (can improve later)
#             words = question.split()
#             if "in" in words:
#                 idx = words.index("in")
#                 if idx + 1 < len(words):
#                     intent["filters"]["state"] = words[idx + 1]

#         if "category" in question:
#             words = question.split()
#             if "in" in words:
#                 idx = words.index("in")
#                 if idx + 1 < len(words):
#                     intent["filters"]["category"] = words[idx + 1]

#         return intent
"""
parser_agent.py

Converts a natural language question into a QueryPlan.

Does NOT execute SQL.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import re
from semantics import (
    FIELDS,
    METRICS,
    STATE_NORMALIZATION,
    get_field,
    resolve_synonym,
    resolve_metric_synonym,
)


# -------------------------------------------------------
# Query Plan
# -------------------------------------------------------

@dataclass
class QueryPlan:
    metric: str | None = None
    dimensions: List[str] = field(default_factory=list)
    filters: List[Dict[str, Any]] = field(default_factory=list)
    group_by: List[str] = field(default_factory=list)
    order_by: str | None = None
    order: str = "DESC"
    limit: int | None = None


# -------------------------------------------------------
# Parser Agent
# -------------------------------------------------------

class ParserAgent:

    def __init__(self):

        # -------------------------
        # Metric dictionary
        # -------------------------

        self.metric_words = {}

        for metric in METRICS.values():

            self.metric_words[metric.name.lower()] = metric.name

            for synonym in metric.synonyms:
                self.metric_words[synonym.lower()] = metric.name

        # -------------------------
        # Dimension dictionary
        # -------------------------

        self.dimension_words = {}

        for field in FIELDS.values():

            if field.role == "measure":
                continue

            self.dimension_words[field.name.lower()] = field.name

            for synonym in field.synonyms:
                self.dimension_words[synonym.lower()] = field.name

    # --------------------------------------------------

    def parse(self, query: str) -> QueryPlan:

        q = query.lower()

        plan = QueryPlan()

        # ==================================================
        # Metric Detection
        # ==================================================

        metric_name = resolve_metric_synonym(query)

        if metric_name:
            plan.metric = metric_name

        # remove metric words before detecting dimensions

        if plan.metric:

            metric = METRICS[plan.metric]

            q = q.replace(metric.name.lower(), "")

            for s in metric.synonyms:
                q = q.replace(s.lower(), "")
        if plan.metric is None:

            if "order" in q or "orders" in q:

                plan.metric = "order_count"
        # ==================================================
        # Dimension Detection
        # ==================================================

        words = re.findall(r"[a-zA-Z_]+", q)

        for word in words:

           field = resolve_synonym(word)

           if field and field not in plan.dimensions:
              plan.dimensions.append(field)

        # ==================================================
        # GROUP BY
        # ==================================================

        if re.search(r"\b(by|per)\b", q):
            plan.group_by = plan.dimensions.copy()

        # ==================================================
        # LIMIT
        # ==================================================

        m = re.search(r"(top|bottom)\s+(\d+)", q)

        if m:
            plan.limit = int(m.group(2))

        # ==================================================
        # Sorting
        # ==================================================

        if "bottom" in q or "lowest" in q:

            plan.order = "ASC"

        else:

            plan.order = "DESC"

        # ==================================================
        # STATUS FILTER
        # ==================================================

        status_field = get_field("Status")

        if status_field and status_field.values:

            for status in status_field.values:

                if status is None:
                    continue

                s = status.lower()

                if s in q:

                    plan.filters.append({
                        "field": "Status",
                        "operator": "=",
                        "value": status
                    })

                elif "cancel" in q and "cancel" in s:

                    plan.filters.append({
                        "field": "Status",
                        "operator": "=",
                        "value": status
                    })

                elif "return" in q and "return" in s:

                    plan.filters.append({
                        "field": "Status",
                        "operator": "=",
                        "value": status
                    })

                elif "pending" in q and "pending" in s:

                    plan.filters.append({
                        "field": "Status",
                        "operator": "=",
                        "value": status
                    })

                elif "ship" in q and s.startswith("shipped"):

                    plan.filters.append({
                        "field": "Status",
                        "operator": "=",
                        "value": status
                    })
                elif "deliver" in q and "delivered" in s:

                    plan.filters.append({
                        "field": "Status",
                        "operator": "=",
                        "value": status
                    })    

        # ==================================================
        # CATEGORY FILTER
        # ==================================================

        category = get_field("Category")

        if category and category.values:

            reserved_words = {
                "top",
                "bottom",
                "highest",
                "lowest",
                "most",
                "least"
            }
            for value in category.values:
                if value.lower() in reserved_words:
                    continue
                if value.lower() in q:

                    plan.filters.append({
                        "field": "Category",
                        "operator": "=",
                        "value": value
                    })

        # ==================================================
        # STATE FILTER
        # ==================================================

        tokens = q.split()

        for token in tokens:

            state = STATE_NORMALIZATION.get(token.lower())

            if state:

                plan.filters.append({
                    "field": "ship_state",
                    "operator": "=",
                     "value": state
              })

        # ==================================================
        # Remove duplicate filters
        # ==================================================

        unique = []
        seen = set()

        for f in plan.filters:

            key = (f["field"], f["operator"], f["value"])

            if key not in seen:

                seen.add(key)

                unique.append(f)

        plan.filters = unique

        return plan

    # --------------------------------------------------

    def pretty_print(self, plan: QueryPlan):

        print("Metric      :", plan.metric)
        print("Dimensions  :", plan.dimensions)
        print("Filters     :", plan.filters)
        print("Group By    :", plan.group_by)
        print("Order       :", plan.order)
        print("Limit       :", plan.limit)


# -------------------------------------------------------
# Testing
# -------------------------------------------------------

if __name__ == "__main__":

    parser = ParserAgent()

    tests = [

        "total revenue",

        "revenue by state",

        "top 10 categories by revenue",

        "units sold by category",

        "cancelled orders",

        "revenue in Maharashtra",

        "top 5 states by units sold",

        "returned orders in Gujarat",

        "GMV by category",

        "bottom 5 states by revenue"

    ]

    for question in tests:

        print("\nQuestion:", question)

        plan = parser.parse(question)

        parser.pretty_print(plan)