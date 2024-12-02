import requests
import os
import asyncio
import sys
import json
import time
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Logging01')))


async def test_upload_to_logfile():
    # url = "http://127.0.0.1:7408/uploadToLogfile"  
    URL = "http://logging_fastapi_server:8000/uploadToLogfile"
    
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












