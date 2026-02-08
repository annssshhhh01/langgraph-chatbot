from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import connect
from psycopg_pool import ConnectionPool
import os

load_dotenv()
database_engine=os.getenv("DATABASE_URL")

llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0.3)

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chatbot(ansh:ChatState):
    messages=ansh["messages"]
    result=llm.invoke(messages)
    return {"messages":[AIMessage(result.content)]}

graph=StateGraph(ChatState)
graph.add_node('chatbot',chatbot)
graph.add_edge(START,"chatbot")
graph.add_edge("chatbot",END)

with connect(database_engine, autocommit=True) as conn:
    checkpointer_setup = PostgresSaver(conn)
    checkpointer_setup.setup()

# Now create the pool for runtime
connection_pool = ConnectionPool(conninfo=database_engine)
checkpointer = PostgresSaver(connection_pool)
# Compile the workflow
workflow = graph.compile(checkpointer=checkpointer)