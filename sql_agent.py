"""
sql_generation_agent.py

Converts a QueryPlan into executable Databricks SQL.
"""

from parser_agent import QueryPlan
from semantics import METRICS


class SQLGenerationAgent:

    def __init__(self):
        pass

    def generate(self, plan: QueryPlan) -> str:

        if plan.metric is None:
            raise ValueError("No metric detected.")

        metric = METRICS[plan.metric]

        # --------------------------------------------------
        # Build fully-qualified table name
        # --------------------------------------------------

        parts = []

        if metric.catalog:
            parts.append(metric.catalog)

        if metric.schema:
            parts.append(metric.schema)

        parts.append(metric.table)

        table_name = ".".join(parts)

        # --------------------------------------------------
        # SELECT
        # --------------------------------------------------

        select_parts = []
        group_parts = []

        for dim in plan.group_by:
            select_parts.append(dim)
            group_parts.append(dim)

        select_parts.append(
            f"{metric.formula} AS {metric.name}"
        )

        sql = f"""
SELECT
    {", ".join(select_parts)}
FROM {table_name}
"""

        # --------------------------------------------------
        # Default metric filters
        # --------------------------------------------------

        conditions = []

        for default_filter in metric.default_filters:
            conditions.append(default_filter)

        # --------------------------------------------------
        # User filters
        # --------------------------------------------------

        if plan.filters:

            merged = {}

            for f in plan.filters:

                field = f["field"]

                merged.setdefault(field, []).append(f)

            for field, filters in merged.items():

                # Single value
                if len(filters) == 1:

                    f = filters[0]

                    value = f["value"]

                    if isinstance(value, str):
                        value = f"'{value}'"

                    conditions.append(
                        f"{field} {f['operator']} {value}"
                    )

                # Multiple values → IN clause
                else:

                    values = []

                    for f in filters:

                        value = f["value"]

                        if isinstance(value, str):
                            value = f"'{value}'"

                        values.append(value)

                    conditions.append(
                        f"{field} IN ({', '.join(values)})"
                    )

        # --------------------------------------------------
        # WHERE
        # --------------------------------------------------

        if conditions:
            sql += "\nWHERE " + "\nAND ".join(conditions)

        # --------------------------------------------------
        # GROUP BY
        # --------------------------------------------------

        if group_parts:
            sql += "\nGROUP BY " + ", ".join(group_parts)

        # --------------------------------------------------
        # ORDER BY
        # --------------------------------------------------

        order_column = (
            plan.order_by
            if plan.order_by
            else metric.name
        )

        sql += f"\nORDER BY {order_column} {plan.order}"

        # --------------------------------------------------
        # LIMIT
        # --------------------------------------------------

        if plan.limit:
            sql += f"\nLIMIT {plan.limit}"

        return sql.strip()