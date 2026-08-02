# # """
# # loader.py
# # =========
# # Optional helper: loads the raw Amazon Sale Report CSV and applies the
# # cleanup/derivation rules described in schema.py (state normalization,
# # has_promotion flag, is_cancelled flag).

# # Kept separate from schema.py so that schema.py itself has zero third-party
# # dependencies (no pandas) and can be imported by any lightweight agent.
# # Only import loader.py where pandas is already a dependency (e.g. data_agent.py).
# # """

# # from typing import Optional

# # try:
# #     import pandas as pd
# # except ImportError as e:
# #     raise ImportError(
# #         "loader.py requires pandas. Install with: pip install pandas --break-system-packages"
# #     ) from e

# # from .schema import normalize_state


# # def load_dataset(csv_path: str) -> "pd.DataFrame":
# #     """
# #     Load the Amazon Sale Report CSV and apply semantic-layer-driven cleanup:
# #       - ship-state_clean: normalized state names (see schema.STATE_NORMALIZATION)
# #       - has_promotion: bool, True if promotion-ids is not null
# #       - is_cancelled: bool, True if Status == 'Cancelled'
# #     """
# #     df = pd.read_csv(csv_path, low_memory=False)

# #     if "ship-state" in df.columns:
# #         df["ship-state_clean"] = df["ship-state"].map(normalize_state)

# #     if "promotion-ids" in df.columns:
# #         df["has_promotion"] = df["promotion-ids"].notna()

# #     if "Status" in df.columns:
# #         df["is_cancelled"] = df["Status"] == "Cancelled"

# #     return df
# from pyspark.sql import SparkSession
# from schema import normalize_state, add_flags  # assuming these functions exist

# spark = SparkSession.builder.getOrCreate()

# def load_data():
#     df = spark.table("amazon_sales")

#     # Apply semantic transformations
#     df = df.withColumn("ship_state", normalize_state(df["ship_state"]))
#     df = add_flags(df)

#     return df

"""
loader.py
=========

Helper for executing SQL queries using the Databricks SQL Connector.
"""

from .databricks_connection import DatabricksConnection


class DataLoader:

    def __init__(self):
        self.connection = DatabricksConnection()

    def execute(self, query: str):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)

            rows = cursor.fetchall()
            columns = [c[0] for c in cursor.description]

            return columns, rows

        finally:
            cursor.close()