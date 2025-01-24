import logging
import json
import sys


# Логгер который давно нашёл и тяну во всех ботов

class JsonFormatter(logging.Formatter):
    def format(self, record):
        result = super().format(record)
        return json.dumps(result)


class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, buffer):
        for line in buffer.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


def bot_logger():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")  # выводим логи в консоль
    logHandler = logging.FileHandler('bot_logs.json')
    formatter = JsonFormatter("%(asctime)s - [%(levelname)s] - %(name)s - "
                              "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    logHandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl

    return logger