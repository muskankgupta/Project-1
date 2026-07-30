class ReasoningAgent:

    def generate(self, query: str, results: dict) -> str:

        if not results:
            return "I could not compute an answer for your query."

        response = f"Query: {query}\n\n"

        for metric, value in results.items():

            if hasattr(value, "to_string"):
                response += f"\n{metric}:\n{value.to_string(index=False)}\n"
            else:
                response += f"\n{metric}: {value}\n"

        return response