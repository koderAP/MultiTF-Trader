import logging
import os

def setup_logger(name, log_file="trade.log", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)

    return logger
