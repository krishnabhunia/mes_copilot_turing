import requests
import os
import asyncio
import sys
import json
import time
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Logging01')))


async def test_upload_to_logfile():
    # url = "http://127.0.0.1:7408/uploadToLogfile"  
    URL = "http://fast_api_server:8000/uploadToLogfile"
    
    # Test payload
    payload = {
        "servicename": "chatbot",
        "logdata": "This is a sample log entry for testing.",
        "file_type": "pdf"
    }
    print(f"Payload: {payload}")

    # Test file upload
    file_name = 'Batch-Manufacturing-Record01.pdf'
    file_path = os.path.abspath(file_name)
    # file_path = os.getcwd() + "/service_log_files/" + file_name

    # logger.debug("Starting file upload...")
    try:
        
        with open(file_path, "rb") as f:
            files = {"files": (os.path.basename(file_path), f, "pdf")}
            print(f"Files: {files}")

            # Send POST request to the FastAPI service
            print(URL, payload, files)
            response = requests.post(URL, data=payload, files=files)

        print("Response Status Code:", response.status_code)
        print("Response JSON:", response.json())
    except requests.exceptions.RequestException as e:
        # logger.error(f"Error during request: {e}")
        print("Error during request:", e)


# To run the async function in the local script
if __name__ == "__main__":
    # Run the async function using asyncio
    time.sleep(1)
    asyncio.run(test_upload_to_logfile())













# from fastapi import FastAPI, HTTPException
# import requests
# import os

# app1 = FastAPI()

# # Define the logging service URL
# logging_service_url = "http://127.0.0.1:8000/uploadToLogfile"

# # Hardcoded file location
# FILE_PATH = r"C:\Users\vajayasr\OneDrive - Capgemini\Desktop\Logging sys\service\Batch-Manufacturing-Record01.pdf"

# @app1.post("/sendLog")
# async def send_log(servicename: str, logdata: str or None, file_type: str = "logs"):
#     """
#     API to send log data and a hardcoded file to the logging service.
#     """
#     # Validate input
#     if not servicename or not logdata:
#         raise HTTPException(status_code=400, detail="Missing required fields: servicename or logdata")

#     # Prepare the payload
#     # payload = {
#     #     "servicename": servicename,
#     #     "logdata": logdata,
#     #     "file_type": file_type
#     # }
#     payload = {
#         "servicename": "chat-test",
#         # "logdata": logdata,
#         "file_type": "pdf"
#     }

#     # Check if the file exists at the hardcoded location
#     if not os.path.exists(FILE_PATH):
#         raise HTTPException(status_code=404, detail=f"File not found at {FILE_PATH}")

#     try:
#         # Read the file and prepare it for upload
#         with open(FILE_PATH, "rb") as f:
#             files = {"files": (os.path.basename(FILE_PATH), f, "application/pdf")}

#             # Send the request to the logging service
#             response = requests.post(logging_service_url, data=payload, files=files)

#         return {"status": response.status_code, "response": response.json()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error sending log: {str(e)}")


# if __name__ == "__main__":
#     import uvicorn
#     # uvicorn.run(app1, host=config["host"], port=config["port"])
#     uvicorn.run(app1, host="0.0.0.0", port=5000)

