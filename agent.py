from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
import tools as t

llm=ChatOpenAI(temperature = 0)
tools = [
    Tool (
        name = "Metric Defination",
        func = t. get_metric,
        description ="Returns formula for business computation"
    ),
    Tool (
         name = "Fetch Data",
        func = t.sample_data,
        description ="Returns business data"
    )
]

agent = initialize_agent(
    tools , llm , agent = "zero - shot -react- description", verboss = True
)
def run_agent(query):
    return agent.run(query)