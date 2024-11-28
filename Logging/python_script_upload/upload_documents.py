import requests

def upload_document(file_path):
    url = "http://fastapi_server:8000/upload/"
    with open(file_path, "rb") as file:
        response = requests.post(url, files={"file": file})
    print(response.json())

# Example usage
if __name__ == "__main__":
    upload_document("sample.pdf")
