# # from data_agent import DataAgent
# # from paresr_agent import ParserAgent
# # from state import State
# # from data import Data
# # class Orchestrator_Agent:
# #     def __init__(self):
# #         self.data_agent = DataAgent(Data)
# #         self.parser_agent = ParserAgent()
# #         self.state = State()
# #     def run(self, user_input):
# #         #step 1: find the quarter from the user input
# #         parsed_data = self.parser_agent.run(user_input)
# #         if "error" in parsed_data:
# #             return {
# #                 "status": "error",
# #                 "value": "Invalid query"
# #             }
# #         print("Parsed Data:", parsed_data)
# #         metric = parsed_data["metric"]
# #         self.state.update("metric", metric)
# #         #step 2: get the data from the data agent
# #         result = self.data_agent.run(metric)
# #         self.state.update("result", result)
# #         return result
# from parser_agent import ParserAgent
# from data_agent import DataAgent
# from config import Database

# class Orchestrator:

#     def __init__(self):
#         self.parser_agent = ParserAgent()
#         self.data_agent = DataAgent()
#         self.db = Database()

#     def run(self, query):
#         # 1️⃣ Parse intent
#         intent = self.parser_agent.parse_intent(query)
#         print("\nParsed Intent:", intent)

#         # 2️⃣ Generate SQL
#         sql_query, params = self.data_agent.generate_query(intent)
#         print("Generated Query:", sql_query)
#         print("Query Parameters:", params)

#         # 3️⃣ DB connection
#         conn = self.db.connect()
#         cursor = conn.cursor()

#         # 4️⃣ Execute query
#         cursor.execute(sql_query, params)
#         result = cursor.fetchall()

#         # 5️⃣ Close connection
#         cursor.close()
#         conn.close()

#         # 6️⃣ Flatten result
#         if result and isinstance(result[0], tuple):
#             return result[0][0]

#         return result
from query_agent import QueryAgent
from data_agent import DataAgent
from parser_agent import ResponseAgent



class Orchestrator:


    def __init__(self):

        self.query_agent = QueryAgent()
        self.data_agent = DataAgent()
        self.response_agent = ResponseAgent()



    def run(self, question):


        sql = self.query_agent.generate_sql(question)


        if sql is None:
            return "I cannot understand your question"



        result = self.data_agent.execute_query(sql)


        answer = self.response_agent.format_response(
            question,
            result
        )


        return answer