"""
validation_agent.py

Validates and improves the QueryPlan before SQL generation.
"""

from __future__ import annotations

from typing import Any

from loader import SemanticLoader, get_semantic_loader
from parser_agent import QueryPlan


class ValidationAgent:
    def __init__(self, semantic_loader: SemanticLoader | None = None) -> None:
        self.semantic = semantic_loader or get_semantic_loader()

    def validate(self, plan: QueryPlan) -> QueryPlan:
        plan.metrics = self._normalize_metrics(plan)
        plan.dimensions = self._normalize_dimensions(plan.dimensions)
        plan.filters = self._normalize_filters(plan.filters)
        plan.group_by = self._normalize_dimensions(plan.group_by or plan.dimensions)

        if not plan.order_by and plan.metrics:
            plan.order_by = plan.metrics[0]

        if plan.limit is not None and plan.limit <= 0:
            plan.limit = None

        if not plan.metrics:
            inferred = self.semantic.infer_metric_from_question(plan.rewritten_query or plan.raw_query)
            if inferred:
                plan.metrics = [inferred]

        if not plan.metrics:
            raise ValueError("No metric detected. Try asking for revenue, units sold, order count, etc.")

        plan.metric = plan.metrics[0]
        return plan

    def _normalize_metrics(self, plan: QueryPlan) -> list[str]:
        metrics: list[str] = []

        candidates = plan.metrics or ([plan.metric] if plan.metric else [])
        for metric_name in candidates:
            if not metric_name:
                continue

            if self.semantic.get_metric(metric_name):
                metrics.append(metric_name)

        return list(dict.fromkeys(metrics))

    def _normalize_dimensions(self, dimensions: list[str]) -> list[str]:
        normalized: list[str] = []

        for dimension in dimensions:
            field = self.semantic.get_field(dimension)
            if field is None:
                resolved = self.semantic.resolve_field(dimension)
                if resolved:
                    dimension = resolved
                    field = self.semantic.get_field(resolved)

            if field is None or field.role in {"measure", "ignore"}:
                continue

            normalized.append(dimension)

        return list(dict.fromkeys(normalized))

    def _normalize_filters(self, filters: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized_filters: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str]] = set()

        for filter_spec in filters:
            field = filter_spec.get("field")
            field_spec = self.semantic.get_field(str(field)) if field else None

            if field_spec is None and field:
                resolved = self.semantic.resolve_field(str(field))
                if resolved:
                    field = resolved
                    field_spec = self.semantic.get_field(resolved)

            if field_spec is None:
                continue

            normalized = {
                "field": field,
                "operator": filter_spec.get("operator", "="),
                "value": filter_spec.get("value"),
            }

            key = (str(normalized["field"]), str(normalized["operator"]), str(normalized["value"]))
            if key in seen:
                continue

            seen.add(key)
            normalized_filters.append(normalized)

        return normalized_filters
