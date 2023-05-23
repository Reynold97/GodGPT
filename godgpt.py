from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import ChatOpenAI
from god_agent.prompt import PREFIX, FORMAT_INSTRUCTIONS, SUFFIX
from god_agent.agent_utils import CustomOutputParser, CustomPromptTemplate

from helper.classes import Role, Message
from helper.openai_api import create_message
from helper.twilio_api import send_message
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
from typing import Dict

import asyncio
import os

load_dotenv()

app = FastAPI()

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

template = PREFIX + FORMAT_INSTRUCTIONS + SUFFIX

prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"]
)

output_parser = CustomOutputParser()

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]

agent = LLMSingleActionAgent(
    llm_chain=llm_chain, 
    output_parser=output_parser,
    stop=["\nObservation:"], 
    allowed_tools=tool_names
)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=False)




@app.get("/")
async def home():
    return {"Cheking" : "OK", "godgpt version" : "0.6.0"}


@app.post("/new_message")
async def new_message(input_messages : list[Message]):
    try:
        def run_chat():
            result = create_message(input_messages)
            return Message(role=Role.assistant, content=result)
        
        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, run_chat)
        return await task
    except:
        return Message(role=Role.assistant, content="Sorry, your request could not be processed, please try again.")


@app.post("/agent_message")
async def agent_message(input_messages : list[Message]):
    try:
        def run_agent():
            result = agent_executor.run(input_messages[0].content)
            return Message(role=Role.assistant, content=result)

        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, run_agent)
        return await task

    except Exception as e:
        return Message(role=Role.assistant, content="Sorry, your request could not be processed, please try again.")
    

@app.post("/twilio/new_message", response_class=PlainTextResponse)
async def twiliomessage(request: Request) -> None:
    try:
        form_data: Dict[str, str] = await request.form()
        input_message = form_data.get("Body")
        sender_id = form_data.get("From")

        message = [
        Message(role=Role.user, content=input_message),
        ]

        def run_chat():
            result = create_message(message)
            return result
        
        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, run_chat)
        new_message = await task

        send_message(sender_id, new_message)
    except:
        error_mesage = "Sorry, your request could not be processed, please try again."
        send_message(sender_id, error_mesage)


@app.post("/twilio/agent_message")
async def twilio_agent_message(request: Request) -> None:
    try:
        form_data: Dict[str, str] = await request.form()
        input_message = form_data.get("Body")
        sender_id = form_data.get("From")

        def run_agent():
            result = agent_executor.run(input_message)
            return result
        
        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, run_agent)
        new_message = await task
    
        send_message(sender_id, new_message)
    except:
        error_mesage = "Sorry, your request could not be processed, please try again."
        send_message(sender_id, error_mesage)