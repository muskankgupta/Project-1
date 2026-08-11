# Databricks notebook source

# import os
# import re
# from datetime import datetime
# from pyspark.sql import SparkSession  

# spark = SparkSession.builder.appName("MetricMind-Bronze").getOrCreate()

# PROJECT_PATH = "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind"


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
