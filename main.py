from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schema import chatbot
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from redis_test import load_chat_from_redis, save_chat_to_redis, clear_chat_from_redis
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://swelpaylar.vercel.app", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def parse_chat_history(raw_history):
    parsed = []
    for msg in raw_history:
        msg_type = msg.type
        content = msg.content

        if msg_type == "HumanMessage":
            parsed.append(HumanMessage(content=content))
        elif msg_type == "AIMessage":
            parsed.append(AIMessage(content=content))
        else:
            raise ValueError(f"Unknown message type: {msg_type}")
    return parsed

class ChatRequest(BaseModel):
    text: str
    user_id: str
    chat_history: List[BaseMessage]

@app.get("/")
def home():
    return {"message": "API is runing."}

@app.post("/generate")
def generate_chat(request: ChatRequest):
    text = request.text
    user_id = request.user_id
    chat_history = parse_chat_history(request.chat_history)

    result = chatbot.invoke({'question': text, 'chat_history': chat_history})
    print(result)

    if result:
        chat_history.append(HumanMessage(content=text))
        chat_history.append(AIMessage(content=result['response']['answer']))
        save_chat_to_redis(chat_history, user_id)
        print("Done")

    return {
        "input_text": text,
        "response_text": result['response']['answer']
    }

#uvicorn main:app --host 0.0.0.0 --port 8000 --reload