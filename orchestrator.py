
from parser_agent import ParserAgent
from query_agent import QueryAgent
from data_agent import DataAgent
from response_agent import ResponseAgent
from validation_agent import ValidationAgent
from memory import Memory
from planner_agent import PlannerAgent


class Orchestrator:
    def __init__(self):
        self.parser_agent = ParserAgent()
        self.query_agent = QueryAgent()
        self.data_agent = DataAgent()
        self.response_agent = ResponseAgent()
        self.validation_agent = ValidationAgent()
        self.memory = Memory()
        self.planner_agent = PlannerAgent()

    def run(self, question: str):
        try:
            print(f"\n🧠 Question: {question}")

            if self.planner_agent.requires_planning(question):
                return self._handle_planned_query(question)

            intent = self.parser_agent.parse(question)
            print(f"🧩 Intent: {intent}")

            sql = self.query_agent.generate_query(intent)

            if not isinstance(sql, str):
                return "❌ Failed to generate SQL query."

            print(f"✅ SQL:\n{sql}")

            if not self.validation_agent.validate(sql):
                return "❌ SQL validation failed."


            result = self.data_agent.execute_query(sql)
            print(f"📦 Result: {result}")


            self.memory.store({
                "question": question,
                "intent": intent,
                "sql": sql,
                "result": result
            })


            return self.response_agent.format_response(question, result)

        except Exception as e:
            return f"❌ Error: {str(e)}"


    def _handle_planned_query(self, question):
        print("🧠 Planner Agent Activated...")

        # 1. Decompose query
        steps = self.planner_agent.decompose(question)
        print(f"📌 Plan: {steps}")

        results = []

        for step in steps:
            print(f"\n🔹 Step: {step}")

            # Parse
            intent = self.parser_agent.parse(step)

            # Generate SQL
            sql = self.query_agent.generate_query(intent)

            if not isinstance(sql, str):
                return f"❌ Failed at step: {step}"

            # Validate
            if not self.validation_agent.validate(sql):
                return f"❌ Invalid SQL at step: {step}"

            # Execute
            result = self.data_agent.execute_query(sql)

            # Extract numeric value safely
            value = self._extract_value(result)
            results.append(value)

            # Store each step in memory
            self.memory.add({
                "question": step,
                "intent": intent,
                "sql": sql,
                "result": result
            })

        # 2. Let PlannerAgent combine results
        final_answer = self.planner_agent.combine(question, steps, results)

        return final_answer


    def _extract_value(self, result):
        try:
            if result and result[0][0] is not None:
                return float(result[0][0])
        except:
            pass
        return 0.0