import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = getpass.getpass("LangSmith Project: ")
os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("LangSmith API Key: ")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key: ")

model = ChatOpenAI(model="gpt-4")

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]
model.invoke(messages)
