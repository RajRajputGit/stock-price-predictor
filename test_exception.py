import sys 
from exception.custom_exception import CustomException 
from logger import logger

def test_custom_exception(a,b):
    try:
        result = a/b 
    except Exception as e:
        logger.error("Divide by Zero error occurred", exc_info=True)
        raise CustomException("Error while dividing the number", sys)

test_custom_exception(3,0)