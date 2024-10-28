import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langserve import add_routes

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = getpass.getpass("LangSmith Project: ")
os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("LangSmith API Key: ")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key: ")

#Prompt Template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])

#Model
model = ChatOpenAI(model="gpt-4")

#Parser
parser = StrOutputParser()

#Chain
chain = prompt_template | model | StrOutputParser()
print(chain.invoke({"language": "italian", "text": "hi"}))

#App Definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain"
)

add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)


from langserve import RemoteRunnable
remote_chain = RemoteRunnable("http://localhost:8000/chain/")
remote_chain.invoke({"language": "italian", "text": "hi"})
