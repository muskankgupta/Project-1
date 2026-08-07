# """
# semantics
# =========
# The semantic layer package for the Amazon Sales chatbot.

# Public API (import directly from the package):

#     from semantics import (
#         SEMANTIC_LAYER,      # full schema as a dict, for dumping into an LLM prompt
#         FIELDS,               # dict[str, FieldSpec] -- one entry per raw CSV column
#         STATUS_GROUPS,        # broad status buckets (cancelled/delivered/returned/...)
#         BUSINESS_RULES,       # named business logic definitions (revenue, AOV, etc.)
#         DERIVED_FLAGS,        # boolean flags derivable from raw columns
#         RESPONSE_GUIDELINES,  # how the chatbot should phrase answers
#         UNANSWERABLE_TOPICS,  # things this dataset cannot answer
#         get_field,            # get_field("Amount") -> FieldSpec
#         resolve_synonym,      # resolve_synonym("revenue") -> "Amount"
#         status_bucket,        # status_bucket("Cancelled") -> "cancelled"
#         normalize_state,      # normalize_state("RAJSHTHAN") -> "Rajasthan"

#         # metric layer
#         METRICS,               # dict[str, MetricSpec] -- named KPIs (revenue, AOV, etc.)
#         MetricSpec,
#         get_metric,             # get_metric("revenue") -> MetricSpec
#         resolve_metric_synonym, # resolve_metric_synonym("gmv") -> "revenue"

#         # query schema layer
#         QUERY_SCHEMA,          # declarative shape of a parsed query plan
#         validate_query_plan,   # validate_query_plan(plan) -> list[str] of errors

#         # time intelligence layer
#         DATASET_DATE_RANGE,       # (date(2022,3,31), date(2022,6,29))
#         TIME_GRAINS,               # {"day": ..., "week": ..., "month": ...}
#         RELATIVE_TIME_SHORTHANDS,  # {"last_7_days": ..., "full_range": ...}
#         TIME_INTELLIGENCE,         # bundled dict version, for prompts
#         bucket_date,               # bucket_date(d, "week") -> "2022-04-11"
#         resolve_relative_range,    # resolve_relative_range("last_7_days") -> (start, end)
#         previous_period,           # previous_period(start, end) -> (prev_start, prev_end)
#         is_in_dataset_range,       # is_in_dataset_range(d) -> bool
#     )

# This keeps other agents (parser_agent.py, data_agent.py, orchestrator.py, etc.)
# from having to know the internal module layout -- they just do
# `import semantics` or `from semantics import X`.
# """

# from .schema import (
#     FieldSpec,
#     FIELDS,
#     STATUS_GROUPS,
#     STATE_NORMALIZATION,
#     BUSINESS_RULES,
#     DERIVED_FLAGS,
#     RESPONSE_GUIDELINES,
#     UNANSWERABLE_TOPICS,
#     SEMANTIC_LAYER,
#     get_field,
#     resolve_synonym,
#     status_bucket,
#     normalize_state,

#     # metric layer
#     METRICS,
#     MetricSpec,
#     get_metric,
#     resolve_metric_synonym,

#     # query schema layer
#     QUERY_SCHEMA,
#     validate_query_plan,

#     # time intelligence layer
#     DATASET_DATE_RANGE,
#     TIME_GRAINS,
#     RELATIVE_TIME_SHORTHANDS,
#     TIME_INTELLIGENCE,
#     bucket_date,
#     resolve_relative_range,
#     previous_period,
#     is_in_dataset_range,
# )

# # load_dataset needs pandas; import lazily so `import semantics` never
# # requires pandas just to read the schema.
# def load_dataset(csv_path: str):
#     from .loader import load_dataset as _load_dataset
#     return _load_dataset(csv_path)


# __all__ = [
#     "FieldSpec",
#     "FIELDS",
#     "STATUS_GROUPS",
#     "STATE_NORMALIZATION",
#     "BUSINESS_RULES",
#     "DERIVED_FLAGS",
#     "RESPONSE_GUIDELINES",
#     "UNANSWERABLE_TOPICS",
#     "SEMANTIC_LAYER",
#     "get_field",
#     "resolve_synonym",
#     "status_bucket",
#     "normalize_state",
#     "load_dataset",

#     # metric layer
#     "METRICS",
#     "MetricSpec",
#     "get_metric",
#     "resolve_metric_synonym",

#     # query schema layer
#     "QUERY_SCHEMA",
#     "validate_query_plan",

#     # time intelligence layer
#     "DATASET_DATE_RANGE",
#     "TIME_GRAINS",
#     "RELATIVE_TIME_SHORTHANDS",
#     "TIME_INTELLIGENCE",
#     "bucket_date",
#     "resolve_relative_range",
#     "previous_period",
#     "is_in_dataset_range",
# ]

# __version__ = "1.1.0"
"""
semantics
=========
The semantic layer package for the Amazon Sales chatbot.

Public API:

    from semantics import (
        SEMANTIC_LAYER,
        FIELDS,
        STATUS_GROUPS,
        BUSINESS_RULES,
        DERIVED_FLAGS,
        RESPONSE_GUIDELINES,
        UNANSWERABLE_TOPICS,
        get_field,
        resolve_synonym,
        status_bucket,
        normalize_state,

        # metric layer
        METRICS,
        MetricSpec,
        get_metric,
        resolve_metric_synonym,

        # query schema layer
        QUERY_SCHEMA,
        validate_query_plan,

        # time intelligence layer
        DATASET_DATE_RANGE,
        TIME_GRAINS,
        RELATIVE_TIME_SHORTHANDS,
        TIME_INTELLIGENCE,
        bucket_date,
        resolve_relative_range,
        previous_period,
        is_in_dataset_range,
    )
"""

from .schema import (
    FieldSpec,
    FIELDS,
    STATUS_GROUPS,
    STATE_NORMALIZATION,
    BUSINESS_RULES,
    DERIVED_FLAGS,
    RESPONSE_GUIDELINES,
    UNANSWERABLE_TOPICS,
    SEMANTIC_LAYER,
    get_field,
    resolve_synonym,
    status_bucket,
    normalize_state,

    # Metric layer
    METRICS,
    MetricSpec,
    get_metric,
    resolve_metric_synonym,

    # Query schema layer
    QUERY_SCHEMA,
    validate_query_plan,

    # Time intelligence layer
    DATASET_DATE_RANGE,
    TIME_GRAINS,
    RELATIVE_TIME_SHORTHANDS,
    TIME_INTELLIGENCE,
    bucket_date,
    resolve_relative_range,
    previous_period,
    is_in_dataset_range,
)

__all__ = [
    "FieldSpec",
    "FIELDS",
    "STATUS_GROUPS",
    "STATE_NORMALIZATION",
    "BUSINESS_RULES",
    "DERIVED_FLAGS",
    "RESPONSE_GUIDELINES",
    "UNANSWERABLE_TOPICS",
    "SEMANTIC_LAYER",

    "get_field",
    "resolve_synonym",
    "status_bucket",
    "normalize_state",

    # Metric layer
    "METRICS",
    "MetricSpec",
    "get_metric",
    "resolve_metric_synonym",

    # Query schema layer
    "QUERY_SCHEMA",
    "validate_query_plan",

    # Time intelligence layer
    "DATASET_DATE_RANGE",
    "TIME_GRAINS",
    "RELATIVE_TIME_SHORTHANDS",
    "TIME_INTELLIGENCE",
    "bucket_date",
    "resolve_relative_range",
    "previous_period",
    "is_in_dataset_range",
]

__version__ = "2.0.0"