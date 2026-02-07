import { useState } from "react";
function App(){
const [input,setInput]=useState("")
const [messages,Setmessages]=useState([])
const[Threadid,SetThreadid]=useState(null)
const[loading,setLoading]=useState(false)


async function sendMessage(){
  console.log("SEND BUTTON CLICKED");
if(!input.trim()) return;
try{
  setLoading(true)
const userMessage={role:"user",content:input}
Setmessages((prev)=>[...prev,userMessage])

const response=await fetch("http://127.0.0.1:8000/stream",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({
    message:input,
    thread_id:Threadid
  })
})
if(!response.ok){
 const text=await response.text(); // gives whatever is written in the response after failing
console.error("backend error:",text);
return;
}
console.log("Response status:", response.status);

//creating a variable which will store the threadid of the user (main use case of this is to use the threadid for resume feature)
const newThreadid=response.headers.get("thread_id");
if(newThreadid)
  SetThreadid(newThreadid)
//since the content is coming chunk by chunk so we need a loop so first we will initialize setmessage as ""
const reader=response.body.getReader();
const decoder =new TextDecoder();
let assistantText="";

Setmessages((prev)=>[...prev,{role:"assistant",content:""}])

while (true){
const{done,value}=await reader.read()
if(done) break;
const chunk=decoder.decode(value)
assistantText+=chunk
Setmessages((prev)=>{
 const updated=[...prev];
 updated[updated.length-1]={role:"assistant","content":assistantText}
 return updated;
})
}

setInput("")
}
catch(err){
  console.log("fetched failes",err)
}
finally {
  setLoading(false); // This ensures the message disappears regardless of success or failure
}
 
}
return (
  <div className="chat-container">
    <header className="chat-header">
      <h2>LangGraph Agent</h2>
      <div className="status-dot"></div>
    </header>

    <div className="messages-window">
      {messages.map((m, i) => (
        <div key={i} className={`message-bubble ${m.role === "user" ? "user" : "assistant"}`}>
          <div className="message-info">
            <b>{m.role === "user" ? "You" : "Assistant"}</b>
          </div>
          <div className="message-text">{m.content}</div>
        </div>
      ))}
      {loading && (
        <div className="message-bubble assistant">
          <div className="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      )}
    </div>

    <div className="input-area">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()} // Send on Enter key
        placeholder="Ask something..."
      />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? "..." : "Send"}
      </button>
    </div>
  </div>
);
}
export default App;