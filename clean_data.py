import pandas as pd
import numpy as np
import os

os.makedirs("data/cleaned", exist_ok=True)
os.makedirs("output", exist_ok=True)

RAW_FILE = "data/raw/Amazon Sale Report.csv"
CLEAN_FILE = "data/cleaned/Amazon Sale Report.csv"

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_csv(RAW_FILE)

print(f"\nOriginal Shape : {df.shape}")

print("\nRemoving Empty Columns...")

df.drop(columns=["Unnamed: 22"], errors="ignore", inplace=True)

print("Removing Duplicate Orders...")

duplicate_count = df.duplicated(subset=["Order ID"]).sum()

df.drop_duplicates(subset=["Order ID"], inplace=True)

missing_order = df["Order ID"].isnull().sum()

df.dropna(subset=["Order ID"], inplace=True)

print("Converting Date...")

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

invalid_dates = df["Date"].isnull().sum()

df.dropna(subset=["Date"], inplace=True)

print("Cleaning Amount...")

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)

df["Amount"] = df["Amount"].fillna(0)

print("Cleaning Quantity...")

df["Qty"] = pd.to_numeric(
    df["Qty"],
    errors="coerce"
)

df["Qty"] = df["Qty"].fillna(0)

df["Qty"] = df["Qty"].astype(int)

negative_qty = (df["Qty"] < 0).sum()
negative_amount = (df["Amount"] < 0).sum()

df = df[df["Qty"] >= 0]
df = df[df["Amount"] >= 0]

print("Cleaning Text Columns...")

text_columns = [

    "Status",
    "Fulfilment",
    "Sales Channel ",
    "ship-service-level",
    "Style",
    "SKU",
    "Category",
    "Size",
    "ASIN",
    "Courier Status",
    "currency",
    "ship-city",
    "ship-state",
    "ship-country",
    "promotion-ids",
    "fulfilled-by"

]

for col in text_columns:

    if col in df.columns:

        df[col] = (

            df[col]

            .fillna("Unknown")

            .astype(str)

            .str.strip()

        )

print("Standardizing Text...")

title_columns = [

    "Status",

    "Category",

    "Courier Status",

    "ship-city",

    "ship-state"

]

for col in title_columns:

    if col in df.columns:

        df[col] = df[col].str.title()

if "ship-country" in df.columns:

    df["ship-country"] = df["ship-country"].replace({

        "IN": "India",

        "In": "India",

        "INDIA": "India"

    })

if "promotion-ids" in df.columns:
    df["promotion-ids"] = df["promotion-ids"].fillna("No Promotion")

if "fulfilled-by" in df.columns:
    df["fulfilled-by"] = df["fulfilled-by"].fillna("Unknown")

if "currency" in df.columns:
    df["currency"] = df["currency"].fillna("INR")

if "ship-postal-code" in df.columns:
    df["ship-postal-code"] = df["ship-postal-code"].fillna(0)

if "B2B" in df.columns:
    df["B2B"] = df["B2B"].fillna(False)

df.reset_index(drop=True, inplace=True)

print("Saving Clean Dataset...")

df.to_csv(
    CLEAN_FILE,
    index=False
)

print("Generating Reports...")

missing = df.isnull().sum()

missing.to_csv(
    "output/missing_values_report.csv"
)

duplicates = df[df.duplicated(subset=["Order ID"])]

duplicates.to_csv(
    "output/duplicate_orders.csv",
    index=False
)

with open("output/data_summary.txt", "w") as f:

    f.write("=" * 50 + "\n")
    f.write("AMAZON SALES DATA CLEANING REPORT\n")
    f.write("=" * 50 + "\n\n")

    f.write(f"Rows : {df.shape[0]}\n")
    f.write(f"Columns : {df.shape[1]}\n\n")

    f.write(f"Duplicate Orders Removed : {duplicate_count}\n")
    f.write(f"Rows with Missing Order ID Removed : {missing_order}\n")
    f.write(f"Invalid Dates Removed : {invalid_dates}\n")
    f.write(f"Negative Quantity Rows : {negative_qty}\n")
    f.write(f"Negative Amount Rows : {negative_amount}\n\n")

    f.write("Missing Values\n")
    f.write("----------------------------\n")
    f.write(str(df.isnull().sum()))

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nFinal Shape :", df.shape)

print("\nFiles Generated")

print("data/cleaned/Amazon Sale Report_Clean.csv")

print("output/missing_values_report.csv")

print("output/duplicate_orders.csv")

print("output/data_summary.txt")