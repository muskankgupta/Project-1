# class ReasoningAgent:

#     def generate(self, query: str, results: dict) -> str:

#         if not results:
#             return "I could not compute an answer for your query."

#         response = f"Query: {query}\n\n"

#         for metric, value in results.items():

#             if hasattr(value, "to_string"):
#                 response += f"\n{metric}:\n{value.to_string(index=False)}\n"
#             else:
#                 response += f"\n{metric}: {value}\n"

#         return response
"""
reasoning_agent.py

Converts SQL results into natural language responses.
"""


class ReasoningAgent:
    """
    Converts Databricks query results into a human-readable answer.
    """

    def __init__(self):
        pass

    def generate(self, user_query: str, result):

        if result is None:
            return "No results were returned."

        # ------------------------------------------
        # Handle dict format
        # ------------------------------------------

        if isinstance(result, dict):

            columns = result.get("columns", [])
            rows = result.get("rows", [])

        # ------------------------------------------
        # Handle tuple format returned by DataLoader
        # ------------------------------------------

        elif isinstance(result, tuple):

            columns, rows = result

        else:
            return "Unsupported result format."

        # ------------------------------------------
        # No rows
        # ------------------------------------------

        if not rows:
            return "No matching records were found."

        # ------------------------------------------
        # Single value result
        # ------------------------------------------

        if len(columns) == 1 and len(rows) == 1:

            value = rows[0][0]

            if isinstance(value, float):
                value = f"{value:,.2f}"

            elif isinstance(value, int):
                value = f"{value:,}"

            return f"The answer is {value}."

        # ------------------------------------------
        # Multi-row result
        # ------------------------------------------

        output = []

        output.append(f"Results for: {user_query}\n")

        output.append(" | ".join(columns))
        output.append("-" * 70)

        for row in rows:

            formatted = []

            for item in row:

                if isinstance(item, float):
                    formatted.append(f"{item:,.2f}")

                elif isinstance(item, int):
                    formatted.append(f"{item:,}")

                else:
                    formatted.append(str(item))

            output.append(" | ".join(formatted))

        output.append(f"\n{len(rows)} row(s) returned.")

        return "\n".join(output)