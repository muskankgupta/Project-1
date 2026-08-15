"""
data_agent.py

Executes semantic SQL against Databricks.
"""

from __future__ import annotations

import logging
from typing import Any

from loader import SemanticLoader, get_semantic_loader
from databricks_connection import get_connection


logger = logging.getLogger(__name__)


class DataAgent:
    def __init__(self, semantic_loader: SemanticLoader | None = None) -> None:
        self.semantic = semantic_loader or get_semantic_loader()

    def run(self, request: str | dict[str, Any]):
        sql = request.get("sql") if isinstance(request, dict) else request

        if not sql:
            raise ValueError("DataAgent requires a SQL string or a request dict containing 'sql'.")

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)

            rows = [tuple(row) for row in cursor.fetchall()]
            columns = [column[0] for column in cursor.description] if cursor.description else []

            logger.info("Databricks query executed successfully.")
            return {
                "columns": columns,
                "rows": rows,
                "sql": sql,
                "status": "ok",
            }

        except Exception as exc:
            logger.exception("Databricks query execution failed.")
            return {
                "columns": [],
                "rows": [],
                "sql": sql,
                "status": "error",
                "error": str(exc),
            }

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
