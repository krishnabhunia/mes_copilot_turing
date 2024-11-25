from fastapi import FastAPI
from app.chat_routes import router  # Updated import to avoid conflict

app = FastAPI()

# Include routes
app.include_router(router)

# Run the app with:
# uvicorn app.main:app --reload
