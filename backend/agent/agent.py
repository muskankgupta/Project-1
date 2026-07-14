import sqlite3
from semantic import calculate_margin

def query_data(region):
    conn = sqlite3.connect(r"backend\data\company.db")
    cursor = conn.cursor()

    cursor.execute("SELECT revenue, cost FROM sales WHERE region=?", (region,))
    rows = cursor.fetchall()

    conn.close()
    return rows

def analyze_margin(region):
    data = query_data(region)

    margins = []
    for revenue, cost in data:
        margins.append(calculate_margin(revenue, cost))

    avg_margin = sum(margins) / len(margins) if margins else 0

    return avg_margin

def handle_query(user_input):
    if "margin" in user_input.lower() and "europe" in user_input.lower():
        result = analyze_margin("Europe")
        return f"Average European margin is {result:.2f}"

    return "Sorry, I don't understand yet."

if __name__ == "__main__":
    question = input("Ask: ")
    answer = handle_query(question)
    print(answer)