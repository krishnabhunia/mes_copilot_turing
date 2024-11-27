import requests
import os

def test_upload_to_logfile():
    # url = "http://127.0.0.1:7408/uploadToLogfile"  
    url = "http://127.0.0.1:8000/uploadToLogfile" 
    
    # Test payload
    payload = {
        "servicename": "chatbot",
        "logdata": "This is a sample log entry for testing.",
        "file_type": "pdf" 
    }
    print(f"Payload: {payload}")
    # Test file upload
    # file_path = r"/home/ironman/jayasri/Logging_mc/Logging01/Batch-Manufacturing-Record01.pdf" 
    file_path = r"C:\Users\vajayasr\OneDrive - Capgemini\Desktop\Logging sys\service\Batch-Manufacturing-Record01.pdf"
    # file_path = r"/home/ironman/jayasri/Logging_mc/Logging01/Batch-Manufacturing-Record01.docx"
    # assert os.path.exists(file_path), "Test file not found at specified path!"
    try:
        with open(file_path, "rb") as f:  
            files = {"files": (os.path.basename(file_path), f, "pdf")}
            print(f"Files: {files}")
            # Send POST request to the FastAPI service
            response = requests.post(url, data=payload, files=files)
        
        print("Response Status Code:", response.status_code)
        print("Response JSON:", response.json())
    except Exception as e:
        print("Error during request:", e)


if __name__ == "__main__":
    test_upload_to_logfile()




