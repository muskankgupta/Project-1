# import pymysql
# import os

# # Database connection
# conn = pymysql.connect(
#     host="127.0.0.1",
#     user="root",
#     password="1234",
#     database="sys",
#     local_infile=True
# )

# cursor = conn.cursor()

# print("Database connected successfully!")

# # CSV file path
# csv_path = r"D:\Axlero\Project-1\project\AmazonSale.csv"

# # Check file exists
# if not os.path.exists(csv_path):
#     print("CSV file not found:", csv_path)
#     exit()

# print("CSV file found!")

# # Convert Windows path for MySQL
# csv_path = csv_path.replace("\\", "/")

# # Load CSV into MySQL table
# query = f"""
# LOAD DATA LOCAL INFILE '{csv_path}'
# INTO TABLE amazon_sales
# FIELDS TERMINATED BY ','
# ENCLOSED BY '"'
# LINES TERMINATED BY '\\n'
# IGNORE 1 ROWS
# """

# try:
#     cursor.execute(query)
#     conn.commit()

#     print("CSV imported successfully!")

# except Exception as e:
#     print("Error loading CSV:", e)

# # Check inserted rows
# cursor.execute("SELECT COUNT(*) FROM amazon_sales")

# count = cursor.fetchone()[0]

# print("Total rows inserted:", count)


# # Close connection
# cursor.close()
# conn.close()

# print("Connection closed!")

import os
from config import get_connection


def load_csv():

    csv_path = r"D:\Axlero\Project-1\project\AmazonSale.csv"

    if not os.path.exists(csv_path):
        return "CSV file not found"


    csv_path = csv_path.replace("\\", "/")


    conn = get_connection()

    cursor = conn.cursor()


    query = f"""
    LOAD DATA LOCAL INFILE '{csv_path}'
    INTO TABLE amazon_sales
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\\n'
    IGNORE 1 ROWS
    """


    cursor.execute(query)

    conn.commit()


    cursor.close()
    conn.close()


    return "CSV loaded successfully"