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

Converts a natural-language question into a semantic QueryPlan.

The parser resolves metrics, dimensions, status values, categorical values,
and state names through the shared SemanticLoader instead of maintaining local
keyword tables.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

from loader import SemanticLoader, get_semantic_loader


logger = logging.getLogger(__name__)


def _canonicalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.casefold())).strip()


@dataclass
class QueryPlan:
    metrics: list[str] = field(default_factory=list)
    metric: str | None = None
    dimensions: list[str] = field(default_factory=list)
    filters: list[dict[str, Any]] = field(default_factory=list)
    group_by: list[str] = field(default_factory=list)
    order_by: str | None = None
    order: str = "DESC"
    limit: int | None = None
    raw_query: str = ""
    rewritten_query: str = ""
    notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.metric and self.metric not in self.metrics:
            self.metrics.insert(0, self.metric)

        if self.metrics and self.metric is None:
            self.metric = self.metrics[0]

    @property
    def primary_metric(self) -> str | None:
        return self.metric or (self.metrics[0] if self.metrics else None)


class ParserAgent:
    """Resolve a question into a semantic query plan."""

    def __init__(self, semantic_loader: SemanticLoader | None = None) -> None:
        self.semantic = semantic_loader or get_semantic_loader()

    def parse(self, query: str) -> QueryPlan:
        raw_query = query.strip()
        normalized_query = _canonicalize(raw_query)
        plan = QueryPlan(raw_query=raw_query, rewritten_query=raw_query)

        metric_matches = self.semantic.find_metric_matches(raw_query)
        inferred_metric = self.semantic.infer_metric_from_question(raw_query)

        if metric_matches:
            plan.metrics = metric_matches
        elif inferred_metric:
            plan.metrics = [inferred_metric]

        if plan.metrics:
            plan.metric = plan.metrics[0]

        for field_name in self.semantic.find_field_matches(raw_query):
            field_spec = self.semantic.get_field(field_name)
            if field_spec is None or field_spec.role == "measure":
                continue

            if field_name not in plan.dimensions:
                plan.dimensions.append(field_name)

        self._apply_value_filters(raw_query, plan)
        self._apply_status_filters(normalized_query, plan)
        self._apply_state_filters(normalized_query, plan)
        self._apply_default_grouping(normalized_query, plan)
        self._apply_sorting_and_limit(normalized_query, plan)
        self._deduplicate_plan(plan)

        if plan.metrics and not plan.metric:
            plan.metric = plan.metrics[0]

        return plan

    def _apply_value_filters(self, query: str, plan: QueryPlan) -> None:
        for match in self.semantic.find_value_matches(query):
            value = match.value
            if value is None:
                continue

            filter_spec = {
                "field": match.canonical_name,
                "operator": "=",
                "value": value,
            }

            if filter_spec not in plan.filters:
                plan.filters.append(filter_spec)

    def _apply_status_filters(self, normalized_query: str, plan: QueryPlan) -> None:
        status_values: set[str] = set()

        for alias, values in self.semantic.status_aliases.items():
            if re.search(rf"(?<!\\w){re.escape(alias)}(?!\\w)", normalized_query):
                status_values.update(values)

        for status in status_values:
            filter_spec = {
                "field": "Status",
                "operator": "=",
                "value": status,
            }

            if filter_spec not in plan.filters:
                plan.filters.append(filter_spec)

    def _apply_state_filters(self, normalized_query: str, plan: QueryPlan) -> None:
        for alias, canonical_state in sorted(self.semantic.state_normalization.items(), key=lambda item: len(item[0]), reverse=True):
            alias_term = _canonicalize(alias)
            if alias_term and re.search(rf"(?<!\\w){re.escape(alias_term)}(?!\\w)", normalized_query):
                filter_spec = {
                    "field": "ship-state",
                    "operator": "=",
                    "value": canonical_state,
                }

                if filter_spec not in plan.filters:
                    plan.filters.append(filter_spec)

    def _apply_default_grouping(self, normalized_query: str, plan: QueryPlan) -> None:
        if re.search(r"\b(by|per)\b", normalized_query) and plan.dimensions:
            plan.group_by = list(plan.dimensions)

    def _apply_sorting_and_limit(self, normalized_query: str, plan: QueryPlan) -> None:
        limit_match = re.search(r"(?:top|bottom)\s+(\d+)", normalized_query)
        if limit_match:
            plan.limit = int(limit_match.group(1))

        if any(term in normalized_query for term in ("top", "highest", "most")):
            plan.order = "DESC"
        elif any(term in normalized_query for term in ("bottom", "lowest", "least")):
            plan.order = "ASC"
        else:
            plan.order = "DESC"

        if plan.metrics:
            plan.order_by = plan.metrics[0]

    def _deduplicate_plan(self, plan: QueryPlan) -> None:
        plan.metrics = list(dict.fromkeys(plan.metrics))
        plan.dimensions = list(dict.fromkeys(plan.dimensions))
        plan.group_by = list(dict.fromkeys(plan.group_by))

        unique_filters: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str]] = set()

        for filter_spec in plan.filters:
            key = (
                str(filter_spec.get("field")),
                str(filter_spec.get("operator")),
                str(filter_spec.get("value")),
            )

            if key in seen:
                continue

            seen.add(key)
            unique_filters.append(filter_spec)

        plan.filters = unique_filters

    def pretty_print(self, plan: QueryPlan) -> None:
        logger.info("Metric      : %s", plan.metrics)
        logger.info("Dimensions  : %s", plan.dimensions)
        logger.info("Filters     : %s", plan.filters)
        logger.info("Group By    : %s", plan.group_by)
        logger.info("Order       : %s", plan.order)
        logger.info("Limit       : %s", plan.limit)


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
        "bottom 5 states by revenue",
    ]

    for question in tests:
        print("\nQuestion:", question)
        plan = parser.parse(question)
        parser.pretty_print(plan)