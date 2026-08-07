# Databricks notebook source

from datetime import datetime
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, DoubleType

### ============================================
### CONFIG (UNITY CATALOG)
### ============================================

cfg = {
    "catalog": "workspace",
    "schema": "default"
}

bronze_table = f"{cfg['catalog']}.{cfg['schema']}.amazon_sales_raw"
silver_table = f"{cfg['catalog']}.{cfg['schema']}.amazon_sales_clean"

# ============================================
# START
# ============================================

print("=" * 60)
print("SILVER LAYER : DATA CLEANING")
print("=" * 60)

# ============================================
# LOAD BRONZE DATA (FROM TABLE)
# ============================================

print("\nLoading Bronze Table...")

df = spark.read.table(bronze_table)

print("Bronze Table Loaded Successfully!")

rows_before = df.count()

# ============================================
# REMOVE DUPLICATES
# ============================================

print("\nRemoving Duplicate Records...")

df = df.dropDuplicates()

rows_after = df.count()
duplicates_removed = rows_before - rows_after

print("Duplicates Removed :", duplicates_removed)

# ============================================
# CHECK MISSING VALUES
# ============================================

print("\nChecking Missing Values...")

missing_df = df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
])

missing_df.show(truncate=False)

# ============================================
# FILL MISSING VALUES
# ============================================

print("\nFilling Missing Values...")

string_columns = [
    field.name
    for field in df.schema.fields
    if field.dataType.simpleString() == "string"
]

numeric_columns = [
    field.name
    for field in df.schema.fields
    if field.dataType.simpleString() in
    ["int", "bigint", "double", "float", "decimal"]
]

# Fill string columns
for column in string_columns:
    df = df.fillna({column: "Unknown"})

# Fill numeric columns with median
for column in numeric_columns:

    median = (
        df.approxQuantile(column, [0.5], 0.01)[0]
        if df.filter(col(column).isNotNull()).count() > 0
        else 0
    )

    df = df.fillna({column: median})

print("Missing Values Filled Successfully!")

# ============================================
# TYPE CONVERSIONS
# ============================================

if "Date" in df.columns:
    df = df.withColumn(
        "Date",
        to_date(col("Date"), "MM-dd-yy")
    )

if "Qty" in df.columns:
    df = df.withColumn(
        "Qty",
        col("Qty").cast(IntegerType())
    )

if "Amount" in df.columns:
    df = df.withColumn(
        "Amount",
        col("Amount").cast(DoubleType())
    )

print("Data Types Converted Successfully!")

# ============================================
# TEXT CLEANING
# ============================================

print("\nCleaning Text Columns...")

for column in string_columns:
    df = df.withColumn(
        column,
        initcap(trim(col(column)))
    )

if "ship_state" in df.columns:
    df = df.withColumn(
        "ship_state",
        regexp_replace(col("ship_state"), "&", "And")
    )

# Drop unwanted columns like "Unnamed: 0"
unnamed_columns = [
    c for c in df.columns
    if c.lower().startswith("unnamed")
]

if unnamed_columns:
    df = df.drop(*unnamed_columns)

print("Text Cleaning Completed!")

# ============================================
# WRITE SILVER TABLE (UNITY CATALOG)
# ============================================

print("\nWriting Silver Table...")

df.write \
  .mode("overwrite") \
  .saveAsTable(silver_table)

print("Silver Table Created Successfully!")

# ============================================
# VERIFY OUTPUT
# ============================================

print("\nVerifying Silver Table...")

silver_df = spark.read.table(silver_table)

silver_df.show(10, truncate=False)

print("\nFinal Summary")
print("-" * 40)

print("Rows :", silver_df.count())
print("Columns :", len(silver_df.columns))

print("\nRemaining Missing Values")

silver_df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in silver_df.columns
]).show()

print("\nSilver Layer Completed Successfully")
print("=" * 60)
