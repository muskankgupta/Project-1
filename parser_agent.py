# class ParserAgent:

#     def parse_intent(self, query):
#         query = query.lower()

#         # fix typo
#         query = query.replace("quater", "quarter")

#         aggregation = None
#         column = None
#         filters = {}

#         # aggregation
#         if "total" in query or "sum" in query:
#             aggregation = "SUM"

#         # column
#         if "revenue" in query:
#             column = "amount"

#         # quarter detection
#         if any(word in query for word in ["q1", "first quarter", "1st quarter"]):
#             filters["quarter"] = 1
#         elif any(word in query for word in ["q2", "second quarter", "2nd quarter"]):
#             filters["quarter"] = 2
#         elif any(word in query for word in ["q3", "third quarter", "3rd quarter"]):
#             filters["quarter"] = 3
#         elif any(word in query for word in ["q4", "fourth quarter", "4th quarter"]):
#             filters["quarter"] = 4

#         return {
#             "aggregation": aggregation,
#             "column": column,
#             "filters": filters
#         }

class ResponseAgent:


    def format_response(self, question, result):


        if result and result[0][0] is not None:

            value = result[0][0]


            return f"""
Answer:
The result for '{question}' is {value}.
"""


        return "No data found."