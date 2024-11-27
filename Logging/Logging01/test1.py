import requests

# Base URL of the FastAPI server
BASE_URL = "http://127.0.0.1:8000"

# Test 1: Upload log data only
response = requests.post(
    f"{BASE_URL}/uploadToLogfile",
    data={
        "servicename": "Standard Template",
        "logdata": "Standard Template log message test1",
        # "logdata": "Some log message for pdf1 test01",
        # "file_type": "pdf"
    }
)
print("Test 1 Response:", response.status_code, response.json())

# # Test 2: Upload log data with a PDF file
# file_path = r"/home/ironman/jayasri/Logging_mc/Logging01/Batch-Manufacturing-Record01.pdf"
# try:
#     with open(file_path, "rb") as f:
#         response = requests.post(
#             f"{BASE_URL}/uploadToLogfile",
#             data={
#                 "servicename": "chat",
#                 "logdata": "Some log message for pdf with file",
#                 "file_type": "pdf"
#             },
#             files={"files": (file_path.split("/")[-1], f, "application/pdf")}
#         )
#     print("Test 2 Response:", response.status_code, response.json())
# except FileNotFoundError:
#     print(f"Error: The file {file_path} does not exist.")

# # Test 3: Retrieve logs with filters
# response = requests.get(
#     f"{BASE_URL}/retrieveLogs",
#     params={
#         "servicename": "chat",
#         "logdate": "2024-11-21",
#         "file_type": "pdf"
#     }
# )
# print("Test 3 Response:", response.status_code, response.json())

# # Test 4: Retrieve all logs
# response = requests.get(f"{BASE_URL}/retrieveLogs")
# print("Test 4 Response:", response.status_code, response.json())




# import requests

# # print(requests.get("http://127.0.0.1:5002").json())

# # print(requests.get("http://127.0.0.1:5002/retrieveLogs").json())
# # print(requests.get("http://127.0.0.1:5002/retrieveLogs?servicename=chatbot&logdate=2024-11-21&file_type=logs").json())

# # print(requests.post("http://127.0.0.1:5002/uploadTologfile",
# #                     json={"logdata":"MES1","logdate": "21-11-2024"}).json())

# # print(requests.post("http://127.0.0.1:8000/uploadTologfile",
# #                     json={"logdata":111,"logdate": 19-11-2024}).json())


# # print(requests.post("http://127.0.0.1:5002/uploadToLogfile",
# #                     json={"servicename": "chatbot", "logdata": "Test log entry01"}).json())

# # print(requests.post("http://127.0.0.1:5002/uploadToLogfile",
# #                     json={"servicename": "KM", "logdata": "Test log entry for KM01"}).json())


# # print(requests.post("http://127.0.0.1:5002/uploadToLogfile",
# #                     json={"servicename": "chat","logdata": "Some log message","file_type": "csv"}).json())

# print(requests.post("http://127.0.0.1:5002/uploadToLogfile",
#                     json={"servicename": "chat","logdata": "Some log message for pdf1","file_type": "pdf"}).json())


# # print(requests.post("http://127.0.0.1:5002/uploadToLogfile",
# #                     json={"servicename": "chat","logdata": r"/home/ironman/jayasri/Logging_mc/Logging01/Batch-Manufacturing-Record01.pdf","file_type": "pdf"}).json())
