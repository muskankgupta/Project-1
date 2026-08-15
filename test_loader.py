from semantics.loader import DataLoader

loader = DataLoader()

columns, rows = loader.execute("SELECT 1 AS test")

print("Columns:", columns)
print("Rows:", rows)