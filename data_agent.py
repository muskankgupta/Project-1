
# from config import get_connection
# from load_data import load_csv


# class DataAgent:


#     def __init__(self):
#         pass


#     def ingest_data(self):

#         result = load_csv()

#         return result
#     def execute_query(self, sql):

#        print("\nGenerated SQL:")
#        print(sql)

#        conn = get_connection()

#        cursor = conn.cursor()

#        cursor.execute(sql)

#        result = cursor.fetchall()

#        print("Database Result:")
#        print(result)

#        cursor.close()
#        conn.close()
#        if result and isinstance(result[0], tuple):
#            return float(result[0][0])

#        return result

from semantics import get_metric
from metric_executor import execute_metric

class DataAgent:

    def __init__(self, df):
        self.df = df

    def run(self, plan: dict):

        results = {}

        for metric_name in plan["metrics"]:

            metric_spec = get_metric(metric_name)

            if not metric_spec:
                continue

            group_by = plan.get("dimensions")

            result = execute_metric(self.df, metric_spec, group_by)

            results[metric_name] = result

        return results