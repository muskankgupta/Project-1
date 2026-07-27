# Databricks notebook source
import os
import numpy as np
import pandas as pd

print("MetricMind - Business Data Transformation")


# COMMAND ----------

project_path = "/Workspace/Users/bhilareomkar2006@gmail.com/MetricMind"

clean_path = os.path.join(project_path,"clean_data")

transform_path = os.path.join(project_path,"transformed_data")

report_path = os.path.join(project_path,"reports")

os.makedirs(transform_path,exist_ok=True)

# COMMAND ----------

df = pd.read_csv(os.path.join(clean_path,
"Amazon Sale Report Clean.csv"),

    low_memory=False

)

print(df.shape)

# COMMAND ----------

df["Date"] = pd.to_datetime(df["Date"])

# COMMAND ----------

df["Year"] = df["Date"].dt.year

# COMMAND ----------

df["Month"] = df["Date"].dt.month

# COMMAND ----------

df["Quarter"] = df["Date"].dt.quarter

# COMMAND ----------

df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)

# COMMAND ----------

df["Week"] = df["Date"].dt.isocalendar().week

# COMMAND ----------

df["Day"] = df["Date"].dt.day

# COMMAND ----------

df["Day_Name"] = df["Date"].dt.day_name()

# COMMAND ----------

df["Is_Weekend"] = np.where(

    df["Day_Name"].isin(

        ["Saturday","Sunday"]

    ),

    "Yes",

    "No"

)

# COMMAND ----------

df["Revenue"] = df["Amount"]

# COMMAND ----------

df["Sales_Bucket"] = pd.cut(

    df["Revenue"],

    bins=[ 0,

        500,

        1000,

        5000,

        np.inf

    ],

    labels=[

        "Low",

        "Medium",

        "High",

        "Very High"

    ]

)

# COMMAND ----------

df["Qty_Bucket"] = pd.cut(

    df["Qty"],

    bins=[

        0,

        2,

        5,

        10,

        np.inf

    ],

    labels=[

        "Small",

        "Medium",

        "Large",

        "Bulk"

    ]

)

# COMMAND ----------

df["Status"] = df["Status"].str.title()

# COMMAND ----------

df["Fulfilment"] = df["Fulfilment"].str.title()

# COMMAND ----------

df["Courier Status"] = (

    df["Courier Status"]

    .fillna("Unknown")

    .str.title()

)

# COMMAND ----------

region = {

"Maharashtra":"West",

"Gujarat":"West",

"Goa":"West",

"Delhi":"North",

"Haryana":"North",

"Punjab":"North",

"Rajasthan":"North",

"Uttar Pradesh":"North",

"Bihar":"East",

"Jharkhand":"East",

"West Bengal":"East",

"Odisha":"East",

"Tamil Nadu":"South",

"Karnataka":"South",

"Kerala":"South",

"Andhra Pradesh":"South",

"Telangana":"South"

}

# COMMAND ----------

df["Region"] = df["ship-state"].map(region)

df["Region"] = df["Region"].fillna("Other")

# COMMAND ----------

df["Average_Order_Value"] = (

    df["Revenue"] /

    df["Qty"]

)

# COMMAND ----------

df["Average_Order_Value"] = np.where(

    df["Qty"]==0,

    0,

    df["Revenue"]/df["Qty"]

)

# COMMAND ----------

df["Order_Size"] = np.where(

    df["Qty"]>=5,

    "Bulk",

    "Regular"

)

# COMMAND ----------

top_categories = (

    df["Category"]

    .value_counts()

    .head(5)

    .index

)

df["Top_Category"] = np.where(

    df["Category"].isin(top_categories),

    df["Category"],

    "Others"

)

# COMMAND ----------

print(df.head())

# COMMAND ----------

output = os.path.join(

    transform_path,

    "Amazon Sale Report Transformed.csv"

)

df.to_csv(

    output,

    index=False

)

print("Dataset Saved Successfully")

# COMMAND ----------

print("="*60)

print("Transformation Completed")

print("="*60)

print("Rows :",len(df))

print("Columns :",len(df.columns))

print(df.dtypes)

print("="*60)