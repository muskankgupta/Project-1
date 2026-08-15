# from semantics.loader import DataLoader

# loader = DataLoader()

# query = """
# SELECT *
# FROM main.analytics.amazon_sales
# LIMIT 5
# """

# columns, rows = loader.execute(query)

# print(columns)

# for row in rows:
#     print(row)
from semantics.loader import DataLoader

loader = DataLoader()

query = """
SELECT *
FROM default.amazon_sales_clean
LIMIT 5
"""

columns, rows = loader.execute(query)

print(columns)

for row in rows:
    print(row)