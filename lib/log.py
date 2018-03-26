import logging

FORMAT   = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

def get_wegbot_logger():
    logger = logging.getLogger("Wegbot")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("logs/wegbot.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
