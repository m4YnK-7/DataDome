import logging

# Configure logging with detailed formatting
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("preprocessing.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
