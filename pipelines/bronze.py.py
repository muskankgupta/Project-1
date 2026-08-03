# Databricks notebook source

# import os
# import re
# from datetime import datetime
# from pyspark.sql import SparkSession

# spark = SparkSession.builder.appName("MetricMind-Bronze").getOrCreate()

# PROJECT_PATH = "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind"

# RAW_FILE = os.path.join(
#     PROJECT_PATH,
#     "raw_data",
#     "Amazon Sale Report.csv"
# )

# BRONZE_PATH = os.path.join(
#     PROJECT_PATH,
#     "lakehouse",
#     "bronze",
#     "amazon_sales"
# )

# REPORT_PATH = os.path.join(
#     PROJECT_PATH,
#     "reports"
# )

# BRONZE_LOG = os.path.join(
#     REPORT_PATH,
#     "bronze_log.txt"
# )

# os.makedirs(REPORT_PATH, exist_ok=True)

# print("=" * 60)
# print("BRONZE LAYER : RAW DATA INGESTION")
# print("=" * 60)

# print("\nLoading Amazon Sales Dataset...")

# df = (
#     spark.read
#          .option("header", "true")
#          .option("inferSchema", "true")
#          .option("multiLine", "true")
#          .csv(RAW_FILE)
# )

# print("Dataset Loaded Successfully!")

# print("\nCleaning Column Names...")

# new_columns = []

# for column in df.columns:

#     new_name = re.sub(r"[^A-Za-z0-9_]", "_", column)
#     new_name = re.sub(r"_+", "_", new_name)
#     new_name = new_name.strip("_")

#     new_columns.append(new_name)

# df = df.toDF(*new_columns)

# print("Column Names Cleaned Successfully!")

# rows = df.count()
# columns = len(df.columns)

# print("\nDataset Shape")
# print("-" * 40)
# print("Rows :", rows)
# print("Columns :", columns)

# print("\nColumn Names")
# print("-" * 40)

# for column in df.columns:
#     print(column)

# print("\nSchema")
# print("-" * 40)

# df.printSchema()

# print("\nFirst 10 Records")
# print("-" * 40)

# df.show(10, truncate=False)

# print("\nLast 10 Records")
# print("-" * 40)

# df.tail(10)

# print("\nWriting Bronze Delta Table...")

# (
#     df.write
#       .format("delta")
#       .mode("overwrite")
#       .save(BRONZE_PATH)
# )

# print("Bronze Delta Table Created Successfully!")

# with open(BRONZE_LOG, "w") as file:

#     file.write("MetricMind Bronze Layer Log\n")
#     file.write("=" * 60 + "\n\n")

#     file.write(f"Execution Time : {datetime.now()}\n\n")

#     file.write(f"Input File : {RAW_FILE}\n")
#     file.write(f"Bronze Path : {BRONZE_PATH}\n\n")

#     file.write(f"Rows : {rows}\n")
#     file.write(f"Columns : {columns}\n\n")

#     file.write("Column Names\n")
#     file.write("-" * 40 + "\n")

#     for column in df.columns:
#         file.write(column + "\n")

# print("Bronze Log Created Successfully!")

# print("\nVerifying Bronze Delta Table...")

# bronze_df = spark.read.format("delta").load(BRONZE_PATH)

# bronze_df.show(10, truncate=False)

# print("\nDataset Summary")
# print("-" * 40)
# print("Total Rows :", bronze_df.count())
# print("Total Columns :", len(bronze_df.columns))

# print("\nBronze Layer Completed Successfully")
# print("=" * 60)
# ============================================
# METRICMIND - BRONZE LAYER (FINAL VERSION)
# ============================================

# ============================================
# METRICMIND - BRONZE LAYER (FINAL FIXED)
# ============================================

import re

# ============================================
# CONFIG (UNITY CATALOG)
# ============================================

cfg = {
    "catalog": "workspace",
    "schema": "default"
}

bronze_table = f"{cfg['catalog']}.{cfg['schema']}.amazon_sales_raw"

# ✅ USE WORKSPACE FILE PATH (NOT DBFS)
file_path = "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind/raw_data/Amazon Sale Report.csv"

# ============================================
# LOAD DATA
# ============================================

print("Loading Dataset...")

df = (
    spark.read
         .option("header", "true")
         .option("inferSchema", "true")
         .option("multiLine", "true")
         .csv(file_path)
)

print("Dataset Loaded!")

# ============================================
# CLEAN COLUMN NAMES
# ============================================

new_columns = []

for column in df.columns:
    new_name = re.sub(r"[^A-Za-z0-9_]", "_", column)
    new_name = re.sub(r"_+", "_", new_name)
    new_name = new_name.strip("_")
    new_columns.append(new_name)

df = df.toDF(*new_columns)

print("Columns Cleaned!")

# ============================================
# WRITE AS TABLE (IMPORTANT)
# ============================================

print("Saving Bronze Table...")

df.write \
  .mode("overwrite") \
  .saveAsTable(bronze_table)

print("✅ Bronze table created!")

# ============================================
# VERIFY
# ============================================

print("Verifying...")

spark.read.table(bronze_table).show(10)