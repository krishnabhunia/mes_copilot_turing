from fastapi import FastAPI, HTTPException
import requests
import os
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
 
app = FastAPI()
 
# Define the logging service URL
logging_service_url = "http://fast_api_server:8000/uploadToLogfile"
# logging_service_url= "http://127.0.0.1:7404/uploadToLogfile",
 
class LogData(BaseModel):
    servicename: str
    logdata: str | None = None
    file_type: str = "logs"
 
@app.post("/sendLog")
async def send_log(log_data: LogData):
    """
    API to send log data and a hardcoded file to the logging service.
    """

    # file_path = r"/app/data/Batch-Manufacturing-Record01.pdf"
    # file_path = r"service_log_files/Batch-Manufacturing-Record01.pdf"
    file_name = "dummy_file.pdf"
    # file_path = r"/home/ironman/jayasri/Logging sys/service01/data/Batch-Manufacturing-Record01.pdf"


    # Validate file existence
    # if not os.path.exists(file_path):
    #     raise HTTPException(status_code=404, detail="File not found")


    # # Prepare request payload and files
    payload = log_data.dict()
    file_path = os.path.join("/app", file_name)
    print(file_path)
    files = {"files": (os.path.basename(file_path), open(file_path, "rb"), "application/pdf")}

    try:
        # Send log data and file to the logging service
        response = requests.post(logging_service_url, data=payload, files=files)
        # response = requests.post(logging_service_url, data=payload)
        response.raise_for_status()
        return JSONResponse(status_code=response.status_code, content=response.json())
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=404, detail=f"Error communicating with logging service: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
