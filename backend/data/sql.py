import pandas as pd
import mysql.connector

# Read Excel
df = pd.read_excel("D:/Axlero/Project-1/amazon.xlsx")

# Convert NaN properly
data = [
    tuple(None if pd.isna(value) else value for value in row)
    for row in df.itertuples(index=False, name=None)
]

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="sys"
)

cursor = conn.cursor()

columns = ", ".join(df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))

query = f"INSERT INTO amazon ({columns}) VALUES ({placeholders})"

cursor.executemany(query, data)
conn.commit()

print("✅ Data inserted successfully!")