import logging, os, sys
from config import config

def generate_logger(name: str, logging_type: int, message_format: str):
    # Create a named logger
    logger = logging.getLogger(name)
    logger.setLevel(logging_type)

    # Create and configure a StreamHandler
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(message_format)
    stream_handler.setFormatter(formatter)

    # Prevent adding duplicate handlers on reload
    if not logger.handlers:
        logger.addHandler(stream_handler)

    return logger

endpoint_info_logger = generate_logger(name='api_logger_info', logging_type=logging.DEBUG, message_format="%(message)s")
endpoint_error_logger = generate_logger(name='api_logger_error', logging_type=logging.ERROR, message_format="%(message)s")