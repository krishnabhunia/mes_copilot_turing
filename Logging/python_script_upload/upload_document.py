import requests

def upload_file(file_path):
    url = "http://localhost:8000/upload/"
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "application/pdf")}
        response = requests.post(url, files=files)
    return response.json()

if __name__ == "__main__":
    response = upload_file("sample.pdf")
    print(response)
