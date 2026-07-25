class ResponseAgent:

    def format_response(self, question, result):

        if result is None:
            return "No data found."

        value = float(result)

        if value > 1_000_000:
            return f"""
📊 Insight:
Total revenue is ${value:,.2f}

🚀 High revenue detected!
"""

        return f"""
📊 Insight:
Total revenue is ${value:,.2f}

💡 Moderate performance observed.
"""