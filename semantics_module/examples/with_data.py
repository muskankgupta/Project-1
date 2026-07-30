"""
examples/with_data.py
======================
Shows how data_agent.py would use load_dataset() to get a cleaned dataframe,
then answer a business question using the business rules from the schema.

Requires: pip install pandas --break-system-packages
Run with: python3 examples/with_data.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantics import load_dataset, BUSINESS_RULES

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "amazon_sale_report.csv")

if __name__ == "__main__":
    df = load_dataset(CSV_PATH)
    print(f"Loaded {len(df)} rows, {df['Order ID'].nunique()} distinct orders.")

    print("\nRule applied -- revenue_definition:")
    print(" ", BUSINESS_RULES["revenue_definition"])
    revenue = df.loc[~df["is_cancelled"], "Amount"].sum()
    print(f"  -> Total revenue (excl. cancelled): {revenue:,.0f}")

    print("\nRule applied -- state_field_quality:")
    print(" ", BUSINESS_RULES["state_field_quality"])
    top_states = (
        df.dropna(subset=["ship-state_clean"])
        .groupby("ship-state_clean")["Order ID"]
        .nunique()
        .sort_values(ascending=False)
        .head(5)
    )
    print("  Top 5 states by distinct orders:")
    print(top_states.to_string())
