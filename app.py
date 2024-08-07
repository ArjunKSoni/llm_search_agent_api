from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from langchain.utilities import SerpAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import ArxivQueryRun
from langchain_community.tools import PubmedQueryRun
from langchain_community.tools import ShellTool
from langchain_community.utilities.requests import RequestsWrapper
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Chat_input(BaseModel):
    input: str


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")


llm = ChatGroq(model="llama3-70b-8192",
            temperature=0.5,
            max_tokens=None,
            timeout=60,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY"),)


search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"),search_engine="google")
youtube = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"), search_engine="youtube")
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
duckduckgo_search = DuckDuckGoSearchRun()
arxiv = ArxivQueryRun()
pubmed = PubmedQueryRun()
requests_tool = RequestsWrapper()

def calculate_bmi(input_string):
    try:
        height_cm, weight_kg = map(float, input_string.split(','))
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return f"The BMI is {bmi:.2f}"
    except ValueError:
        return "Error: Please provide input in the format 'height,weight'."


 

tools = [
    Tool(
        name="BMI Calculator",
        func=calculate_bmi,
        description="Calculates BMI when given height in cm and weight in kg. Input should be two numbers separated by a comma: height,weight"
    ),
    Tool(
        name="Youtube",
        func=youtube.run,
        description="Search YouTube for videos. Input should be a query string."
    ),
    Tool(
        name="Search",
        func=search.run,
        description="Useful for when you need to answer questions youtube links, any usefull links."
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Useful for when you need detailed information on a topic. Use this for historical facts, definitions, or in-depth knowledge on a subject."
    ),
    Tool(
        name="Python REPL",
        func=PythonREPLTool().run,
        description="Useful for when you need to execute Python code, especially for calculations or data processing."
    ),
    Tool(
        name="DuckDuckGo Search",
        func=duckduckgo_search.run,
        description="Useful for searching the internet for current information, used it for google search, past information and dark world or hacking related data. Ip address and other information."
    ),
    Tool(
        name="ArXiv",
        func=arxiv.run,
        description="Useful for searching and retrieving scientific papers from arXiv."
    ),
    Tool(
        name="PubMed",
        func=pubmed.run,
        description="Useful for searching and retrieving biomedical literature from PubMed."
    ),
    Tool(
        name="Requests",
        func=requests_tool.get,
        description="Useful for making HTTP requests to websites and APIs."
    ),
    Tool(
        name="Shell",
        func=ShellTool().run,
        description="Useful for running shell commands. Use with caution!"
    )
]

memory=ConversationBufferWindowMemory(k=20, memory_key="chat_history", return_messages=True)

agent = initialize_agent(tools=tools,
                         llm=llm,
                         memory=memory,
                         max_iterations=3,
                         early_stopping_method="generate",
                         agent="zero-shot-react-description",
                         verbose=True,
                         min_tokens=1000,
                         handle_parsing_errors=True)


@app.post("/search")
async def search(input: Chat_input):
    return agent.run(input.input)
    