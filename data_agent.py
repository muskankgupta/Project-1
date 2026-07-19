# class DataAgent:
#     def __init__(self, data):
#         self.data = data

#     def run(self ,metric: str):
#        if metric in self.data:
#             return {
#                 "status": "success",
#                 "metric": metric,
#                 "value" : self.data[metric]
#             }
#        return {
#             "status": "error"}
from config import get_connection
from load_data import load_csv


class DataAgent:


    def __init__(self):
        pass


    def ingest_data(self):

        result = load_csv()

        return result
    def execute_query(self, sql):

       print("\nGenerated SQL:")
       print(sql)

       conn = get_connection()

       cursor = conn.cursor()

       cursor.execute(sql)

       result = cursor.fetchall()

       print("Database Result:")
       print(result)

       cursor.close()
       conn.close()

       return result


    # def execute_query(self, sql):

    #     conn = get_connection()

    #     cursor = conn.cursor()

    #     cursor.execute(sql)

    #     result = cursor.fetchall()


    #     cursor.close()
    #     conn.close()


    #     return result