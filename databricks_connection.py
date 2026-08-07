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
from __future__ import annotations

import logging
import os
from pathlib import Path

from databricks import sql
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

_MODULE_DIR = Path(__file__).resolve().parent
for candidate in (_MODULE_DIR / ".env", _MODULE_DIR / "env"):
    if candidate.exists():
        load_dotenv(candidate, override=False)
        break


class DatabricksConnection:

    def __new__(cls):
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_TOKEN")

        missing = [
            key
            for key, value in {
                "DATABRICKS_SERVER_HOSTNAME": server_hostname,
                "DATABRICKS_HTTP_PATH": http_path,
                "DATABRICKS_TOKEN": access_token,
            }.items()
            if not value
        ]

        if missing:
            raise EnvironmentError(
                "Missing Databricks configuration values: " + ", ".join(missing)
            )

        logger.info("Opening Databricks SQL connection to %s", server_hostname)
        return sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token,
        )


def get_connection():
    return DatabricksConnection()