import requests
from datetime import datetime, timedelta, timezone
import sys
import os
import random
import string

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from database import db

# Base URL for the FastAPI application
BASE_URL = "http://127.0.0.1:8000"

# User ID for testing
USER_ID = "user123"


# Function to add messages to a chat
def generate_random_text(length=15):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_doc():
    payload = [
        {
            "id": "doc002",
            "name": "Forecast",
            "type": "pdf",
            "path": "/path/to/forecast.pdf",
            "size": 1024,
            "data": None
        },
        {
            "id": "img002",
            "name": "Weather Icon",
            "type": "png",
            "path": "https://example.com/weather_icon.png",
            "size": 2048,
            "data": None
        }
    ]
    return payload


def get_msg(i):
    msgs = []
    for m in range(20):
        payload = {
            "message_id": f"msg_{i}_{m+1}",
            "user_prompt": generate_random_text(),
            "user_attachments": get_doc(),
            "user_timestamp": get_create_timestamp(m),
            "chatbot_answer": generate_random_text(),
            "chatbot_attachments": get_doc(),
            "chatbot_timestamp": get_update_timestamp(m) + timedelta(minutes=5)
        }
        msgs.append(payload)
    return msgs


# Function to update cache with recent chats
def update_cache(user_id, chats):
    try:
        url = f"{BASE_URL}/cache/recent_chats/{user_id}"
        headers = {"Content-Type": "application/json"}
        payload = chats
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as ex:
        print(f"Error {ex}")


# Function to fetch recent chats from cache
def fetch_recent_chats(user_id):
    try:
        url = f"{BASE_URL}/cache/recent_chats/{user_id}"
        response = requests.get(url)
        return response.json()
    except Exception as ex:
        print(f"Error {ex}")


def get_create_timestamp(i):
    return datetime.now(timezone.utc) - timedelta(days=5*i)


def get_update_timestamp(i):
    return get_create_timestamp(i) + timedelta(minutes=5)


# Create 25 different chat entries
def main():
    try:
        print("Delete if entries already exist...")
        db.chats.delete_many({})
        print("Creating chat entries...")
        for u in range(5):
            payload = {
                "user_id": f"user_{u+1}",
                "chats": get_chats(u+1)
            }
            db.chats.insert_one(payload)
        print("Chat entries created successfully!")
    except Exception as ex:
        print(f"Error {ex}")


# Function to create chat entries
def get_chats(user_id):
    try:
        chats = []
        for i in range(50):
            payload = {
                    "chat_id": f"chat_{user_id}_{i+1}",
                    "chat_topic": f"This is the Chat Topic : {user_id}_{i+1}",
                    "created_at": get_create_timestamp(i),
                    "updated_at": get_update_timestamp(i),
                    "messages": get_msg(i+1)
            }

            chats.append(payload)
        return chats
    except Exception as ex:
        print(f"Error {ex}")


if __name__ == "__main__":
    main()
