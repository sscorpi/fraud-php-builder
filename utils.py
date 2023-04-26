from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO


def getFolderName(raw):
    name = raw.split("\\")[-2]
    if name == "pages":
        name = "index"
    return name


logger = getLogger(__name__)
logger.setLevel(DEBUG)

# Define a console handler that logs messages with level INFO or higher
console_handler = StreamHandler()
console_handler.setLevel(INFO)
formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Define a file handler that logs messages with level DEBUG or higher
file_handler = FileHandler("log.txt", mode="w")
file_handler.setLevel(DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
