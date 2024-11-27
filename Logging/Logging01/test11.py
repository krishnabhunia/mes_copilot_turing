# Retrive data from docker volume 

import requests

# response = requests.get("http://127.0.0.1:5002/retrieveLogs")
# print(response.json())

# response = requests.get("http://127.0.0.1:5002/retrieveLogs", params={"servicename": "KM"})
# print(response.json())

# response = requests.get("http://127.0.0.1:5002/retrieveLogs", params={"servicename": "chatbot", "logdate": "2024-11-21"})
# print(response.json())

response = requests.get("http://127.0.0.1:5002/retrieveLogs", params={"servicename": "KM", "logdate": "2024-11-22"})
print(response.json())

response = requests.get("http://127.0.0.1:5002/retrieveLogs", params={"servicename": "chat"})
print(response.json())

# response = requests.get(
#     "http://127.0.0.1:5002/retrieveLogs",
#     params={"servicename": "chatbot", "logdate": "21-11-2024", "file_type": "pdf"}
# )
# print(response.json())

# response = requests.get(
#     "http://127.0.0.1:5002/retrieveLogs",
#     params={"servicename": "KM", "logdate": "22-11-2024", "file_type": "logs"}
# )
# print(response.json())