from data_agent import DataAgent
from paresr_agent import ParserAgent
from state import State
from data import Data
class Orchestrator_Agent:
    def __init__(self):
        self.data_agent = DataAgent(Data)
        self.parser_agent = ParserAgent()
        self.state = State()
    def run(self, user_input):
        #step 1: find the quarter from the user input
        parsed_data = self.parser_agent.run(user_input)
        if "error" in parsed_data:
            return {
                "status": "error",
                "value": "Invalid query"
            }
        metric = parsed_data["metric"]
        self.state.update("metric", metric)
        #step 2: get the data from the data agent
        result = self.data_agent.run(metric)
        self.state.update("result", result)
        return result