class ParserAgent:
    def run(self, query):
        query = query.lower()
        if "q3" in query or "quarter 3" in query or "third quarter" in query:
            return {
               "metric": "q3_revenue"
            }
        if "q2" in query or "quarter 2" in query or "second quarter" in query:
            return {
               "metric": "q2_revenue"
            }
        if "q4" in query or "quarter 4" in query or "fourth quarter" in query:
            return {
               "metric": "q4_revenue"
            }
        if "q1" in query or "quarter 1" in query or "first quarter" in query:
            return {
               "metric": "q1_revenue"
            }
        else:
            return {
                "status": "error",
                "value": "Invalid query"
            }