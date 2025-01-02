Logging Service
This repository contains the code for a centralized logging service built with FastAPI.
The service allows for the upload and retrieval of log files, with structured logging and dynamic folder creation based on the service, workflow, sub-workflow, and date.

Features
Log Data Upload: Upload log data and save it to dynamically generated directories based on service name and workflow.
Log File Handling: Supports multiple file types (logs, CSV, PDF, etc.).
Log Retrieval: Retrieve logs by filtering on service name, log date, or file type.
File Serving: Serve log files via HTTP for download.
Rotating Log Handler: Use rotating log files with a specified size limit and backup count.

Requirements
Python 3.12.4
fastAPI[all]
uvicorn
requests

Clone the repository to your local machine:
git clone <repository_url>

Navigate to the project directory:
cd Logging01
Install the required Python dependencies:

pip install -r requirements.txt
If using Docker, you can build and run the container using Docker Compose:

docker-compose up --build
This will set up the FastAPI server and other necessary services.

Configuration
The logging service uses a Config.json file to configure logging behavior. Below is an example of the configuration file:
{
    "loglevel": "DEBUG",
    "badrequest": 400,
    "statusok": 200,
    "CORS_HEADERS": "Content-Type",
    "host": "fast_api_server",
    "port": 8000,
    "logfileName": "logfile.log",
    "base_logdirectory": "/app/log_directory",
    "logURL": "http://fast_api_server:8000/uploadToLogfile",
    "logHandler": {
        "mode": "a",
        "maxBytes": 3145728,
        "backupCount": 10,
        "delay": false
    }
}
Configuration Parameters:
loglevel: Logging level (e.g., DEBUG, INFO, ERROR).
logfileName: Name of the log file.
base_logdirectory: Base directory for storing logs inside the Docker container or on your host.
logHandler: Configures the log handler (mode, max file size, number of backups, etc.).
Endpoints
1. GET /
Returns a simple hello message to verify the server is running.

Example:
GET http://localhost:8000/
Response:
"Hello, World from Logging!!"

2. POST /uploadToLogfile
Uploads log data or files to be saved in the appropriate directory.

Parameters (form data):
servicename (required): Name of the service (e.g., chatbot, Knowledge Management).
logdata (optional): Log data to be saved as a text file.
file_type (optional): Type of the file (default is logs).
files (optional): Files to be uploaded (can be any type).
Example:
POST http://localhost:8000/uploadToLogfile
Content-Type: multipart/form-data

{
    "servicename": "chatbot",
    "logdata": "Sample log data",
    "file_type": "logs",
    "files": [file_data_here]
}

3. GET /retrieveLogs
Retrieves logs based on the filters provided (e.g., service name, log date, file type).
Parameters:
servicename : The name of the service.
logdate (optional): The log date (e.g., 2024-11-29 or current date).
file_type (optional): The file type (e.g., logs, csv, pdf).

Example:
GET http://localhost:8000/retrieveLogs?servicename=chatbot&logdate=2024-11-29&file_type=logs
4. GET /serveFile
Serves a log file for download based on the file path.

Parameters:
filepath (required): The relative path of the file to be served.
Example:
GET http://localhost:8000/serveFile?filepath=Chatbot/2024-11-29/logfile.log

Log Directory Structure
Logs are stored in a directory structure based on the following:
Service name
Workflow (if applicable)
Date
File type

Docker Volume structure:
/app/log_directory/
    Knowledge Management/
        SIPOC Workflow/
            Standard Workflow/
                log_2024-11-29.log
                
    Chatbot/
        2024-11-29/
            logs/
                log_2024-11-29.log
            Pdf/  (like same for CSV,Docx,XML, Test)
                sample.pdf
    Logging/
        2024-11-29/
                logfile.log
                logfile.log.1
        2024-11-30/
                logfile.log
        

Docker Setup
To containerize the service with Docker, the following docker-compose.yml file is provided:

services:
  fast_api_server:
    build:
      context: ./Logging01
    volumes:
      - uploads:/app/log_directory
    ports:
      - "8000:8000"

  fast_api_server_dummy:
    build:
      context: ./dummy_api_service
    ports:
      - "8005:8005"
    depends_on:
      - fast_api_server
  
  python_script_upload:
    build:
      context: ./service_log_files
    depends_on:
      - fast_api_server

volumes:
  uploads:


To run the service with Docker:
Build the services:
docker-compose up --build
Access the service at http://localhost:8000.

Logging:
Logs are handled by a rotating file handler, ensuring that log files do not grow too large. The configuration allows for setting the maximum file size and the number of backups to keep.

Contribution:
Feel free to fork this repository and submit pull requests if you would like to contribute improvements or features.
