# import logging
import sys

IMPORTANT_INFO_LEVEL = 25

# def get_logger():
#     # Create a custom logger
#     logger = logging.getLogger("")
#     logger.setLevel(logging.DEBUG)


#     # Create handlers
#     c_handler = logging.StreamHandler()
#     f_handler = logging.FileHandler('logs/logs.log')
#     c_handler.setLevel(IMPORTANT_INFO_LEVEL)
#     f_handler.setLevel(IMPORTANT_INFO_LEVEL)

#     # Create formatters and add it to handlers
#     c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     c_handler.setFormatter(c_format)
#     f_handler.setFormatter(f_format)

#     # Add handlers to the logger
#     logger.addHandler(c_handler)
#     logger.addHandler(f_handler)
    
#     return logger

def get_logger():
    return None

if __name__ == "__main__":
    l = get_logger()
    l.error("Error!")