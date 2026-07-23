# Databricks notebook source
import os
import warnings
import pandas as pd
import numpy as np

# COMMAND ----------

project_path = "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind"

raw_data_path = os.path.join(project_path, "raw_data")
clean_data_path = os.path.join(project_path, "clean_data")
report_path = os.path.join(project_path, "reports")

os.makedirs(clean_data_path, exist_ok=True)
os.makedirs(report_path, exist_ok=True)

print("Folders Verified Successfully")

# COMMAND ----------

print("\nLoading Raw Dataset...")

file_path = os.path.join(
    raw_data_path,
    "Amazon Sale Report.csv"
)

df = pd.read_csv(
    file_path,
    low_memory=False
)

print("Dataset Loaded Successfully")

# COMMAND ----------

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

# COMMAND ----------

duplicate_count = df.duplicated().sum()

print("="*50)
print("Duplicate Records")
print("="*50)

print("Total Duplicate Records :", duplicate_count)

# COMMAND ----------

duplicates = df[df.duplicated()]

duplicates.to_csv(
    os.path.join(
        report_path,
        "duplicate_records.csv"
    ),
    index=False
)

print("Duplicate Report Saved")

# COMMAND ----------

before = len(df)

df = df.drop_duplicates()

after = len(df)

print("Records Before :", before)
print("Records After  :", after)
print("Duplicates Removed :", before-after)

# COMMAND ----------

missing_df = (
    df.isnull()
      .sum()
      .reset_index(name="Missing Values")
      .rename(columns={"index": "Column"})
)

missing_df["Percentage"] = (
    missing_df["Missing Values"] / len(df) * 100
).round(2)

missing_df = missing_df.sort_values(
    by="Missing Values",
    ascending=False
)

display(missing_df)

# COMMAND ----------

missing_df.to_csv(

    os.path.join(

        report_path,

        "missing_values_report.csv"

    ),

    index=False

)

print("Missing Value Report Saved")

# COMMAND ----------

text_columns = df.select_dtypes(include="object").columns

for column in text_columns:

    df[column] = df[column].fillna("Unknown")

print("Text Missing Values Filled")

# COMMAND ----------

numeric_columns = df.select_dtypes(include=np.number).columns

for column in numeric_columns:

    median = df[column].median()

    df[column] = df[column].fillna(median)

print("Numeric Missing Values Filled")

# COMMAND ----------

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m-%d-%y",
    errors="coerce"
)

print("Date Converted Successfully")

# COMMAND ----------

df["Qty"] = pd.to_numeric(
    df["Qty"],
    errors="coerce"
)

df["Qty"] = (
    df["Qty"]
    .fillna(0)
    .astype(int)
)

# COMMAND ----------

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)

df["Amount"] = df["Amount"].fillna(0)

# COMMAND ----------

text_columns = df.select_dtypes(
    include="object"
).columns

for col in text_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.title()
    )

# COMMAND ----------


df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print(df.head())

# COMMAND ----------

if "ship-state" in df.columns:

    df["ship-state"] = (
        df["ship-state"]
        .str.replace("&","And")
        .str.title()
        .str.strip()
    )

# COMMAND ----------

if "Category" in df.columns:

    df["Category"] = (
        df["Category"]
        .str.strip()
        .str.title()
    )

# COMMAND ----------

print("="*60)

print("Remaining Missing Values")
print(df.isnull().sum().sum())

print("\nRemaining Duplicate Records")
print(df.duplicated().sum())

print("\nShape")
print(df.shape)

print("="*60)

# COMMAND ----------

clean_file = os.path.join(
    "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind/clean_data",
    "Amazon Sale Report Clean.csv"
)

df.to_csv(
    clean_file,
    index=False
)

print("Clean Dataset Saved Successfully")

# COMMAND ----------

print("="*70)

print("Notebook Completed Successfully")

print("="*70)

print("Input Records :", before)

print("Output Records :", len(df))

print("Columns :", len(df.columns))

print("Missing Values :", df.isnull().sum().sum())

print("Duplicates :", df.duplicated().sum())

print("="*70)