# config/config.py

# Base volume path (Databricks Unity Catalog)
BASE_PATH = "/Volumes/workspace/default/metricmind"

# Bronze Layer
BRONZE_PATH = f"{BASE_PATH}/bronze/amazon_sales_raw"

# Silver Layer
SILVER_PATH = f"{BASE_PATH}/silver/amazon_sales_clean"

# Gold Layer
GOLD_TOTAL_REVENUE_PATH = f"{BASE_PATH}/gold/total_revenue"
GOLD_SALES_BY_CATEGORY_PATH = f"{BASE_PATH}/gold/sales_by_category"