class PlannerAgent:

    def requires_planning(self, question):
        keywords = ["compare", "difference", "vs", "versus"]
        return any(k in question.lower() for k in keywords)

    def decompose(self, question):
        if "q1" in question.lower() and "q2" in question.lower():
            return [
                "total revenue in q1",
                "total revenue in q2"
            ]
        return [question]

    def combine(self, original_question, steps, results):
        if len(results) < 2:
            return " Not enough data to compare."

        diff = results[1] - results[0]

        return f"""
 Comparison Result:

{steps[0]} → ${results[0]:,.2f}
{steps[1]} → ${results[1]:,.2f}

Difference: ${diff:,.2f}
"""