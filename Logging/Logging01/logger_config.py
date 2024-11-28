#Logging_sys/logger_config.py
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import json

class LoggerConfig:
    def __init__(self, readfile):
        self.logger = logging.getLogger(__name__)
        # Load configuration from Config.json
        # config_path = os.path.join(os.path.dirname(__file__), '../Logging01/Config.json')
        config_path = os.path.join(os.path.dirname(__file__), 'Config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        # Define the central log directory
        base_logdirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../log_directory'))
        # base_logdirectory = '/app/log_directory'   # Docker volume path

        
        # Ensure main logdirectory exists
        if not os.path.exists(base_logdirectory):
            os.makedirs(base_logdirectory)
            
        logging_directory = os.path.join(base_logdirectory, 'Logging')
        current_date_folder = datetime.now().strftime('%Y-%m-%d')
        logdirectory = os.path.join(logging_directory, current_date_folder)
        if not os.path.exists(logdirectory):
            os.makedirs(logdirectory)
        logfile = os.path.join(logdirectory, readfile["logfileName"])

        logHandler = RotatingFileHandler(
            logfile,
            mode=config["logHandler"]["mode"],
            maxBytes=config["logHandler"]["maxBytes"],  
            backupCount=config["logHandler"]["backupCount"],  
            delay=config["logHandler"]["delay"]
        )

        
        # logFormatter = logging.Formatter('[%(levelname)s]\t: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logFormatter = logging.Formatter('[%(levelname)s]\t: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logHandler.setFormatter(logFormatter)

        # Add the handler to the logger
        self.logger.addHandler(logHandler)
        logLevel = readfile['loglevel']
        numeric_level = getattr(logging, logLevel.upper(), 10)
        self.logger.setLevel(level=numeric_level)

    def get_logger(self):
        return self.logger














