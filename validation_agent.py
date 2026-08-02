"""
validation_agent.py

Validates and improves the QueryPlan before SQL generation.
"""

from semantics import METRICS, FIELDS
from parser_agent import QueryPlan


class ValidationAgent:

    def __init__(self):
        pass

    def validate(self, plan: QueryPlan) -> QueryPlan:

        # -------------------------------------
        # Metric validation
        # -------------------------------------

        if plan.metric:

            if plan.metric not in METRICS:
                raise ValueError(f"Unknown metric: {plan.metric}")

        else:

            # Default metric when asking about orders
            if any(d == "Order_ID" for d in plan.dimensions):
                plan.metric = "order_count"

        # -------------------------------------
        # Dimension validation
        # -------------------------------------

        valid_dimensions = []

        for dim in plan.dimensions:

            if dim in FIELDS:
                valid_dimensions.append(dim)

        plan.dimensions = valid_dimensions

        # -------------------------------------
        # Remove duplicate dimensions
        # -------------------------------------

        plan.dimensions = list(dict.fromkeys(plan.dimensions))

        # -------------------------------------
        # Validate filters
        # -------------------------------------

        cleaned_filters = []
        seen = set()

        for f in plan.filters:

            key = (
                f["field"],
                f["operator"],
                str(f["value"])
            )

            if key not in seen:

                seen.add(key)
                cleaned_filters.append(f)

        plan.filters = cleaned_filters

        # -------------------------------------
        # GROUP BY
        # -------------------------------------

        if plan.dimensions and not plan.group_by:

            plan.group_by = plan.dimensions.copy()

        # -------------------------------------
        # ORDER BY
        # -------------------------------------

        if plan.metric and plan.order_by is None:

            plan.order_by = plan.metric

        # -------------------------------------
        # LIMIT
        # -------------------------------------

        if plan.limit is not None:

            if plan.limit <= 0:
                plan.limit = None

        # -------------------------------------
        # Require metric
        # -------------------------------------

        if plan.metric is None:

            raise ValueError(
                "No metric detected. Try asking for revenue, units sold, order count, etc."
            )

        return plan