

import sys
import os
import pytest
import logging

# Add Logging01 to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../Logging01")))

from logger_config import LoggerConfig  # Now it can find `LoggerConfig`

@pytest.fixture
def config_data():
    return {
        "loglevel": "DEBUG",
        "logfileName": "logfile.log",
        "logHandler": {
            "mode": "a",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 3,
            "delay": False
        }
    }

def test_logger_config_initialization(config_data):
    logger_config = LoggerConfig(config_data)
    logger = logger_config.get_logger()
    
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) > 0


