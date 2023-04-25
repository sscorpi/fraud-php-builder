import logging


def getFolderName(raw):
    name = raw.split('\\')[-2]
    if name == 'pages':
        name = 'index'
    return name


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define a console handler that logs messages with level INFO or higher
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Define a file handler that logs messages with level DEBUG or higher
file_handler = logging.FileHandler('log.txt', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
