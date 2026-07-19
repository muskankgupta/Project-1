# from orchestrator import Orchestrator

# if __name__ == "__main__":
#     orch = Orchestrator()

#     while True:
#         query = input("\nEnter your query (or type 'exit' to quit): ")

#         if query.lower() == "exit":
#             break

#         try:
#             result = orch.run(query)

#             if result is not None:
#                 print(f"\n✅ Answer: {float(result):,.2f}")
#             else:
#                 print("\n⚠️ No data found")

#         except Exception as e:
#             print("\n❌ Error:", e)

from orchestrator import Orchestrator


agent = Orchestrator()


while True:

    user_input = input("Enter query: ")


    if user_input == "exit":
        break


    response = agent.run(user_input)

    print(response)