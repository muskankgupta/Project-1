"""
sql_generation_agent.py

Converts a QueryPlan into semantic SQL.
"""

from __future__ import annotations

import re
from typing import Any

from loader import SemanticLoader, get_semantic_loader
from parser_agent import QueryPlan


class SQLGenerationAgent:
    def __init__(self, semantic_loader: SemanticLoader | None = None) -> None:
        self.semantic = semantic_loader or get_semantic_loader()

    def generate(self, plan: QueryPlan) -> str:
        metric_names = plan.metrics or ([plan.metric] if plan.metric else [])
        if not metric_names:
            raise ValueError("No metric detected.")

        metrics = []
        for metric_name in metric_names:
            metric = self.semantic.get_metric(metric_name)
            if metric is None:
                raise ValueError(f"Unknown metric: {metric_name}")
            metrics.append(metric)

        table_name = self._build_table_name(metrics[0])
        select_parts = [self._quote_identifier(self.semantic.to_sql_column(dimension)) for dimension in plan.group_by]

        for metric in metrics:
            formula = self._normalize_formula(metric.formula)
            select_parts.append(f"{formula} AS {self._quote_identifier(metric.name)}")

        sql = ["SELECT", f"    {', '.join(select_parts)}", f"FROM {table_name}"]
        conditions = list(metrics[0].default_filters or [])
        conditions.extend(self._build_filter_clauses(plan.filters))

        if conditions:
            sql.append("WHERE " + "\nAND ".join(conditions))

        if plan.group_by:
            sql.append("GROUP BY " + ", ".join(self._quote_identifier(self.semantic.to_sql_column(dimension)) for dimension in plan.group_by))

        order_by = plan.order_by or metrics[0].name
        order_by_sql = self.semantic.to_sql_column(order_by) if self.semantic.resolve_field(order_by) else order_by
        sql.append(f"ORDER BY {self._quote_identifier(order_by_sql)} {plan.order}")

        if plan.limit:
            sql.append(f"LIMIT {plan.limit}")

        return "\n".join(sql).strip()

    def _build_table_name(self, metric: Any) -> str:
        parts = [part for part in [metric.catalog, metric.schema, metric.table] if part]
        return ".".join(parts)

    def _build_filter_clauses(self, filters: list[dict[str, Any]]) -> list[str]:
        clauses: list[str] = []

        for filter_spec in filters:
            field = self._quote_identifier(self.semantic.to_sql_column(str(filter_spec.get("field"))))
            operator = str(filter_spec.get("operator", "="))
            value = filter_spec.get("value")

            if isinstance(value, bool):
                rendered_value = "TRUE" if value else "FALSE"
            elif isinstance(value, (int, float)):
                rendered_value = str(value)
            else:
                rendered_value = f"'{value}'"

            clauses.append(f"{field} {operator} {rendered_value}")

        return clauses

    def _normalize_formula(self, formula: str) -> str:
        normalized = formula.strip()

        for field_name in sorted(self.semantic.field_specs, key=len, reverse=True):
            sql_name = self.semantic.to_sql_column(field_name)
            normalized = re.sub(rf"\b{re.escape(field_name)}\b", sql_name, normalized)

        return normalized

    def _quote_identifier(self, identifier: str) -> str:
        if identifier.startswith("`") and identifier.endswith("`"):
            return identifier

        if any(character in identifier for character in (" ", "-", ".")):
            return f"`{identifier}`"

        return identifier
