import logging
from .common import default_log_format

default_formatter = default_log_format()


class Logger:
    _logger = None

    @staticmethod
    def make_stream_logger(name: str, formatter: str, level: int = logging.DEBUG) -> logging.Logger:
        logger = logging.getLogger(name)
        stream_logger = logging.StreamHandler()
        stream_logger.setFormatter(formatter)
        logger.addHandler(stream_logger)
        logger.setLevel(level)
        logger.propagate = False

        return logger

    @classmethod
    def set_logger(cls, logger) -> logging.Logger:
        cls._logger = logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if not cls._logger:
            cls._logger = Logger.make_stream_logger('ROOT', default_formatter)
        return cls._logger


class LoggerInstance(Logger):
    def __init__(self, logger_name: str, formetter: str = default_formatter):
        self.set_logger(Logger.make_stream_logger(logger_name, formetter))

    @property
    def logger(self) -> logging.Logger:
        return self.get_logger()

    @classmethod
    def get_instance(cls) -> logging.Logger:
        return cls.get_logger()
