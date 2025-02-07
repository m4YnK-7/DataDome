import logging
from datetime import datetime
import os

# Ensure the log directory exists
os.makedirs("log", exist_ok=True)

# Get the current date and time in the desired format
date_time = datetime.now().strftime("%m-%d_%H-%M-%S")

# Configure logging with detailed formatting and dynamic filename
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"log\\log_{date_time}.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
