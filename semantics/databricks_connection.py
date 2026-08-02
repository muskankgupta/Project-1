# from databricks import sql
# import os

# class DatabricksConnection:

#     def __init__(self):
#         self.connection = sql.connect(
#             server_hostname=os.getenv("DB_HOST"),
#             http_path=os.getenv("DB_HTTP_PATH"),
#             access_token=os.getenv("DB_TOKEN")
#         )

#     def cursor(self):
#         return self.connection.cursor()
# from databricks import sql
# import os


# class DatabricksConnection:

#     def __new__(cls):
#         return sql.connect(
#             server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
#             http_path=os.getenv("DATABRICKS_HTTP_PATH"),
#             access_token=os.getenv("DATABRICKS_TOKEN"),
#         )
from databricks import sql
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

class DatabricksConnection:

    def __new__(cls):
        return sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN"),
        )