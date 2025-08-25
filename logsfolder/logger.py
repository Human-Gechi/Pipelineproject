import os
import logging

log_dir = os.path.dirname(__file__)  # This resolves to the logs/ folder
log_path = os.path.join(log_dir, 'newslogs.log')

# Setting basic logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path,
    filemode="a",
)
# Creating logger instance
logger = logging.getLogger(__name__)
