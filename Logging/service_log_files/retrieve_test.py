# retrive_test.py
import requests
import time

time.sleep(1)
# Retrieve logs metadata
response = requests.get("http://fast_api_server:8000/retrieveLogs", params={"servicename": "Knowledge Management"})

# # Retrieve logs metadata
# # response = requests.get("http://127.0.0.1:7408/retrieveLogs")
# response = requests.get("http://127.0.0.1:7408/retrieveLogs", params={"servicename": "chat"})

# response = requests.get("http://127.0.0.1:7408/retrieveLogs", params={"servicename": "chat", "logdate": "2024-11-26"})

# response = requests.get("http://127.0.0.1:8000/retrieveLogs", params={"servicename": "chatbot", "logdate": "2024-11-26", "file_type":"pdf"})

# response = requests.get("http://127.0.0.1:7408/retrieveLogs",params={"servicename": "chat", "logdate": "2024-11-22"})
metadata = response.json()

print("Logs Metadata:")
print(metadata)



# if "logs" in metadata:
#     for filename, file_info in metadata["logs"].items():
#         file_url = file_info.get("url")
#         if file_url:
#             print(f"Downloading file from: {file_url}")
#             try:
#                 file_response = requests.get(file_url, timeout=10)
#                 if file_response.status_code == 200:
#                     local_filename = filename.replace("/", "_")  # Avoid folder creation locally
#                     with open(local_filename, "wb") as f:
#                         f.write(file_response.content)
#                     print(f"Downloaded file successfully: {local_filename}")
#                 else:
#                     print(f"Failed to download file: {file_url} (HTTP {file_response.status_code})")
#             except requests.RequestException as e:
#                 print(f"Failed to download file: {file_url} (Error: {e})")
# else:
#     print("No logs found.")

