import logging
from logging.handlers import RotatingFileHandler

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(message)s"


def get_logger(module_name) -> logging.Logger:
    """
    Создает и возвращает настроенный логгер.
    :param module_name: название логируемого модуля
    :return: Настроенный логгер.
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(LOG_LEVEL)

    handler = RotatingFileHandler(filename=f'logs/{module_name}.log', maxBytes=10 * 1024 * 1024, backupCount=5)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
