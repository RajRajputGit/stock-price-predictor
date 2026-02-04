from logger import logger 

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logger.error("An error occurred", exc_info=True)

logger.info("Program completed successfully")