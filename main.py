from orchestrator import Orchestrator_Agent
orch = Orchestrator_Agent()
while True:
    query = input("Enter your query (or type 'exit' to quit): ")
    if query.lower() == 'exit':
        break
    response = orch.run(query)
    print(response)
    