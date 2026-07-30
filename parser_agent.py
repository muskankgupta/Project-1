# import re

# class ParserAgent:

#     def parse(self, question: str) -> dict:
#         question = question.lower()

#         intent = {
#             "aggregation": None,
#             "column": None,
#             "filters": {}
#         }


#         if any(word in question for word in ["total", "sum", "revenue"]):
#             intent["aggregation"] = "SUM"

#         elif any(word in question for word in ["average", "avg"]):
#             intent["aggregation"] = "AVG"

#         elif any(word in question for word in ["count", "number of", "how many"]):
#             intent["aggregation"] = "COUNT"

#         if "revenue" in question or "sales" in question:
#             intent["column"] = "amount"

#         elif "orders" in question:
#             intent["column"] = "order_id"

#         elif "units" in question or "quantity" in question:
#             intent["column"] = "quantity"

#         quarter_match = re.search(r'q([1-4])', question)
#         if quarter_match:
#             intent["filters"]["quarter"] = int(quarter_match.group(1))

#         year_match = re.search(r'(20\d{2})', question)
#         if year_match:
#             intent["filters"]["year"] = int(year_match.group(1))

#         if "state" in question:
#             # naive extraction (can improve later)
#             words = question.split()
#             if "in" in words:
#                 idx = words.index("in")
#                 if idx + 1 < len(words):
#                     intent["filters"]["state"] = words[idx + 1]

#         if "category" in question:
#             words = question.split()
#             if "in" in words:
#                 idx = words.index("in")
#                 if idx + 1 < len(words):
#                     intent["filters"]["category"] = words[idx + 1]

#         return intent

import json
from semantics import SEMANTIC_LAYER

class ParserAgent:

    def __init__(self, llm=None):
        self.llm = llm  # optional (can plug OpenAI later)

    def parse(self, user_query: str) -> dict:
        """
        Convert natural language → structured query plan
        """

        # 🔥 For now: simple rule-based fallback (replace with LLM later)
        query = user_query.lower()

        plan = {
            "metrics": [],
            "dimensions": [],
            "filters": [],
            "time_range": None
        }

        # metric detection
        if "revenue" in query or "sales" in query:
            plan["metrics"].append("revenue")

        if "orders" in query:
            plan["metrics"].append("order_count")

        # dimension detection
        if "state" in query:
            plan["dimensions"].append("ship-state")

        if "category" in query:
            plan["dimensions"].append("Category")

        return plan