"""
explanation_agent.py

Generates a business-friendly explanation of query results.
"""


class ExplanationAgent:

    def __init__(self):
        pass

    def generate(self, user_query: str, result):

        if result is None:
            return "No explanation available."

        # Support tuple and dict results
        if isinstance(result, tuple):
            columns, rows = result

        elif isinstance(result, dict):
            columns = result.get("columns", [])
            rows = result.get("rows", [])

        else:
            return "No explanation available."

        if not rows:
            return "No data returned."

        # ----------------------------
        # Single KPI
        # ----------------------------

        if len(columns) == 1:

            value = rows[0][0]

            if isinstance(value, float):
                value = f"{value:,.2f}"

            elif isinstance(value, int):
                value = f"{value:,}"

            return (
                f"This query calculates **{columns[0]}** "
                f"for the requested data.\n"
                f"The resulting value is **{value}**."
            )

        # ----------------------------
        # Aggregated Results
        # ----------------------------

        dimension = columns[0]
        metric = columns[-1]

        return (
            f"This query groups the data by **{dimension}** "
            f"and calculates **{metric}** for each group.\n"
            f"{len(rows)} record(s) were returned."
        )