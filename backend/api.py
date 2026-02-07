from .langgraph_python import workflow
from pydantic import BaseModel
from langchain_core.messages import HumanMessage,AIMessage
from fastapi import FastAPI
from uuid import uuid4
from fastapi.responses import StreamingResponse
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

@app.post("/stream")
def response(req:UserReply):
    thread_id=req.thread_id or str(uuid4())
#note that AImessage is a class and chunk is an object of that class and content is just a method 
    def chunk_generator(): 
        for chunk,metadata in workflow.stream({"messages":[HumanMessage(content=req.message)]}, config={"configurable":{"thread_id":thread_id}}, stream_mode="messages"): #langraph uses plural so dont mention message or etc  ---when this line hit and the langgraph_python trigger and start happen which make .invoje hit and give output in chatbot and that output containing aimessage is shown 
            if isinstance(chunk,AIMessage) and chunk.content: #---then this line gets printed --- isinstance(obj,class) this is the main syntax
                yield chunk.content
    return StreamingResponse(
        chunk_generator(),  # no need to write body= as the first positional arg is always a body
        media_type="text/plain",
        headers={"thread_id":thread_id}
    )         
