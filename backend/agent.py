from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import BaseTool
from langchain.callbacks.base import BaseCallbackHandler

from tools.analysis_tool import DataAnalysisTool

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

tools = [DataAnalysisTool()]

prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        """
        You are an expert air quality data analyst. You help users analyze air quality data from multiple rooms using natural language queries.

        Available data includes:
        - Room A, Room B, Room C data files
        - Metrics: CO2 levels, temperature, humidity, timestamps
        - Note: Column names may vary between files (co2 vs CO2 vs CO2 (PPM))

        Response Format Guidelines:
        1. For tabular data: Always format as a proper table with headers
        2. For trends: Provide both numerical data AND descriptive insights
        3. For comparisons: Use clear comparative language
        4. Include relevant statistics (averages, ranges, etc.)
        5. When appropriate, suggest chart visualizations

        Note: Always provide a summary of the analysis, even if it's just a few sentences.

        Always use the data_analysis_tool to access and analyze the actual data files.

        Example Response Templates:

        For hourly analysis:
        | Hour | Temperature (°C) | CO2 (PPM) |
        |------|------------------|-----------|
        | 00:00| 22.1            | 420       |
        | 01:00| 21.8            | 410       |

        Analysis: "Temperature shows a decreasing trend from midnight to 6 AM, with the lowest reading of 19.2°C at 6 AM."

        For room comparisons:
        | Room | Avg Temperature | Avg CO2 | Humidity Range |
        |------|----------------|---------|----------------|
        | A    | 23.5°C         | 450 PPM | 45-65%         |
        | B    | 22.1°C         | 380 PPM | 40-60%         |

        Analysis: "Room A consistently runs warmer and has higher CO2 levels, suggesting higher occupancy or less ventilation."

        """
    ),
    (
        "user",
        "{input}"
    ),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_tool_calling_agent(llm, tools, prompt)
# agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)