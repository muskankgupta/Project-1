"""
insight_agent.py

Generates business insights from SQL query results.
"""


class InsightAgent:
    """
    Generates analytical insights from query results.
    """

    def __init__(self):
        pass

    def generate(self, user_query: str, result):

        if result is None:
            return []

        # ------------------------------------------
        # Support tuple or dictionary result
        # ------------------------------------------

        if isinstance(result, tuple):

            columns, rows = result

        elif isinstance(result, dict):

            columns = result.get("columns", [])
            rows = result.get("rows", [])

        else:
            return []

        if not rows:
            return []

        insights = []

        # ------------------------------------------
        # Single KPI
        # ------------------------------------------

        if len(columns) == 1:

            value = rows[0][0]

            if isinstance(value, float):
                value = f"{value:,.2f}"

            elif isinstance(value, int):
                value = f"{value:,}"

            insights.append(f"The overall value is {value}.")

            return insights

        # ------------------------------------------
        # Aggregated results
        # Assumes first column = dimension
        # Last column = metric
        # ------------------------------------------

        metric_index = len(columns) - 1

        numeric_rows = []

        for row in rows:

            try:
                value = float(row[metric_index])
                numeric_rows.append((row[0], value))

            except Exception:
                continue

        if not numeric_rows:
            return insights

        highest = max(numeric_rows, key=lambda x: x[1])
        lowest = min(numeric_rows, key=lambda x: x[1])

        total = sum(v for _, v in numeric_rows)

        insights.append(
            f"Highest {columns[0]}: {highest[0]} ({highest[1]:,.2f})"
        )

        insights.append(
            f"Lowest {columns[0]}: {lowest[0]} ({lowest[1]:,.2f})"
        )

        insights.append(
            f"Total {columns[-1]}: {total:,.2f}"
        )

        if len(numeric_rows) >= 3:

            top3 = sorted(
                numeric_rows,
                key=lambda x: x[1],
                reverse=True
            )[:3]

            top_text = ", ".join(
                f"{name} ({value:,.2f})"
                for name, value in top3
            )

            insights.append(f"Top 3: {top_text}")

        if total > 0:

            pct = highest[1] / total * 100

            insights.append(
                f"{highest[0]} contributes {pct:.1f}% of the total."
            )

        return insights