from redis_test import load_chat_from_redis
import requests

history = load_chat_from_redis("chat_history:01a0f162-0986-4e17-8559-cfa01df5a2c3")

url = "http://localhost:8000/generate"  # Adjust if hosted elsewhere

# Convert chat history to a JSON-serializable format
chat_history_serializable = [
    {"type": type(m).__name__, "content": m.content}
    for m in history
]

payload = {
    "text": "Hello, Who is Min Thant Kyaw?",
    "user_id": "chat_history:01a0f162-0986-4e17-8559-cfa01df5a2c3",
    "chat_history": chat_history_serializable
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
