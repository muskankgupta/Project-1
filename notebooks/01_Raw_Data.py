# Databricks notebook source
import os
import pandas as pd

# COMMAND ----------

import pandas as pd

print("Loading Amazon Sales Dataset...")

df = pd.read_csv(
    "/Volumes/workspace/default/amazon_sale_reports/Amazon Sale Report.csv"
)

print("Dataset Loaded Successfully!")

df.to_csv(
    "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind/raw_data/Amazon Sale Report.csv",
    index=False
)

print("File copied to MetricMind/raw_data successfully!")

# COMMAND ----------

print(df)

# COMMAND ----------

print("\nLast 10 Rows\n")
print(df.tail(10))

# COMMAND ----------


rows, columns = df.shape

print("\nDataset Shape")
print("----------------")
print("Rows :", rows)
print("Columns :", columns)

# COMMAND ----------

print("\nColumn Names")
print("----------------")

for column in df.columns:
    print(column)

# COMMAND ----------

print("\nData Types")
print("----------------")

print(df.dtypes)

# COMMAND ----------

print("\nMissing Values")
print("----------------")

print(df.isnull().sum())

# COMMAND ----------

duplicates = df.duplicated().sum()

print("\nDuplicate Rows")
print("----------------")

print(duplicates)

# COMMAND ----------

print("\nSummary Statistics")
print("----------------")

print(df.describe(include="all"))

# COMMAND ----------

REPORTS_PATH = "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind/reports"

# Create reports folder if it does not exist
os.makedirs(REPORTS_PATH, exist_ok=True)

summary_file = os.path.join(REPORTS_PATH, "data_summary.txt")

with open(summary_file, "w") as file:

    file.write("MetricMind Data Summary\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Rows : {rows}\n")
    file.write(f"Columns : {columns}\n\n")

    file.write("Column Names\n")
    file.write("-" * 50 + "\n")

    for column in df.columns:
        file.write(column + "\n")

    file.write("\n\nData Types\n")
    file.write("-" * 50 + "\n")
    file.write(str(df.dtypes))

    file.write("\n\nMissing Values\n")
    file.write("-" * 50 + "\n")
    file.write(str(df.isnull().sum()))

    file.write("\n\nDuplicate Rows\n")
    file.write("-" * 50 + "\n")
    file.write(str(duplicates))

print("\nData Summary Report Created Successfully.")

# COMMAND ----------

log_file = os.path.join(REPORTS_PATH, "project_log.txt")

with open(log_file, "w") as file:

    file.write("MetricMind Project Log\n")
    file.write("=" * 50 + "\n\n")

    file.write("Step 1 : Dataset Loaded Successfully\n")
    file.write("Step 2 : Dataset Inspected\n")
    file.write("Step 3 : Summary Report Generated\n")

print("Project Log Created Successfully.")

# COMMAND ----------

print("\n" + "=" * 50)
print("Raw Data Loading Completed Successfully")
print("=" * 50)

# COMMAND ----------

