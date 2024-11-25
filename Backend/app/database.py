from pymongo import MongoClient
import os

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)  # type:ignore
db = client.chatbot_db

# Ensure indexes for performance
db.chats.create_index([("user_id", 1), ("chats.chat_id", 1)], unique=True)
