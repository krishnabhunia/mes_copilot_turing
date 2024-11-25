import os
import logging
from datetime import datetime


class Local_Logger:
    def __init__(self):
        self.folderPath = 'ChatBotBackEnd_Logs'
        print(self.create_log_folder())
        self.tdate = datetime.now().strftime("%Y-%b-%d")
        self.filename = os.path.join(os.getcwd() + '/' + self.folderPath, f"ChatBotBackEnd_{self.tdate}.log")
        logging.basicConfig(
            filename=self.filename,
            level="INFO",
            format="[%(asctime)s][%(levelname)s] - \t%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        return self.logger

    def create_log_folder(self):
        if not os.path.exists(os.path.join(os.getcwd(), self.folderPath)):
            os.makedirs(os.path.join(os.getcwd(), self.folderPath))
        return os.path.join(os.getcwd(), self.folderPath)
