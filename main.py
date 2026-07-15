import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# Load env
load_dotenv()

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -----------------------------
# 🧩 Define Tools
# -----------------------------

@tool
def sales_analyzer(query: str) -> str:
    return f"[Sales Tool] Analysis for: {query}"

@tool
def profit_calculator(query: str) -> str:
    return f"[Profit Tool] Calculation for: {query}"

@tool
def summary_generator(query: str) -> str:
    return f"[Summary Tool] Generated summary for: {query}"

tools = [sales_analyzer, profit_calculator, summary_generator]

# -----------------------------
# 🧠 Orchestrator Logic
# -----------------------------

def route_query(query: str):
    query_lower = query.lower()

    if "sales" in query_lower:
        return sales_analyzer.invoke(query)

    elif "profit" in query_lower or "margin" in query_lower:
        return profit_calculator.invoke(query)

    elif "summary" in query_lower or "report" in query_lower:
        return summary_generator.invoke(query)

    else:
        # fallback to LLM
        return llm.invoke(query).content


# -----------------------------
# ▶️ Run
# -----------------------------

if __name__ == "__main__":
    while True:
        q = input("\nEnter your query: ")
        if q.lower() == "exit":
            break

        result = route_query(q)
        print("\nResponse:", result)