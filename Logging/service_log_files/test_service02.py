import requests
from pathlib import Path
import time
def test_upload_log():
    base_url = "http://logging_fastapi_server:7404/"  

    # Test cases for various services
    test_cases = [
        {
            "servicename": "Standard Template",
            "logdata": "This is a log for Standard Template test2",
            "file_type": "logs"
        },
        {
            "servicename": "Custom Template",
            "logdata": "This is a log for Custom Template test1",
            "file_type": "logs"
        },
        {
            "servicename": "Batch Record Workflow",
            "logdata": "This is a log for Batch Record Workflow test002",
            "file_type": "logs"
        },
        {
            "servicename": "Visio Workflow",
            "logdata": "This is a log for Visio Workflow 002",
            "file_type": "logs"
        },
        {
            "servicename": "Chatbot",
            "logdata": "This is a log for Chatbot service 002",
            "file_type": "logs"
        }
    ]

    for case in test_cases:
        servicename = case["servicename"]
        logdata = case["logdata"]
        file_type = case["file_type"]
        filename = case.get("filename", None)
        file_content = case.get("file_content", None)

        # Prepare the payload and files for the request
        data = {
            "servicename": servicename,
            "logdata": logdata,
            "file_type": file_type,
        }

        files = {}
        if file_content and filename:
            files["files"] = (filename, file_content)

        # Send POST request to the upload endpoint
        response = requests.post(f"{base_url}/uploadToLogfile", data=data, files=files)

        # Print results
        print(f"Test case for service: {servicename}")
        print(f"Response: {response.json()}")
        print("-" * 50)

if __name__ == "__main__":
    time.sleep(1)
    test_upload_log()
