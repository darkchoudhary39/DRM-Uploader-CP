import logging
from logging.handlers import RotatingFileHandler

# Bot Created by @NtrRazYt
logging.basicConfig(
    level=logging.ERROR,  # Change to logging.INFO or logging.DEBUG if needed
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("Assist.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# Set logger level for 'pyrogram' library
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Get the logger instance
logger = logging.getLogger()  # Changed variable name from logging to logger
