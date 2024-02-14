import time
import logging
from pythonjsonlogger import jsonlogger

def initialise_logger(level=logging.CRITICAL, stream=False, logfile=None, name=None):
    """
    Initializes and returns a logger with JSON formatting.

    This function configures a logging instance that can output logs either to a stream (such as console)
    or a specified logfile, with messages formatted in JSON. The time is converted to GMT for consistency
    across different time zones. 

    Parameters:
    - level (int, optional): The logging level, defaults to logging.CRITICAL. 
      Determines the severity of the messages that the logger will handle.
    - stream (bool, optional): If True, logs will be output to the console. Defaults to False.
    - logfile (str, optional): The path to a file where logs will be written. If None, no file logging is setup. Defaults to None.
    - name (str, optional): Name of the logger. A logger with the same name returns the same logger instance. Defaults to None.

    Returns:
    - logging.Logger: Configured logger instance with the specified parameters.
    """

    # Obtain a logger instance. If `name` is None, returns a root logger.
    logger = logging.getLogger(name)
    
    # Define a custom format for the logs. Adjust the format as per requirements.
    custom_format = "%(asctime) %(levelname) %(message)"
    
    # Set up JSON formatting using the custom format. The time is converted to GMT.
    formatter = jsonlogger.JsonFormatter(custom_format)
    formatter.converter = time.gmtime  # Converts log time to GMT for uniformity.

    # If stream logging is enabled, configure stream handler with the formatter.
    if stream:
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

    # If logfile path is provided, configure file handler with the formatter.
    if logfile:
        log_handler = logging.FileHandler(logfile)
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

    # Set the logger's level to the specified level.
    logger.setLevel(level)

    # Return the configured logger instance.
    return logger
