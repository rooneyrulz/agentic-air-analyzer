import os
from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import BaseTool
from langchain.callbacks.base import BaseCallbackHandler

from tools.analysis_tool import DataAnalysisTool

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

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

        **IMPORTANT: When using the data_analysis_tool, you MUST provide input in EXACTLY this format:**
        {{"input": "<ACTUAL_JSON_PARAMETERS>"}}

        Where <ACTUAL_JSON_PARAMETERS> is a string containing:
        {{
            "operation": "analyze|load|chart",
            "rooms": ["room_a", "room_b", "room_c"] or "all",
            "metrics": ["temperature", "co2", "humidity"],
            "group_by": "hour|day|week|room",
            "filter": {{"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}},
            "chart_type": "line|bar|scatter|heatmap"
        }}

        **Correct Examples:**
        1. For hourly analysis:
        {{"input": "{{\\"operation\\":\\"analyze\\",\\"rooms\\":\\"all\\",\\"metrics\\":[\\"co2\\"],\\"group_by\\":\\"hour\\"}}"}}

        2. For room comparison:
        {{"input": "{{\\"operation\\":\\"analyze\\",\\"rooms\\":[\\"room_a\\",\\"room_b\\"],\\"metrics\\":[\\"temperature\\",\\"humidity\\"],\\"group_by\\":\\"room\\"}}"}}

        **Response Guidelines:**
        - Always return a clear summary
        - Use Markdown tables for data
        - Include statistics (averages, ranges)
        - Suggest visualization types
        - Explain patterns in natural language
        """
    ),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_tool_calling_agent(llm, tools, prompt)
# agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)