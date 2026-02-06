from .langgraph_python import workflow
from pydantic import BaseModel
from langchain_core.messages import HumanMessage,AIMessage
from fastapi import FastAPI
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserReply(BaseModel):
    message:str
    thread_id:str|None=None
class llmResponse(BaseModel):
    thread_id:str 
    reply:str

#my name is ansh
#hey
@app.post("/send",response_model=llmResponse)   #response_model is in built and is used to check whether the output coming is of schema llmresponse or not
def response(req:UserReply):
    thread_id=req.thread_id or str(uuid4())
    result=workflow.invoke({"messages":[HumanMessage(req.message)]},config={"configurable":{"thread_id":thread_id}})

    reply=result['messages'][-1].content

    return{
        "reply":reply,
        "thread_id":thread_id
    }
