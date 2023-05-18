from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from god_agent.prompt import PREFIX, FORMAT_INSTRUCTIONS, SUFFIX
import re
import os

# Define which tools the agent can use to answer user queries
search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="""useful for when you need to answer questions about current events or you need more context to answer the quiestion
        """
    )
]


