from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0.3)
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chatbot(ansh:ChatState):

    messages=ansh["messages"]
    result=llm.invoke(messages)
    return {'messages':[AIMessage(result.content)]}
    


graph=StateGraph(ChatState)
checkpointer = InMemorySaver()

graph.add_node('chatbot',chatbot)
graph.add_edge(START,"chatbot")
graph.add_edge("chatbot",END)

workflow=graph.compile(checkpointer=checkpointer)
