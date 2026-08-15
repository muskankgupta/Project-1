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
import socket
from pathlib import Path

from databricks import sql
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

# Connection/socket timeouts in seconds. Ensures the backend fails fast
# (instead of hanging indefinitely) when the configured Databricks host is
# unreachable — e.g. a network-level DNS block or a down warehouse.
CONNECT_TIMEOUT_SECONDS = int(os.getenv("DATABRICKS_CONNECT_TIMEOUT", "8"))
SOCKET_TIMEOUT_SECONDS = int(os.getenv("DATABRICKS_SOCKET_TIMEOUT", "15"))

_MODULE_DIR = Path(__file__).resolve().parent
for candidate in (_MODULE_DIR / ".env", _MODULE_DIR / "env"):
    if candidate.exists():
        load_dotenv(candidate, override=False)
        break


def _hostname_resolves(server_hostname: str) -> bool:
    """Return True if the hostname resolves via DNS (fast check)."""
    try:
        socket.getaddrinfo(server_hostname, None)
        return True
    except (socket.gaierror, OSError):
        return False


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

        if not _hostname_resolves(server_hostname):
            raise ConnectionError(
                f"Databricks hostname '{server_hostname}' does not resolve via DNS. "
                "Check the network/allowlist or the DATABRICKS_SERVER_HOSTNAME value."
            )

        logger.info("Opening Databricks SQL connection to %s", server_hostname)
        return sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token,
            _user_agent_entry=None,
            connect_args={
                "connect_timeout": CONNECT_TIMEOUT_SECONDS,
                "socket_timeout": SOCKET_TIMEOUT_SECONDS,
            },
        )


def get_connection():
    return DatabricksConnection()
