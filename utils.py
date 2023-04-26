from logging import getLogger, StreamHandler, FileHandler, DEBUG, INFO, Formatter
from colorlog import ColoredFormatter


def getFolderName(raw):
    name = raw.split("\\")[-2]
    if name == "pages":
        name = "index"
    return name


def getFileName(raw):
    name = raw.split("\\")[-1]
    # Remove .php extension
    name = name.split(".")[0]
    return name


logger = getLogger(__name__)
logger.setLevel(DEBUG)

# Define a console handler that logs messages with level INFO or higher
console_handler = StreamHandler()
console_handler.setLevel(INFO)

# Define a color formatter for the console output
color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors={
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "purple",
    },
)

# Set the formatter for the console handler
console_handler.setFormatter(color_formatter)
logger.addHandler(console_handler)

file_formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
# Define a file handler that logs messages with level DEBUG or higher
file_handler = FileHandler("log.txt", mode="w")
file_handler.setLevel(DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
