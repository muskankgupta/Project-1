
# from semantics import load_dataset
# from parser_agent import ParserAgent
# from data_agent import DataAgent
# from reasoning_agent import ReasoningAgent


# class Orchestrator:

#     def __init__(self, csv_path):

#         print("Loading dataset...")
#         self.df = load_dataset(csv_path)

#         self.parser = ParserAgent()
#         self.data_agent = DataAgent(self.df)
#         self.reasoning = ReasoningAgent()

#     def run(self, query: str):

#         print(f"\nUser Query: {query}")

#         # 1. Parse
#         plan = self.parser.parse(query)
#         print("Query Plan:", plan)

#         # 2. Execute
#         results = self.data_agent.run(plan)

#         # 3. Reason
#         answer = self.reasoning.generate(query, results)

#         return answer


# if __name__ == "__main__":

#     csv_path = "AmazonSale.csv"   # 🔥 change path

#     orchestrator = Orchestrator(csv_path)

#     while True:
#         q = input("\nAsk a question: ")

#         if q.lower() in ["exit", "quit"]:
#             break

#         output = orchestrator.run(q)

#         print("\nAnswer:")
#         print(output)
"""
orchestrator.py

Main controller for the Agentic BI System.
"""

from query_rewrite_agent import QueryRewriteAgent
from parser_agent import ParserAgent
from validation_agent import ValidationAgent
from time_intelligence_agent import TimeIntelligenceAgent
from sql_agent import SQLGenerationAgent
from data_agent import DataAgent
from reasoning_agent import ReasoningAgent
from insight_agent import InsightAgent
from chart_agent import ChartAgent
from explaination_agent import ExplanationAgent


class Orchestrator:

    def __init__(self):

        print("=" * 60)
        print("Initializing Agentic Orchestrator...")
        print("=" * 60)

        self.rewriter = QueryRewriteAgent()
        self.parser = ParserAgent()
        self.validator = ValidationAgent()
        self.time_agent = TimeIntelligenceAgent()
        self.sql_agent = SQLGenerationAgent()
        self.data_agent = DataAgent()
        self.reasoning = ReasoningAgent()
        self.insight = InsightAgent()
        self.chart = ChartAgent()
        self.explainer = ExplanationAgent()

        print("Initialization complete.")

    def run(self, query: str):

        print("\n" + "=" * 60)
        print("USER QUERY")
        print("=" * 60)
        print(query)

        # ---------------------------------------
        # Step 1 : Rewrite Query
        # ---------------------------------------

        print("\nRewriting query...")

        rewritten_query = self.rewriter.rewrite(query)

        print(rewritten_query)

        # ---------------------------------------
        # Step 2 : Parse
        # ---------------------------------------

        print("\nParsing query...")

        plan = self.parser.parse(rewritten_query)

        print(plan)

        # ---------------------------------------
        # Step 3 : Validate
        # ---------------------------------------

        print("\nValidating query...")

        plan = self.validator.validate(plan)

        print(plan)

        # ---------------------------------------
        # Step 4 : Time Intelligence
        # ---------------------------------------

        print("\nApplying time intelligence...")

        plan = self.time_agent.enhance(rewritten_query, plan)

        print(plan)

        # ---------------------------------------
        # Step 5 : Generate SQL
        # ---------------------------------------

        print("\nGenerating SQL...")

        sql = self.sql_agent.generate(plan)

        print(sql)

        # ---------------------------------------
        # Step 6 : Execute SQL
        # ---------------------------------------

        print("\nExecuting SQL...")

        result = self.data_agent.run(sql)

        # ---------------------------------------
        # Step 7 : Natural Language Answer
        # ---------------------------------------

        print("\nGenerating answer...")

        answer = self.reasoning.generate(
            rewritten_query,
            result
        )

        # ---------------------------------------
        # Step 8 : Insights
        # ---------------------------------------

        insights = self.insight.generate(
            rewritten_query,
            result
        )

        # ---------------------------------------
        # Step 9 : Chart Recommendation
        # ---------------------------------------

        chart = self.chart.suggest(
            rewritten_query,
            result
        )

        # ---------------------------------------
        # Step 10 : Explanation
        # ---------------------------------------

        explanation = self.explainer.generate(
            rewritten_query,
            result
        )

        # ---------------------------------------
        # Final Output
        # ---------------------------------------

        output = []

        output.append("=" * 60)
        output.append("ANSWER")
        output.append("=" * 60)
        output.append(answer)

        if insights:

            output.append("\nBUSINESS INSIGHTS")

            for item in insights:
                output.append(f"• {item}")

        if chart:

            output.append("\nRECOMMENDED VISUAL")
            output.append(chart)

        if explanation:

            output.append("\nEXPLANATION")
            output.append(explanation)

        return "\n".join(output)


def main():

    orchestrator = Orchestrator()

    print("\nAgentic Orchestrator Ready!")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:

        query = input("Ask a question: ").strip()

        if query.lower() in ("exit", "quit"):

            print("\nGoodbye!")
            break

        try:

            response = orchestrator.run(query)

            print()
            print(response)

        except Exception as e:

            print("\nERROR")
            print(e)


if __name__ == "__main__":
    main()