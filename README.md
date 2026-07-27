Project Notebooks

Notebook 01 – Raw Data Ingestion

This notebook performs the following:

- Imports the required Python libraries (`pandas`, `os`)
- Loads the raw Amazon Sales CSV dataset
- Creates the MetricMind project folder structure
- Copies the raw dataset into the `raw_data` folder
- Performs initial data exploration
- Displays the dataset shape, column names, and sample records
- Generates a project log for the ingestion process

Output:

- `raw_data/Amazon Sale Report.csv`

---

Notebook 02 – Clean Data

This notebook performs the following:

- Loads the raw dataset from the `raw_data` folder
- Identifies duplicate records
- Removes duplicate rows
- Detects missing values across all columns
- Generates `missing_values_report.csv`
- Generates `duplicate_records.csv`
- Converts the `Date` column to datetime format
- Converts the `Qty` column to integer format
- Converts the `Amount` column to float format
- Standardizes text fields (`State`, `Category`, `Fulfilment`, `Courier Status`, `Sales Channel`, etc.)
- Generates summary statistics
- Creates a project log
- Saves the cleaned dataset to the `clean_data` folder

Output:

- `clean_data/Amazon Sale Report Clean.csv`
- `reports/missing_values_report.csv`
- `reports/duplicate_records.csv`
- `reports/data_summary.txt`
- `reports/project_log.txt`

---

Notebook 03 – Transform Data

This notebook performs the following:

- Loads the cleaned dataset from the `clean_data` folder
- Creates business-ready date attributes:
  - Year
  - Month
  - Quarter
  - Week
  - Day
  - Day Name
  - Weekend Flag
- Creates business metrics:
  - Revenue
  - Average Order Value
  - Order Size
  - Sales Bucket
  - Quantity Bucket
- Maps states into business regions (North, South, East, West, and Central)
- Creates additional analytical columns for business intelligence
- Validates the transformed dataset
- Saves the transformed dataset to the `transformed_data` folder

Output:

- `transformed_data/Amazon Sale Report Transformed.csv`

---

Notebook 04 – Delta Lakehouse

This notebook performs the following:

- Loads the transformed dataset into a Pandas DataFrame
- Converts the Pandas DataFrame to a Spark DataFrame
- Standardizes column names for Spark SQL compatibility
- Creates the `metricmind` database in Databricks
- Writes the Spark DataFrame in Delta format
- Registers the Delta table as `amazon_sales`
- Creates the following analytical tables:
  - `sales_fact`
  - `date_dim`
  - `product_dim`
  - `location_dim`
  - `customer_dim`
- Executes validation queries to verify data integrity
- Prepares the Delta tables

Tables Created:

- `metricmind.amazon_sales`
- `metricmind.sales_fact`
- `metricmind.date_dim`
- `metricmind.product_dim`
- `metricmind.location_dim`
- `metricmind.customer_dim`
