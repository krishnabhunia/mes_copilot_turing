from datetime import datetime
from typing import Optional

error_messages = []
bool_valid_flag: Optional[bool] = None


def validate_user(data: dict):
    global error_messages
    global bool_valid_flag

    # Validate user_id
    if not (len(data["user_id"]) > 0 and len(data["user_id"]) < 50 and data["user_id"].isalnum()):
        set_valid_flag(True, "User not found or invalid user_id")

    # Check if chats key exists and has at least one item
    if "chats" not in data or not isinstance(data["chats"], list) or len(data["chats"]) == 0:
        set_valid_flag(True, "No chats found")
    else:
        bool_valid_flag, error_messages = validate_chat(data["chats"])

    # Return True if chats are valid, but continue adding error messages for other validations
    return (bool_valid_flag, error_messages)


def set_valid_flag(flag, msg):
    global bool_valid_flag
    global error_messages
    bool_valid_flag = flag
    error_messages.append(msg)


def validate_chat(chat_data):
    global error_messages
    global bool_valid_flag

    if not (len(chat_data["chat_id"]) > 0 and chat_data["chat_id"].isalnum()):
        set_valid_flag(True, "Chat not found or invalid chat_id")

    if not isinstance(chat_data["created_at"], datetime):
        set_valid_flag(True, "Invalid or missing created_at")

    if not isinstance(chat_data["updated_at"], datetime):
        set_valid_flag(True, "Invalid or missing updated_at")

    if "messages" not in chat_data or not isinstance(chat_data["messages"], list) or len(chat_data["messages"]) == 0:
        set_valid_flag(True, "No messages found")
    else:
        bool_valid_flag, error_messages = validate_messages(chat_data["messages"])

    # Return True if chats are valid, but continue adding error messages for other validations
    return (bool_valid_flag, error_messages)


def validate_messages(message):
    global error_messages
    global bool_valid_flag

    # Validate message_id
    if not (message.get("message_id") and message["message_id"].isalnum()):
        set_valid_flag(True, "message_id not found or invalid")

    # Validate user_prompt
    if not (message.get("user_prompt") and len(message["user_prompt"]) > 0 and len(message["user_prompt"]) < 5000):
        set_valid_flag(True, "user_prompt not found or invalid")

    # Validate user_timestamp
    if not (isinstance(message.get("user_timestamp"), datetime) or isinstance(message.get("user_timestamp"), str)):
        set_valid_flag(True, "user_timestamp not found or invalid")

    # Validate chatbot_timestamp
    if not isinstance(message.get("chatbot_timestamp"), datetime):
        set_valid_flag(True, "chatbot_timestamp not found or invalid")

    # Validate chatbot_answer
    if not (message.get("chatbot_answer") and message["chatbot_answer"].isalpha()):
        set_valid_flag(True, "chatbot_answer not found or invalid")

    # Check if user_attachments and chatbot_attachments are present
    if "user_attachments" not in message or len(message["user_attachments"]) == 0:
        set_valid_flag(True, "user_attachments not found")
    else:
        bool_valid_flag, error_messages = validate_user_attachments(message["user_attachments"])

    if "chatbot_attachments" not in message or len(message["chatbot_attachments"]) == 0:
        set_valid_flag(True, "chatbot_attachments not found")
    else:
        bool_valid_flag, error_messages = validate_chatbot_attachments(message["chatbot_attachments"])

    return (bool_valid_flag, error_messages)


def validate_user_attachments(user_attachments):
    global error_messages
    global bool_valid_flag

    for user_attachment in user_attachments:
        if not (len(user_attachment["id"]) > 0 and user_attachment["id"].isalnum()):
            set_valid_flag(True, "user_attachments_id not found or invalid")

        if not (user_attachment["name"] != "" and user_attachment["name"].isalnum()):
            set_valid_flag(True, "user_attachments_name not found or invalid")

        if not user_attachment["type"] in ('pdf', 'png', 'docx', 'jpg'):
            set_valid_flag(True, "user_attachments_type not found or invalid")

        if not user_attachment["path"] != "":
            set_valid_flag(True, "user_attachments_path not found or invalid")
    return (bool_valid_flag, error_messages)


def validate_chatbot_attachments(chatbot_attachments):
    global error_messages
    global bool_valid_flag

    for chatbot_attachment in chatbot_attachments:
        if not (len(chatbot_attachment["id"]) > 0 and chatbot_attachment["id"].isalnum()):
            set_valid_flag(True, "chatbot_attachments_id not found or invalid")

        if not (chatbot_attachment["name"] != "" and chatbot_attachment["name"].isalpha()):
            set_valid_flag(True, "chatbot_attachments_name not found or invalid")

        if not chatbot_attachment["type"] in ('pdf', 'png', 'docx', 'jpg'):
            set_valid_flag(True, "chatbot_attachments_type not found or invalid")

        if not chatbot_attachment["path"] != "":
            set_valid_flag(True, "chatbot_attachments_path not found or invalid")

    return (bool_valid_flag, error_messages)
