# Databricks notebook source
# # ============================================
# # GOLD LAYER - FINAL CLEAN VERSION
# # ============================================

# from pyspark.sql.functions import sum as _sum

# # --------------------------------------------
# # CONFIG (DEFINE THIS FIRST — fixes cfg error)
# # ---------------------------------------------
# #cfg = {
# #    "catalog": "workspace",
# #    "schema": "default",
# #    "volume": "metricmind"
## }

# # --------------------------------------------
# # FULL TABLE PATHS
# # --------------------------------------------
# silver_table = f"{cfg['catalog']}.{cfg['schema']}.amazon_sales_clean"
# gold_table   = f"{cfg['catalog']}.{cfg['schema']}.total_revenue"

# # --------------------------------------------
# # READ SILVER TABLE (NO DBFS, NO VOLUMES PATH)
# # --------------------------------------------
# df = spark.read.table(silver_table)

# # --------------------------------------------
# # TRANSFORMATION (GOLD LOGIC)
# # --------------------------------------------
# gold_df = df.groupBy("category").agg(
#     _sum("amount").alias("total_revenue")
#  )

# # --------------------------------------------
# # WRITE TO GOLD TABLE (UNITY CATALOG)
# # --------------------------------------------
# gold_df.write \
#     .mode("overwrite") \
#     .saveAsTable(gold_table)

# # --------------------------------------------
# # SHOW RESULT
# # --------------------------------------------
# display(gold_df)

# ============================================
# METRICMIND - GOLD LAYER (FINAL VERSION)
# ============================================

# ============================================
# METRICMIND - GOLD LAYER (FIXED VERSION)
# ============================================
# ============================================
# METRICMIND - GOLD LAYER (FINAL FIXED)
# ============================================

from pyspark.sql.functions import sum, col, round

# ============================================
# CONFIG
# ============================================

cfg = {
    "catalog": "workspace",
    "schema": "default"
}

silver_table = f"{cfg['catalog']}.{cfg['schema']}.amazon_sales_clean"
gold_table = f"{cfg['catalog']}.{cfg['schema']}.category_revenue"

# ============================================
# LOAD DATA
# ============================================

print("Loading Silver Data...")

df = spark.read.table(silver_table)

print("Columns Available:", df.columns)

# ============================================
# USE CORRECT COLUMN NAMES
# ============================================

category_col = "Category"
amount_col = "Amount"

# ============================================
# TRANSFORMATION
# ============================================

print("Calculating Revenue...")

gold_df = (
    df.groupBy(col(category_col))
      .agg(round(sum(col(amount_col)), 2).alias("total_revenue"))
      .orderBy(col("total_revenue").desc())
)

# Rename for standard output
gold_df = gold_df.withColumnRenamed(category_col, "category")

# ============================================
# SAVE
# ============================================

gold_df.write \
    .mode("overwrite") \
    .saveAsTable(gold_table)

print("✅ Gold Table Created Successfully!")

# ============================================
# SHOW OUTPUT
# ============================================

gold_df.show()
