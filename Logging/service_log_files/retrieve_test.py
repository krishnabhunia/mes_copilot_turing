# retrive_test.py
import requests
import time

time.sleep(1)
# Retrieve logs metadata
# response = requests.get("http://logging_fastapi_server:7404/retrieveLogs", params={"servicename": "Knowledge Management"})

response = requests.get("http://logging_fastapi_server:7404/retrieveLogs", params={"servicename": "Chatbot"})
# # Retrieve logs metadata
# # response = requests.get("http://logging_fastapi_server:7404/retrieveLogs")
# response = requests.get("http:/logging_fastapi_server:7404/retrieveLogs", params={"servicename": "chat"})

# response = requests.get("http://logging_fastapi_server/retrieveLogs", params={"servicename": "chat", "logdate": "2024-11-26"})

# response = requests.get("http://logging_fastapi_server/retrieveLogs", params={"servicename": "chatbot", "logdate": "2024-11-26", "file_type":"pdf"})

# response = requests.get("http://logging_fastapi_server/retrieveLogs",params={"servicename": "chat", "logdate": "2024-11-22"})
metadata = response.json()

print("Logs Metadata:")
print(metadata)

