from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Attachment(BaseModel):
    id: str            # Unique identifier for the attachment
    name: str          # Name of the attachment (document or image)
    type: str          # Type of the attachment (e.g., docx, pdf, jpg, png)
    path: str          # Path or URL to the attachment
    size: int          # Size of the file in bytes
    data: bytes        # File data stored as binary data


class Message(BaseModel):
    message_id: str
    user_prompt: str
    user_attachments: Optional[List[Attachment]] = None  # Replaces user_documents and user_images
    user_timestamp: datetime = datetime.now()
    chatbot_answer: str
    chatbot_attachments: Optional[List[Attachment]] = None  # Replaces chatbot_documents and chatbot_images
    chatbot_timestamp: datetime = datetime.now()


class Chat(BaseModel):
    chat_id: str
    chat_topic: str = "New Chat"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    messages: List[Message]


class UserChats(BaseModel):
    user_id: str
    chats: List[Chat]


# TODO : Get All Chats -> Adding Feature to accept date ranges
# Define a model for the input data (user_id, start_date, end_date)
class DateRangeFilter(BaseModel):
    user_id: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
