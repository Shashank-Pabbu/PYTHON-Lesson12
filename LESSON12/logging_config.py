import logging

# Configure logging
logging.basicConfig(
    filename='app.log',             # Log file
    level=logging.DEBUG,            # Log level
    format='%(asctime)s %(levelname)s: %(message)s',
)

# Logger instance
logger = logging.getLogger(__name__)
logger.info("Logging is configured and ready.")
