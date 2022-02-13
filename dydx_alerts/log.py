import logging

IMPORTANT_INFO_LEVEL = logging.INFO + 5

def get_logger():
    """
    Instantiates the canonical logger used by all bot modules.
    """
    # Create a custom logger
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("logs/logs.log")
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    f_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

if __name__ == "__main__":
    l = get_logger()
    l.error("Error!")
