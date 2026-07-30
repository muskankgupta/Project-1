
from semantics import load_dataset
from parser_agent import ParserAgent
from data_agent import DataAgent
from reasoning_agent import ReasoningAgent


class Orchestrator:

    def __init__(self, csv_path):

        print("Loading dataset...")
        self.df = load_dataset(csv_path)

        self.parser = ParserAgent()
        self.data_agent = DataAgent(self.df)
        self.reasoning = ReasoningAgent()

    def run(self, query: str):

        print(f"\nUser Query: {query}")

        # 1. Parse
        plan = self.parser.parse(query)
        print("Query Plan:", plan)

        # 2. Execute
        results = self.data_agent.run(plan)

        # 3. Reason
        answer = self.reasoning.generate(query, results)

        return answer


if __name__ == "__main__":

    csv_path = "AmazonSale.csv"   # 🔥 change path

    orchestrator = Orchestrator(csv_path)

    while True:
        q = input("\nAsk a question: ")

        if q.lower() in ["exit", "quit"]:
            break

        output = orchestrator.run(q)

        print("\nAnswer:")
        print(output)