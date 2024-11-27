from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

# Base URL of the app.py service
MAIN_LOGGING_SERVICE_URL = "http://127.0.0.1:7408/uploadToLogfile"  # app.py runs on port 7408

@app.post("/store_logs")
async def store_logs(servicename: str, file_path: str=None):
    """
    API to send a file and metadata to the main logging FastAPI service.
    """
    file_path=r"C:\Users\vajayasr\OneDrive - Capgemini\Desktop\Logging sys\Logging01\Batch-Manufacturing-Record01.docx"
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail=f"File '{file_path}' does not exist")

        with open(file_path, "rb") as file:
            files = {"files": (os.path.basename(file_path), file, "application/octet-stream")}
            payload = {
                "servicename": servicename,
                "file_type": "logs",  # or adjust based on file type
            }

            # Send POST request to the main logging service
            response = requests.post(MAIN_LOGGING_SERVICE_URL, data=payload, files=files)

        # Return response from the logging service
        return {"status": response.status_code, "response": response.json()}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with logging service: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
