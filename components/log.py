import logging

def log():
    class handler(logging.StreamHandler):
        colors = {
            logging.DEBUG: '\033[37m',
            logging.INFO: '\033[36m',
            logging.WARNING: '\033[33m',
            logging.ERROR: '\033[31m',
            logging.CRITICAL: '\033[101m',
        }
        reset = '\033[0m'
        fmtr = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                                '%m-%d-%Y %H:%M:%S')

        def format(self, record):
            color = self.colors[record.levelno]
            log = self.fmtr.format(record)
            reset = self.reset
            return color + log + reset

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                                '%m-%d-%Y %H:%M:%S')

    file_handler = logging.FileHandler('logs.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(handler())