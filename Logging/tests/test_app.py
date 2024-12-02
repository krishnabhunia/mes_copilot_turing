import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add Logging01 to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../Logging01")))

# Change working directory for the test
os.chdir(os.path.join(os.path.dirname(__file__), "../Logging01"))

from app import app  # Make sure app is imported correctly

client = TestClient(app)

# Setup log environment before all tests
@pytest.fixture(scope="module", autouse=True)
def setup_log_environment():
    base_logdirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../log_directory"))
    
    # Chatbot - Logs and Pdf
    os.makedirs(os.path.join(base_logdirectory, "Chatbot/2024-12-02/logs"), exist_ok=True)
    with open(os.path.join(base_logdirectory, "Chatbot/2024-12-02/logs/log_2024-12-02.log"), "w") as f:
        f.write("Sample log content for Chatbot logs testing")

    os.makedirs(os.path.join(base_logdirectory, "Chatbot/2024-12-02/Pdf"), exist_ok=True)
    with open(os.path.join(base_logdirectory, "Chatbot/2024-12-02/Pdf/sample.pdf"), "wb") as f:
        f.write(b"%PDF-1.4 Sample PDF content for testing")

    # Logging
    os.makedirs(os.path.join(base_logdirectory, "Logging/2024-12-02"), exist_ok=True)
    with open(os.path.join(base_logdirectory, "Logging/2024-12-02/logfile.log"), "w") as f:
        f.write("Sample log file content for Logging/2024-12-02")
    with open(os.path.join(base_logdirectory, "Logging/2024-12-02/logfile.log.1"), "w") as f:
        f.write("Sample rolled over log content for Logging/2024-12-02")

    os.makedirs(os.path.join(base_logdirectory, "Logging/2024-12-02"), exist_ok=True)
    with open(os.path.join(base_logdirectory, "Logging/2024-12-02/logfile.log"), "w") as f:
        f.write("Sample log file content for Logging/2024-12-02")

# Test for the root endpoint
def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"Hello, World from Logging!!"'

# Test uploading log files
def test_upload_logfile():
    data = {"servicename": "Chatbot", "logdata": "Test log entry for pytest", "file_type": "logs"}
    response = client.post("/uploadToLogfile", data=data)
    assert response.status_code == 200
    assert "Log data saved successfully" in response.json()["message"]

# Test retrieving logs for Chatbot
def test_retrieve_logs_chatbot():
    response = client.get("/retrieveLogs", params={"servicename": "Chatbot", "logdate": "2024-12-02"})
    assert response.status_code == 200
    assert "Chatbot/2024-12-02/logs/log_2024-12-02.log" in response.json()["logs"]

# Test serving a log file for Chatbot
def test_serve_file_chatbot():
    response = client.get("/serveFile", params={"filepath": "Chatbot/2024-11-29/logs/log_2024-11-29.log"})
    assert response.status_code == 200
    assert response.content == b"Sample log content for Chatbot logs testing"

# Test serving a PDF file for Chatbot
def test_serve_file_pdf():
    response = client.get("/serveFile", params={"filepath": "Chatbot/2024-11-29/Pdf/sample.pdf"})
    assert response.status_code == 200
    assert b"%PDF-1.4 Sample PDF content for testing" in response.content


