import sqlite3

conn = sqlite3.connect("backend/data/company.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    region TEXT,
    revenue REAL,
    cost REAL
)
""")

cursor.execute("INSERT INTO sales (region, revenue, cost) VALUES ('Europe', 1000, 600)")

conn.commit()
conn.close()

print("DB ready ✅")