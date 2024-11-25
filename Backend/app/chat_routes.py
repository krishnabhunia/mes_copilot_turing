from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models import Chat, Message, Attachment
from app.database import db
from datetime import datetime, timedelta
import hashlib
from app.helper.authenticate import authenticate_user
from fastapi.security.api_key import APIKeyHeader
import app.validations as validate
from app.local_logger import Local_Logger

from app.simpleCaching import cache, ignore_milliseconds
from app.models import DateRangeFilter


router = APIRouter()
security = HTTPBasic()
api_key_header = APIKeyHeader(name="API-Key", auto_error=False)

lg = Local_Logger().get_logger()


# CREATE a new chat for a user
@router.post("/create_chat")
async def create_chat(data: dict):
    try:
        user_id = data["user_id"]
        chat_data = Chat(**data["chat"])
        lg.debug(f"Data : {user_id},{chat_data}")

        user = db.chats.find_one({"user_id": user_id})
        lg.info(f"User Found : {user_id}")

        if not user:
            user_data = {
                "user_id": user_id,
                "chats": [chat_data.dict()]
            }
            db.chats.insert_one(user_data)
            lg.info(f"Chat created for new user :{user_id} ")
            return {"status": "Chat created for new user"}

        if any(existing_chat["chat_id"] == chat_data.chat_id for existing_chat in user["chats"]):
            lg.debug(f"Chat ID already exists for this user : {user_id}")
            raise HTTPException(status_code=400, detail="Chat ID already exists for this user")

        db.chats.update_one(
            {"user_id": user_id},
            {"$push": {"chats": chat_data.dict()}}
        )
        lg.info(f"Chat added for existing user : {user_id}")
        return {"status": "Chat added for existing user"}
    except Exception as ex:
        lg.error(f"Function Name : create_chat - HTTPException - {ex} for user id : {user_id}")
        raise


# ADD a new message to an existing chat
@router.put("/add_message")
async def add_message(data: dict):
    try:
         # Start of the request processing
        lg.debug(f"Received data: {data}")  # DEBUG level for raw input data
        # Extracting necessary data from the request
        user_id = data["user_id"]
        chat_id = data["chat_id"]
        message_data = Message(**data["message"])
        # Validation of message data
        # val_res = validate.validate_messages(data["message"])
        # if val_res[0]:
        #     lg.error(f"Validation Error: {val_res[1]} for user_id: {user_id}, chat_id: {chat_id}")
        #     raise HTTPException(status_code=400, detail=f"Validation Error : {val_res[1]}")

        user = db.chats.find_one({"user_id": user_id})
        if not user:
            lg.error(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        chat = next((c for c in user["chats"] if c["chat_id"] == chat_id), None)
        if not chat:
            lg.error(f"Chat not found for user_id: {user_id}, chat_id: {chat_id}")
            raise HTTPException(status_code=404, detail="Chat not found for this user")

        if any(msg["message_id"] == message_data.message_id for msg in chat["messages"]):
            lg.error(f"Message ID {message_data.message_id} already exists in chat {chat_id} for user {user_id}")
            raise HTTPException(status_code=400, detail="Message ID already exists in this chat")

        db.chats.update_one(
            {"user_id": user_id, "chats.chat_id": chat_id},
            {
                "$push": {"chats.$.messages": message_data.dict()},
                "$set": {"chats.$.updated_at": datetime.now()}
            }
        )
        lg.info(f"Message added successfully for user {user_id}, chat_id {chat_id}, message_id {message_data.message_id}")
        return {"status": "Message added to chat"}
    
    except Exception as ex:
        # Log unexpected errors with full stack trace
        lg.error(f"Function Name : add_message - HTTPException - {ex} for user id : {user_id}")
        raise


# GET all messages in a specific chat
@router.get("/get_messages")
async def get_messages(data: dict):
    try:
        # Log received request data at DEBUG level
        lg.debug(f"Received request data: {data}")

        user_id = data["user_id"]
        chat_id = data["chat_id"]
        
        # Query the database for the user and chat
        lg.info(f"Attempting to retrieve messages for user_id: {user_id}, chat_id: {chat_id}")

        user = db.chats.find_one(
            {"user_id": user_id, "chats.chat_id": chat_id},
            {"chats.$": 1, "_id": 0}
        )

        if not user or "chats" not in user or not user["chats"]:
            lg.warning(f"Chat not found for user_id: {user_id}, chat_id: {chat_id}")
            raise HTTPException(status_code=404, detail="Chat not found for this user")

        lg.info(f"Messages retrieved successfully for user_id: {user_id}, chat_id: {chat_id}")
        return user["chats"][0]["messages"]

    except Exception as ex:
        # Log unexpected errors with the exception details
        lg.error(f"Function Name : get_messages - HTTPException - {ex} for user id : {user_id}, chat_id: {chat_id}")
        raise
    

# DELETE a chat
@router.delete("/delete_chat")
async def delete_chat(data: dict):
    try:
        # Log received request data at DEBUG level
        lg.debug(f"Received request data: {data}")

        user_id = data["user_id"]
        chat_id = data["chat_id"]
        
        # Log the attempt to delete the chat
        lg.info(f"Attempting to delete chat with chat_id: {chat_id} for user_id: {user_id}")

        result = db.chats.update_one(
            {"user_id": user_id},
            {"$pull": {"chats": {"chat_id": chat_id}}}
        )

        if result.modified_count == 0:
            lg.warning(f"Chat with chat_id: {chat_id} not found for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="Chat not found for this user")
        
        # Log successful deletion
        lg.info(f"Chat with chat_id: {chat_id} successfully deleted for user_id: {user_id}")
        return {"status": "Chat deleted"}
    
    except Exception as ex:
        # Log unexpected errors with full stack trace
        lg.error(f"Function Name : delete_chat - HTTPException - {ex} for user id : {user_id}, chat_id: {chat_id}")
        raise


# DELETE a specific message in a chat
@router.delete("/delete_message")
async def delete_message(data: dict):
    try:
        # Log received request data at DEBUG level
        lg.debug(f"Received request data: {data}")

        user_id = data["user_id"]
        chat_id = data["chat_id"]
        message_id = data["message_id"]

        # Log the attempt to delete the message
        lg.info(f"Attempting to delete message with message_id: {message_id} in chat with chat_id: {chat_id} for user_id: {user_id}")

        result = db.chats.update_one(
            {"user_id": user_id, "chats.chat_id": chat_id},
            {"$pull": {"chats.$.messages": {"message_id": message_id}}}
        )

        if result.modified_count == 0:
            lg.warning(f"Message with message_id: {message_id} not found in chat {chat_id} for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="Message not found in chat for this user")
        
        lg.info(f"Message with message_id: {message_id} successfully deleted from chat {chat_id} for user_id: {user_id}")
        return {"status": "Message deleted"}
        
    except Exception as ex:
        # Log unexpected errors with full stack trace
        lg.error(f"Function Name : delete_chat - HTTPException - {ex} for user id : {user_id}, chat_id: {chat_id}, user_id: {user_id}")
        raise


# UPDATE an existing message in a chat
@router.put("/update_message")
async def update_message(data: dict):
    try:
        # Log received request data at DEBUG level
        lg.debug(f"Received request data: {data}")

        user_id = data["user_id"]
        chat_id = data["chat_id"]
        message_id = data["message_id"]
        updated_message_data = Message(**data["updated_message"])

        # Log the beginning of the message update process
        lg.info(f"Attempting to update message with message_id: {message_id} in chat with chat_id: {chat_id} for user_id: {user_id}")

        user = db.chats.find_one({"user_id": user_id})
        if not user:
            lg.warning(f"User with user_id: {user_id} not found.")
            raise HTTPException(status_code=404, detail="User not found")

        chat = next((c for c in user["chats"] if c["chat_id"] == chat_id), None)
        if not chat:
            lg.warning(f"Chat with chat_id: {chat_id} not found for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="Chat not found for this user")

        message = next((msg for msg in chat["messages"] if msg["message_id"] == message_id), None)
        if not message:
            lg.warning(f"Message with message_id: {message_id} not found in chat with chat_id: {chat_id} for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="Message not found in chat for this user")

        if any(msg["message_id"] == updated_message_data.message_id for msg in chat["messages"] if msg["message_id"] != message_id):
            lg.warning(f"Duplicate message_id: {updated_message_data.message_id} found in chat with chat_id: {chat_id}.")
            raise HTTPException(status_code=400, detail="Message ID already exists in this chat")

        update_fields = {
            "chats.$[chat].messages.$[msg].message_id": updated_message_data.message_id,
            "chats.$[chat].messages.$[msg].user_prompt": updated_message_data.user_prompt,
            "chats.$[chat].messages.$[msg].chatbot_answer": updated_message_data.chatbot_answer,
            "chats.$[chat].messages.$[msg].user_documents": [doc.dict() for doc in updated_message_data.user_documents] if updated_message_data.user_documents else [],
            "chats.$[chat].messages.$[msg].user_images": [img.dict() for img in updated_message_data.user_images] if updated_message_data.user_images else [],
            "chats.$[chat].messages.$[msg].chatbot_documents": [doc.dict() for doc in updated_message_data.chatbot_documents] if updated_message_data.chatbot_documents else [],
            "chats.$[chat].messages.$[msg].chatbot_images": [img.dict() for img in updated_message_data.chatbot_images] if updated_message_data.chatbot_images else [],
            "chats.$[chat].updated_at": datetime.now()
        }

        result = db.chats.update_one(
            {"user_id": user_id},
            {"$set": update_fields},
            array_filters=[{"chat.chat_id": chat_id}, {"msg.message_id": message_id}]
        )

        if result.matched_count == 0:
            lg.warning(f"Failed to update message with message_id: {message_id} in chat with chat_id: {chat_id} for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="Failed to update message")

        lg.info(f"Message with message_id: {message_id} successfully updated in chat with chat_id: {chat_id} for user_id: {user_id}")
        return {"status": "Message updated successfully"}
    except Exception as ex:
        # Log unexpected errors with full stack trace
        lg.error(f"Function Name : update_message - HTTPException - {ex} for user id : {user_id}, chat_id: {chat_id}, user_id: {user_id}")
        raise


@router.post("/add_user_prompt_and_generate_response")
# async def add_user_prompt_and_generate_response(data: dict, credentials: HTTPBasicCredentials = Depends(security), api_key: str = Depends(api_key_header)):
async def add_user_prompt_and_generate_response(data: dict):
    try:
        lg.debug(f"Received request data: {data}")
        # if not authenticate_user(credentials.username, credentials.password):
        #     raise HTTPException(status_code=401, detail="Unauthorized")
        # Log received request data at DEBUG level

        user_id = data.get("user_id")
        
        chat_id = data.get("chat_id")
        message_id = str(data.get("message_id"))
        user_prompt = str(data.get("user_prompt"))
        user_attachments_data = data.get("user_attachments", [])

        # Log attempt to find user and chat
        lg.info(f"Attempting to process user_prompt for user_id: {user_id}, chat_id: {chat_id}, message_id: {message_id}")

        # val_res = validate.validate_user(data)
        # if val_res[0]:
        #     raise HTTPException(status_code=422, detail=f"Validation Error :{val_res[1]}")

        # if authorization != API_KEY:
        #     raise HTTPException(status_code=401, detail="Unauthorized")
        # return {"message": "Authorized access", "data": "Here is your data!"}

        # Validate user and chat existence
        user = db.chats.find_one({"user_id": user_id})
        if not user:
            lg.warning(f"User with user_id: {user_id} not found.")
            raise HTTPException(status_code=404, detail="User not found")
        chat = next((c for c in user["chats"] if c["chat_id"] == chat_id), None)
        if not chat:
            lg.warning(f"Chat with chat_id: {chat_id} not found for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="Chat not found for this user")

        # Check for duplicate message ID within the chat
        if any(msg["message_id"] == message_id for msg in chat["messages"]):
            lg.warning(f"Message ID {message_id} already exists in chat {chat_id} for user {user_id}.")
            raise HTTPException(status_code=400, detail="Message ID already exists in this chat")

        # Convert user_attachments_data to a list of Attachment objects
        lg.debug(f"Converting user attachments: {user_attachments_data}")
        user_attachments = [Attachment(**attachment) for attachment in user_attachments_data]

        # Generate a dummy chatbot answer and attachments
        chatbot_answer = "The weather tomorrow is expected to be sunny with a high of 25°C."
        chatbot_attachments = [
            Attachment(id="doc002", name="Detailed Weather Forecast", type="pdf", path="/path/to/detailed_forecast.pdf", size=1024, data="ksdhfskdbhfbs87s69".encode('utf-8')),
            Attachment(id="img002", name="Weather Icon", type="png", path="https://example.com/weather_icon.png", size=2048, data="af*^&%*&vjcgGHCHG".encode('utf-8'))
        ]
        chatbot_timestamp = datetime.now()

        # Log the chatbot response being generated
        lg.info(f"Generated chatbot answer: {chatbot_answer}, timestamp: {chatbot_timestamp}")

        # Create a new Message object with user prompt and chatbot response
        new_message = Message(
            message_id=message_id,
            user_prompt=user_prompt,
            user_timestamp=datetime.now(),
            user_attachments=user_attachments,
            chatbot_answer=chatbot_answer,
            chatbot_timestamp=chatbot_timestamp,
            chatbot_attachments=chatbot_attachments
        )

        # Add the new message to the cache
        cache_key = f"{user_id}_{chat_id}"
        cached_chat = cache.get_from_cache(cache_key) or {"messages": []}
        lg.info(f"Adding new message to cache with key: {cache_key}")

        cached_chat["messages"].append(new_message.dict())
        cache.add_to_cache(cache_key, cached_chat)
        lg.info(f"Message added to cache for key: {cache_key}")

        # Construct the response with all fields
        response_data = {
            "status": "User prompt and chatbot response added to chat",
            "message_id": new_message.message_id,
            "user_prompt": new_message.user_prompt,
            "user_timestamp": new_message.user_timestamp,
            "user_attachments": [attachment.dict() for attachment in new_message.user_attachments],
            "chatbot_answer": new_message.chatbot_answer,
            "chatbot_timestamp": new_message.chatbot_timestamp,
            "chatbot_attachments": new_message.chatbot_attachments
        }
         
        # Log the response being returned
        lg.info(f"Returning response for message_id: {new_message.message_id}")
        return response_data
    except Exception as ex:
        # Log unexpected errors with full stack trace
        # lg.error(f"Unexpected error occurred while processing user_prompt and generating response for user_id: {data.get('user_id')} chat_id: {data.get('chat_id')}: {str(e)}")
        lg.error(f"Function Name : add_user_prompt_and_generate_response - HTTPException - {ex} for user id : {user_id}, chat_id: {chat_id}, user_id: {user_id}")
        raise


# TODO : Creating a seperate enpoint to Save Cache Data into MongoDB : Reason for simplicity
# app/chat_routes.py

@router.post("/save_cached_data_to_db")
async def save_cached_data_to_db():
    try:
        lg.info("Starting the process of saving cached data to MongoDB.")
        for cache_key in list(cache.cache.keys()):
            user_id, chat_id = cache_key.split("_")
            cached_chat = cache.get_from_cache(cache_key)
            
            if cached_chat:
                # Log the data being processed at DEBUG level
                lg.debug(f"Processing cache for user_id: {user_id}, chat_id: {chat_id}")

                # Add the cached messages to the corresponding chat in MongoDB                 
                result = db.chats.update_one(
                    {"user_id": user_id, "chats.chat_id": chat_id},
                    {
                        "$push": {"chats.$.messages": {"$each": cached_chat["messages"]}},
                        "$set": {"chats.$.updated_at": datetime.now()}
                    }
                )
        # Notice : Update : 1. Saving in result, and using result for further logging.        
                # Log the result of the update operation
                if result.modified_count > 0:
                    lg.info(f"Successfully added cached messages for user {user_id}, chat_id {chat_id}")
                else:
                    lg.warning(f"No modification made for user {user_id}, chat_id {chat_id} - No matching chat found")

                # Clear the cache after saving to DB
                cache.clear_cache()

        # INFO level: Log successful operation when message is added
        lg.info(f"Message added successfully for user {user_id}, chat_id {chat_id}")
        return {"status": "Cached data saved to MongoDB"}

    except Exception as ex:
        # EXCEPTION level: Log any unexpected errors with the full stack trace
        # lg.error(f"Unexpected error occurred: {str(e)}")
        lg.error(f"Function Name : save_cached_data_to_db - HTTPException - {ex} for user id : {user_id}")
        raise


# TODO : 1. Add Number of days/How many days to fetch 2. Write in Cache
# TODO: 2. Modify to fetch a batch of 90 days only instead of all chats
# TODO 3: Check from cache
# TODO AwaitSol: Updated Logic that 1. Fetch 90 days data from mongo 
# 2. Stores in cache and sends 30 days data as response, checks from cache.
# Global variable to track the hit count

count_hit = 0  # Initializing with 1 hit for the first request


@router.get("/get_chats")
async def get_chats(data: DateRangeFilter, username: str = Header(...), password: str = Header(...)):
    user_id = data.user_id
    current_date = datetime.now()
    global count_hit

    try:
        # Log the incoming request with headers and user details
        lg.info(f"Received request for user_id: {user_id}, username: {username}, count_hit: {count_hit}")
        # TODO:  implement this when session is defined by FE
        # Check if the count_hit is stored in the session, if not, initialize it
        # count_hit = session.get('count_hit', 1)

        # # Determine start_date and end_date based on count_hit logic
        # if count_hit == 1:
        #     end_date = current_date - timedelta(days=30)
        #     start_date = end_date - timedelta(days=30)
        # else:
        #     end_date = current_date - timedelta(days=(count_hit * 30))
        #     start_date = end_date - timedelta(days=30)

        # # Update session with the incremented count_hit
        # session['count_hit'] = count_hit + 1

        # Calculate end_date and start_date based on the count_hit logic
        if count_hit == 0:
            end_date = current_date
            start_date = end_date - timedelta(days=30) 
        else:
            end_date = current_date - timedelta(days=(count_hit * 30))
            start_date = end_date - timedelta(days=30)

        # Log the date range calculation
        lg.debug(f"Calculated date range: start_date = {start_date}, end_date = {end_date}")

        # Check cache key based on user_id
        cache_key = f"{user_id}"
        cache_key_hash = hashlib.sha256(cache_key.encode()).hexdigest()
        print(f"Count Hit : {count_hit}")
        print(f"Cache Key: {cache_key_hash}")
        lg.debug(f"Generated cache key hash: {cache_key_hash}")

        # Check if the data is in the cache
        cached_data = cache.get_from_cache(cache_key_hash)

        if cached_data:
            lg.info("Cache hit. Checking if cache contains the requested date range.")

            # Cache hit: Check if the cached data contains the requested date range
            print("Cache hit. Checking if cache contains the requested date range.")    
            cached_start_date = ignore_milliseconds(cached_data["start_date"])
            cached_end_date = ignore_milliseconds(cached_data["end_date"])

            print(f"Cached Date Range: {cached_start_date} to {cached_end_date}")
            print(f"Requested Date Range: {start_date} to {end_date}")

            lg.debug(f"Cached Date Range: {cached_start_date} to {cached_end_date}")
            lg.debug(f"Requested Date Range: {start_date} to {end_date}")

            # if cached_start_date <= start_date and cached_end_date >= end_date:
            if start_date >= cached_start_date and end_date <= cached_end_date:                
                print("Cache data covers the requested range.")
                recent_chats = cached_data["chats"]
                lg.info("Cache data covers the requested range. Returning cached chats.")                
            else:
                # Cache is missing some data: Fetch next 90 days from MongoDB
                print("Cache data is incomplete. Fetching missing data from MongoDB...")
                lg.info("Cache data is incomplete. Fetching missing data from MongoDB...")

                new_end_date = end_date
                new_start_date = end_date - timedelta(days=90)

                new_chats = await fetch_chats_from_db(user_id, new_start_date, new_end_date)

                recent_chats = cached_data["chats"] + new_chats
                cache.add_to_cache(cache_key_hash, {
                    "chats": recent_chats,
                    "start_date": new_start_date,
                    "end_date": new_end_date
                })
        else:
            # Cache miss: Fetch 90 days of data from MongoDB
            print("Cache miss. Fetching 90 days of data from MongoDB...")
            lg.info("Cache miss. Fetching 90 days of data from MongoDB...")

            new_end_date = end_date
            new_start_date = end_date - timedelta(days=90)

            new_chats = await fetch_chats_from_db(user_id, new_start_date, new_end_date)

            lg.info(f"Saving {len(new_chats)} new chats to cache for user_id: {user_id}.")
            cache.add_to_cache(cache_key_hash, {
                "chats": new_chats,
                "start_date": new_start_date,
                "end_date": new_end_date
            })

            recent_chats = new_chats

        # Define the date range for the response (last 30 days)
        response_end_date = end_date
        response_start_date = end_date - timedelta(days=30)

        response_chats = [
            chat for chat in recent_chats
            if response_start_date <= chat["created_at"] <= response_end_date
        ]

        print(f"Returning {len(response_chats)} chats from cache")
        lg.info(f"Returning {len(response_chats)} chats from cache or DB within date range {response_start_date} to {response_end_date}")

        if not response_chats:
            lg.warning(f"No chats found within the date range for user_id: {user_id}. Returning empty list.")
            return {"user_id": user_id, "chats": []}

        # Increment the global hit count
        count_hit += 1
        lg.debug(f"Incremented count_hit to {count_hit}")

        return {"user_id": user_id, "chats": response_chats}
    except Exception as ex:
        # Log unexpected errors with full stack trace
        lg.error(f"Function Name : save_cached_data_to_db - HTTPException - {ex} for user id : {user_id}")
        raise


async def fetch_chats_from_db(user_id: str, start_date: datetime, end_date: datetime):
    try:
        user_chats = db.chats.find_one({"user_id": user_id}, {"_id": 0})
        if not user_chats:
            lg.warning(f"No chats found for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="No chats found for this user")

        recent_chats = [
            chat for chat in user_chats["chats"]
            if start_date <= chat["created_at"] <= end_date
        ]
        lg.debug(f"Fetched {len(recent_chats)} chats from DB for user_id: {user_id} within date range {start_date} to {end_date}")
        return recent_chats
    except Exception as e:
        lg.error(f"Error fetching chats from DB for user_id: {user_id}: {str(e)}")
        raise
