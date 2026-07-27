# Databricks notebook source
import pandas as pd
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

print("MetricMind - Delta Lakehouse")


# COMMAND ----------

spark = SparkSession.builder \
    .appName("MetricMind") \
    .getOrCreate()

print("Spark Session Created Successfully")

# COMMAND ----------

file_path = "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind/transformed_data/Amazon Sale Report Transformed.csv"

pandas_df = pd.read_csv(
    file_path,
    low_memory=False
)

print("Dataset Loaded Successfully")

print("Rows :", len(pandas_df))

print("Columns :", len(pandas_df.columns))

# COMMAND ----------

pandas_df.head()

# COMMAND ----------

pandas_df.tail(20)

# COMMAND ----------

pandas_df.info()

# COMMAND ----------

spark_df = spark.createDataFrame(pandas_df)

print("Spark DataFrame Created Successfully")

# COMMAND ----------

spark_df.printSchema()

# COMMAND ----------

display(spark_df.limit(10))

# COMMAND ----------

def clean_column_name(column):

    column = column.lower()

    column = column.strip()

    column = re.sub(r'[^a-zA-Z0-9]+', '_', column)

    return column.strip("_")


new_columns = [

    clean_column_name(c)

    for c in spark_df.columns

]

spark_df = spark_df.toDF(*new_columns)

print("Column Names Cleaned Successfully")

# COMMAND ----------


print("Updated Column Names")

for c in spark_df.columns:

    print(c)

# COMMAND ----------


print("Schema")

spark_df.printSchema()

# COMMAND ----------

total_rows = spark_df.count()

print("Total Records :", total_rows)

# COMMAND ----------

duplicates = total_rows - spark_df.dropDuplicates().count()

print("Duplicate Records :", duplicates)

# COMMAND ----------

missing = spark_df.select(

[
sum(col(c).isNull().cast("int")).alias(c)

for c in spark_df.columns

]

)

display(missing)

# COMMAND ----------

spark_df.createOrReplaceTempView("amazon_sales_temp")

print("Temporary SQL View Created")

# COMMAND ----------

spark.sql("""

SELECT

COUNT(*) AS total_orders

FROM amazon_sales_temp

""").show()

# COMMAND ----------

spark.sql("""

SELECT

SUM(revenue) AS total_revenue

FROM amazon_sales_temp

""").show()

# COMMAND ----------

spark.sql("""

SELECT

category,

SUM(revenue) AS revenue

FROM amazon_sales_temp

GROUP BY category

ORDER BY revenue DESC

LIMIT 10

""").show()

# COMMAND ----------

spark.sql("""

SELECT

region,

SUM(revenue) AS revenue

FROM amazon_sales_temp

GROUP BY region

ORDER BY revenue DESC

""").show()

# COMMAND ----------

from pyspark.sql.functions import when

spark_df = spark_df.withColumn(
    "month_name",
    when(col("month")==1,"January")
    .when(col("month")==2,"February")
    .when(col("month")==3,"March")
    .when(col("month")==4,"April")
    .when(col("month")==5,"May")
    .when(col("month")==6,"June")
    .when(col("month")==7,"July")
    .when(col("month")==8,"August")
    .when(col("month")==9,"September")
    .when(col("month")==10,"October")
    .when(col("month")==11,"November")
    .otherwise("December")
)

# COMMAND ----------

spark_df.createOrReplaceTempView("amazon_sales_temp")

# COMMAND ----------

spark.sql("""
SELECT
    month_name,
    SUM(revenue) AS revenue
FROM amazon_sales_temp
GROUP BY month_name
ORDER BY revenue DESC
""").show()

# COMMAND ----------

display(spark_df.limit(20))

# COMMAND ----------

# Remove unwanted index column if it exists

if "index" in spark_df.columns:
    spark_df = spark_df.drop("index")

print("Index column removed.")

# COMMAND ----------

spark.sql("""

CREATE DATABASE IF NOT EXISTS metricmind

""")

print("Database Created Successfully")

# COMMAND ----------

spark.sql("""

USE metricmind

""")

print("Using MetricMind Database")

# COMMAND ----------

spark_df.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("amazon_sales")

print("amazon_sales Delta Table Created")

# COMMAND ----------

spark.sql("""

SELECT *

FROM amazon_sales

LIMIT 10

""").show()

# COMMAND ----------

spark.sql("""

SELECT

COUNT(*) Total_Records

FROM amazon_sales

""").show()

# COMMAND ----------

sales_fact = spark_df.select(

"order_id",

"date",

"sku",

"qty",

"amount",

"revenue",

"status",

"courier_status",

"fulfilment",

"category",

"region"

)

# COMMAND ----------

sales_fact.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("sales_fact")

print("Sales Fact Created")

# COMMAND ----------

spark.sql("""

SELECT *

FROM sales_fact

LIMIT 10

""").show()

# COMMAND ----------

date_dim = spark_df.select(

"date",

"year",

"month",

"quarter",

"week",

"day",

"day_name",

"is_weekend"

).dropDuplicates()

# COMMAND ----------

date_dim.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("date_dim")

print("Date Dimension Created")

# COMMAND ----------

spark.sql("""

SELECT *

FROM date_dim

LIMIT 10

""").show()

# COMMAND ----------

product_dim = spark_df.select(

"sku",

"category",

"style",

"size",

"asin",

"top_category"

).dropDuplicates()

# COMMAND ----------

product_dim.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("product_dim")

print("Product Dimension Created")

# COMMAND ----------

location_dim = spark_df.select(

"ship_city",

"ship_state",

"ship_postal_code",

"ship_country",

"region"

).dropDuplicates()

# COMMAND ----------

location_dim.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("location_dim")

print("Location Dimension Created")

# COMMAND ----------

customer_dim = spark_df.select(

"b2b",

"sales_channel",

"ship_country"

).dropDuplicates()

# COMMAND ----------

customer_dim.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable("customer_dim")

print("Customer Dimension Created")

# COMMAND ----------

spark.sql("""

SHOW TABLES

""").show(truncate=False)

# COMMAND ----------

tables = [

"amazon_sales",

"sales_fact",

"date_dim",

"product_dim",

"location_dim",

"customer_dim"

]

for table in tables:

    print("="*40)

    print(table)

    spark.sql(

        f"SELECT COUNT(*) AS total_rows FROM {table}"

    ).show()

# COMMAND ----------

spark.sql("""

SELECT

region,

SUM(revenue) Revenue

FROM sales_fact

GROUP BY region

ORDER BY Revenue DESC

""").show()

# COMMAND ----------

spark.sql("""

SELECT

category,

SUM(revenue) Revenue

FROM sales_fact

GROUP BY category

ORDER BY Revenue DESC

""").show()

# COMMAND ----------

spark.sql("""

SELECT

sku,

SUM(qty) Total_Qty

FROM sales_fact

GROUP BY sku

ORDER BY Total_Qty DESC

LIMIT 10

""").show()

# COMMAND ----------

spark.sql("""

SELECT

status,

COUNT(*) Orders

FROM sales_fact

GROUP BY status

ORDER BY Orders DESC

""").show()

# COMMAND ----------

print("="*30)

print("Schema Validation")

print("="*30)

sales_fact.printSchema()

date_dim.printSchema()

product_dim.printSchema()

location_dim.printSchema()

customer_dim.printSchema()

# COMMAND ----------

print("="*20)

print("Notebook 04 - Delta Lakehouse Completed Successfully")

print("="*20)

print("Tables Created")

print("✔ amazon_sales")

print("✔ sales_fact")

print("✔ date_dim")

print("✔ product_dim")

print("✔ location_dim")

print("✔ customer_dim")

print("="*20)