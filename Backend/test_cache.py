import requests
import json
from datetime import datetime, timedelta

# Base URL for the FastAPI application
BASE_URL = "http://127.0.0.1:8000"

# User ID for testing
USER_ID = "user123"

# Function to create chat entries
def create_chat(user_id, chat_id, created_at, updated_at):
    url = f"{BASE_URL}/create_chat/"
    headers = {"Content-Type": "application/json"}
    payload = {
        "user_id": user_id,
        "chat": {
            "chat_id": chat_id,
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat(),
            "messages": []
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Function to update cache with recent chats
def update_cache(user_id, chats):
    url = f"{BASE_URL}/cache/recent_chats/{user_id}"
    headers = {"Content-Type": "application/json"}
    payload = chats
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Function to fetch recent chats from cache
def fetch_recent_chats(user_id):
    url = f"{BASE_URL}/cache/recent_chats/{user_id}"
    response = requests.get(url)
    return response.json()

# Create 25 different chat entries
print("Creating chat entries...")
chats = []
current_time = datetime.utcnow()
for i in range(50):
    chat_id = f"chat{i+1}"
    created_at = current_time - timedelta(days=5*i) 
    updated_at = created_at + timedelta(minutes=5)
    response = create_chat(USER_ID, chat_id, created_at, updated_at)
    print(f"Created chat {chat_id}: {response}")
    chats.append({
        "chat_id": chat_id,
        "chat_topic": "New Chat",
        "created_at": created_at.isoformat(),
        "updated_at": updated_at.isoformat(),
        "messages": []
    })

# # Update cache with recent chats
# print("\nUpdating cache with recent chats...")
# update_response = update_cache(USER_ID, chats)
# print(f"Cache update response: {update_response}")

# # Fetch recent chats from cache
# print("\nFetching recent chats from cache...")
# fetch_response = fetch_recent_chats(USER_ID)
# print(f"Fetched chats: {json.dumps(fetch_response, indent=2)}")
