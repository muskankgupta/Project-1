"""
chart_agent.py

Suggests the best chart based on query results.
"""


class ChartAgent:

    def __init__(self):
        pass

    def suggest(self, user_query: str, result):

        if result is None:
            return "No chart recommended."

        if isinstance(result, tuple):
            columns, rows = result

        elif isinstance(result, dict):
            columns = result.get("columns", [])
            rows = result.get("rows", [])

        else:
            return "No chart recommended."

        if not rows:
            return "No chart recommended."

        # KPI
        if len(columns) == 1:
            return "KPI Card"

        # Dimension + Metric
        if len(columns) == 2:

            dimension = columns[0].lower()

            if "date" in dimension or "month" in dimension or "year" in dimension:
                return "Line Chart"

            if len(rows) <= 10:
                return "Bar Chart"

            return "Column Chart"

        # Multiple dimensions
        if len(columns) > 2:
            return "Pivot Table"

        return "Table"