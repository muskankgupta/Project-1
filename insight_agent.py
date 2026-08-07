"""
insight_agent.py

Generates business insights from SQL query results.

Insights are formatted as short executive narratives. Numeric values use
Indian compact notation (₹ Cr / ₹ L) where the raw unit is INR, so output
reads naturally in a business dashboard or chat response.
"""

INR_METRIC_KEYS = {"revenue", "gross_revenue", "average_order_value", "amount", "sales"}


def _compact_inr(value: float) -> str:
    """Format a raw INR number using Indian compact units (Cr / L / K)."""
    absolute = abs(value)

    if absolute >= 10_000_000:
        return f"₹{value / 10_000_000:.2f} Cr"
    if absolute >= 100_000:
        return f"₹{value / 100_000:.2f} L"
    if absolute >= 1_000:
        return f"₹{value / 1_000:.1f}K"

    return f"₹{value:,.0f}"


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

        metric_key = (columns[-1] if columns else "").lower()
        query_tokens = " ".join(user_query.lower().split())
        is_currency = (
            metric_key in INR_METRIC_KEYS
            or "amount" in metric_key
            or any(term in query_tokens for term in ("revenue", "sales", "gmv", "aov", "order value"))
        )
        is_currency = is_currency and not any(
            term in metric_key for term in ("count", "orders", "units", "items", "share")
        )

        # ------------------------------------------
        # Single KPI
        # ------------------------------------------

        if len(columns) == 1:

            value = rows[0][0]

            if is_currency and isinstance(value, (int, float)):
                insights.append(f"The overall value is {_compact_inr(float(value))}.")
            elif isinstance(value, float):
                insights.append(f"The overall value is {value:,.2f}.")
            elif isinstance(value, int):
                insights.append(f"The overall value is {value:,}.")
            else:
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

        def _metric(value: float) -> str:
            return _compact_inr(value) if is_currency else f"{value:,.2f}"

        insights.append(
            f"Highest {columns[0]}: {highest[0]} ({_metric(highest[1])})"
        )

        insights.append(
            f"Lowest {columns[0]}: {lowest[0]} ({_metric(lowest[1])})"
        )

        insights.append(
            f"Total {columns[-1]}: {_metric(total)}"
        )

        if len(numeric_rows) >= 3:

            top3 = sorted(
                numeric_rows,
                key=lambda x: x[1],
                reverse=True
            )[:3]

            top_text = ", ".join(
                f"{name} ({_metric(value)})"
                for name, value in top3
            )

            insights.append(f"Top 3: {top_text}")

        if total > 0:

            pct = highest[1] / total * 100

            insights.append(
                f"{highest[0]} leads with {pct:.1f}% of total {columns[-1]}."
            )

        return insights
