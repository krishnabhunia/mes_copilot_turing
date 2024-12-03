# Logging/Logging01/app.py
from datetime import datetime
import os
import json
import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from logger_config import LoggerConfig
from fastapi.responses import FileResponse

# Load configuration from Config.json
with open('Config.json', 'r') as f:
    config = json.load(f)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=86400
)

# Initialize LoggerConfig
logger_config = LoggerConfig(config)
logger = logger_config.get_logger()

# base_logdirectory = '/app/log_directory'
base_logdirectory = config["base_logdirectory"]
# base_logdirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../log_directory'))


class UploadLog:
    def __init__(self, servicename: str, logdata: str= None, file_type: str= None, sub_workflow: str = None):
        self.servicename = servicename
        self.logdata = logdata
        self.file_type = file_type if file_type else 'logs'  # Default to 'logs' if file_type is not provided
        self.sub_workflow = sub_workflow
        self.logdate = datetime.now().strftime('%Y-%m-%d')

        # Base log directory (could be dynamically configured or hardcoded)
        self.base_logdirectory = config["base_logdirectory"]
        # self.base_logdirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../log_directory'))

        # Dynamically create the folder structure based on service, workflow, sub-workflow, and log date
        self.logdirectory = self._build_directory_structure()

        # Create the directory if it doesn't exist
        os.makedirs(self.logdirectory, exist_ok=True)

    def _build_directory_structure(self):
        """
        Dynamically build directory structure based on service, workflow, and date.
        """
        if self.servicename.lower() in ['standard template', 'custom template', 'batch record workflow', 'visio workflow']:
            base_directory = os.path.join(self.base_logdirectory, "Knowledge Management")

            if self.servicename.lower() == 'standard template':
                return os.path.join(base_directory, 'SIPOC Workflow', 'Standard Workflow', self.logdate)

            elif self.servicename.lower() == 'custom template':
                return os.path.join(base_directory, 'SIPOC Workflow', 'Custom Workflow', self.logdate)

            elif self.servicename.lower() == 'batch record workflow':
                return os.path.join(base_directory, 'Batch Record Workflow', self.logdate)

            elif self.servicename.lower() == 'visio workflow':
                return os.path.join(base_directory, 'Visio Workflow', self.logdate)

        elif self.servicename.lower() == 'chatbot':
            # Define the directory for Chatbot service outside of Knowledge Management
            return os.path.join(self.base_logdirectory, 'Chatbot', self.logdate, self.file_type)

        else:
            # Default fallback for unknown services outside of Knowledge Management
            return os.path.join(self.base_logdirectory, self.servicename, self.logdate, self.file_type)

    def save_log(self, file_content=None, filename=None):
        """
        Save the log data (text or file) to the appropriate directory.
        """
        try:
            logger.info(f"Attempting to save log data for service '{self.servicename}', type '{self.file_type}'")

            if self.file_type == 'logs':
                # Save logs to a log file
                log_file_path = os.path.join(self.logdirectory, f'log_{self.logdate}.log')
                with open(log_file_path, 'a') as logfile:
                    logfile.write(self.logdata + "\n")
            else:
                # Handle dynamic file types (e.g., CSV, PDF, DOCX, etc.)
                if filename:
                    file_path = os.path.join(self.logdirectory, filename)
                    with open(file_path, 'wb') as file:
                        file.write(file_content)
                else:
                    # If no file content or filename, save logdata to a default file
                    default_log_path = os.path.join(self.logdirectory, f'default_{self.logdate}.log')
                    with open(default_log_path, 'a') as default_logfile:
                        default_logfile.write(self.logdata + "\n")

            logger.info(f"File saved successfully in {self.logdirectory}")
            return {"message": "File saved successfully", "path": self.logdirectory}
        except Exception as e:
            logger.error(f"Error saving logs: {e}")
            raise HTTPException(status_code=500, detail="Error saving files")


@app.get("/")
def hello():
    return "Hello, World from Logging!!"


@app.post("/uploadToLogfile")
async def upload_to_logfile(request: Request, files: list[UploadFile] = File(None)):
    
    try:
        print("API 1")
        form_data = await request.form()  # Use form() instead of json() to handle multipart/form-data
        servicename = form_data.get('servicename')
        logdata = form_data.get('logdata', '')  # Default to empty string if not provided
        file_type = form_data.get('file_type', 'logs')
        
        print("servicename,logdata,file_type", servicename, logdata,file_type)
        # Validate input
        if not servicename:
            logger.error("Missing required fields: servicename ")
            raise HTTPException(status_code=400, detail="Missing required fields: servicename")

        if not file_type:
            logger.error("Missing required field: file_type")
            raise HTTPException(status_code=400, detail="Missing required field: file_type")

        # Create an UploadLog instance
        upload_log = UploadLog(servicename, logdata, file_type)
        print("upload_log",upload_log)
        # If files are included in the request, save them
        if files:
            for file in files:
                file_content = await file.read()
                upload_log.save_log(file_content=file_content, filename=file.filename)
            return {"message": "Files uploaded successfully"}
        
        if logdata:
            upload_log.save_log()
            return {"message": "Log data saved successfully in the default folder"}
        else:
            return {"message": "No log data provided, only files uploaded."}


    except Exception as e:
        logger.error(f"Error in uploadToLogfile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/retrieveLogs")
def retrieve_logs(servicename: str = None, logdate: str = None, file_type: str = None):
    # Start with the base path of the Docker volume
    search_directory = base_logdirectory
    
    # Dynamically add filters to construct the directory path
    if servicename:
        search_directory = os.path.join(search_directory, servicename)
    if logdate:
        search_directory = os.path.join(search_directory, logdate)
    if file_type:
        search_directory = os.path.join(search_directory, file_type)

    # Check if the directory exists
    if not os.path.exists(search_directory):
        logger.error(f"No logs found for the given filters")
        raise HTTPException(status_code=404, detail="No logs found")

    # Retrieve all files recursively from the directory
    logs = {}
    for root, _, files in os.walk(search_directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Generate the relative path with respect to `base_logdirectory`
            relative_path = os.path.relpath(file_path, base_logdirectory)
            
            # Construct a clean URL for the file
            logs[relative_path] = {
                "url": f"http://{config['host']}:{config['port']}/serveFile?filepath={relative_path}"
            }
            success_message = f"Logs retrieved successfully for {logs}" 

    logger.info(success_message)
    return {"message": "Logs retrieved successfully", "logs": logs}



@app.get("/serveFile")
def serve_file(filepath: str):
    try:
        # Construct the absolute file path in the Docker volume
        absolute_path = os.path.join(base_logdirectory, filepath)
        if not os.path.exists(absolute_path):
            logger.error(f"File not found: {absolute_path}")
            raise HTTPException(status_code=404, detail="File not found")

        # Serve the file
        return FileResponse(absolute_path)

    except Exception as e:
        logger.error(f"Error serving file: {e}")
        raise HTTPException(status_code=500, detail="Error serving file")


if __name__ == "__main__":
    uvicorn.run(app, host=config["host"], port=config["port"])






