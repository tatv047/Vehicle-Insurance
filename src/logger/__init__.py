import logging
import os
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

# Constants for log configuration
LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Number of backup log files to keep

# Construct log file path
log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)
log_file_path = os.path.join(log_dir_path, LOG_FILE)

def configure_logger():
    """
    Configures logging with a rotating file handler and a console handler.
    """
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Define formatter
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Configure the logger
configure_logger()



# Better approach that handles duplicacy,will imporve later on 

# import logging
# import os
# from logging.handlers import RotatingFileHandler
# from from_root import from_root
# from datetime import datetime
# import sys

# # Constants for log configuration
# LOG_DIR = 'logs'
# LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
# BACKUP_COUNT = 3  # Number of backup log files to keep

# # Construct log file path
# log_dir_path = os.path.join(from_root(), LOG_DIR)
# os.makedirs(log_dir_path, exist_ok=True)
# log_file_path = os.path.join(log_dir_path, LOG_FILE)

# def configure_logger(logger_name=None, force_reconfigure=False):
#     """
#     # Configures logging with a rotating file handler and a console handler.
    
#     # Args:
#     #     logger_name (str, optional): Name of the logger. If None, uses root logger.
#     #     force_reconfigure (bool): If True, clears existing handlers before configuring.
    
#     # Returns:
#     #     logging.Logger: Configured logger instance
#     """
#     # Get logger - use named logger if provided
#     logger = logging.getLogger(logger_name)
    
#     # Prevent duplicate handlers
#     if logger.handlers and not force_reconfigure:
#         return logger
    
#     # Clear existing handlers if force_reconfigure or if it's the root logger
#     if force_reconfigure or logger_name is None:
#         logger.handlers.clear()
    
#     # Set logger level
#     logger.setLevel(logging.DEBUG)
    
#     # Prevent propagation to avoid duplicate messages (except for root logger)
#     if logger_name is not None:
#         logger.propagate = False
    
#     # Define formatter with more detailed format
#     formatter = logging.Formatter(
#         "[ %(asctime)s ] %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
#         datefmt='%Y-%m-%d %H:%M:%S'
#     )

#     try:
#         # File handler with rotation
#         file_handler = RotatingFileHandler(
#             log_file_path, 
#             maxBytes=MAX_LOG_SIZE, 
#             backupCount=BACKUP_COUNT,
#             encoding='utf-8'  # Ensure proper encoding
#         )
#         file_handler.setFormatter(formatter)
#         file_handler.setLevel(logging.DEBUG)
#         logger.addHandler(file_handler)
        
#     except Exception as e:
#         print(f"Warning: Could not set up file logging: {e}", file=sys.stderr)
    
#     # Console handler with colored output (optional)
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setFormatter(formatter)
#     console_handler.setLevel(logging.INFO)
#     logger.addHandler(console_handler)
    
#     return logger

# def get_logger(name=None):
#     """
#     # Get a configured logger instance.
    
#     # Args:
#     #     name (str, optional): Logger name. If None, returns root logger.
    
#     # Returns:
#     #     logging.Logger: Logger instance
#     """
#     return logging.getLogger(name)

# # Configure the root logger only once
# _root_logger_configured = False

# def setup_logging(force=False):
#     """
#     # Setup logging configuration. Call this once at the start of your application.
    
#     # Args:
#     #     force (bool): Force reconfiguration even if already configured
#     """
#     global _root_logger_configured
    
#     if _root_logger_configured and not force:
#         return
    
#     # Configure root logger
#     configure_logger(logger_name=None, force_reconfigure=force)
#     _root_logger_configured = True
    
#     # Log startup message
#     logger = get_logger(__name__)
#     logger.info("Logging system initialized")
#     logger.info(f"Log file: {log_file_path}")

# # Auto-configure on import (optional - you can remove this line if you prefer manual setup)
# setup_logging()


# # Example usage functions
# def example_usage():
#     # Example of how to use the logging system
    
#     # Get logger for current module
#     logger = get_logger(__name__)
    
#     # Log different levels
#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
    
#     # Get logger for specific class/module
#     class_logger = get_logger("MyClass")
#     class_logger.info("This is from MyClass")

# if __name__ == "__main__":
#     example_usage()
