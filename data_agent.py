
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
       if result and isinstance(result[0], tuple):
           return float(result[0][0])

       return result