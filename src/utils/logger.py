import os 
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

os.makedirs(os.path.join(LOG_DIR, 'logs'), exist_ok=True)

logger = logging.getLogger("debate-ai")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, 'logs', 'app.log'),
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding='utf-8'
    )

console_handler = logging.StreamHandler()

formatter = logging.Formatter(  "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)