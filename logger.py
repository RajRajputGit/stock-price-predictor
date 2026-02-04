# Step 1: Import required modules
import logging
import os
from datetime import datetime

# Step 2: Get current date and time
current_date = datetime.now().strftime("%Y-%m-%d")     # e.g. 2026-02-04
current_time = datetime.now().strftime("%H-%M-%S")     # e.g. 14-32-10

# Step 3: Create date-wise log directory
LOG_DIR = os.path.join("logs", current_date)
os.makedirs(LOG_DIR, exist_ok=True)

# Step 4: Create unique log file per execution
LOG_FILE = f"app_{current_time}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Step 5: Create logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Step 6: Prevent duplicate handlers
if not logger.handlers:

    # Step 7: Create file handler
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)

    # Step 8: Create log format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Step 9: Attach formatter to handler
    file_handler.setFormatter(formatter)

    # Step 10: Attach handler to logger
    logger.addHandler(file_handler)
