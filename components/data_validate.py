import os
import pandas as pd
from exception.custom_exception import CustomException
from logger import logger
import sys


REQUIRED_COLUMNS = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

DATE_COLUMN = "Date"

MIN_REQUIRED_ROWS = 200   # minimum data points needed for time series

DATE_FREQUENCY = "D"      # Daily data


class DataValidation:
    def __init__(self,file_path: str):
        self.file_path = file_path 
        self.df = pd.read_csv(self.file_path)
        logger.info("Data Validation component initialized.")
    
    def validate_data(self,df: pd.DataFrame):
        try:
            logger.info("Starting data validation.")

            try:
                df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"] # standardize column names
                
                df.drop(index = [0,1], inplace=True)
                
                df = df.reset_index(drop=True)

                df["Date"] = pd.to_datetime(df["Date"])
            
            except Exception as e:
                raise CustomException("Error in standardizing columns or parsing dates.", sys)


            logger.info("All required columns are present.")
            
            #check for missing values
            for col in df.columns:
                if df[col].isnull().sum() == df.shape[0]:
                    raise CustomException(f"Column {col} contains all missing values.", sys)
                logger.info(f"Column {col} has valid data.")

                

            
            # Check for minimum number of rows
            if df.shape[0] < MIN_REQUIRED_ROWS:
                raise CustomException(f"Insufficient data points. Minimum required is {MIN_REQUIRED_ROWS}.", sys)
            logger.info("Sufficient data points available.")
            
            # Check date format and frequency
            df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors='coerce')
            if df[DATE_COLUMN].isnull().sum() > 0:
                raise CustomException("Date column contains invalid date formats.", sys)
            
            df = df.set_index(DATE_COLUMN).asfreq(DATE_FREQUENCY)
            if df.index.isnull().sum() > 0:
                raise CustomException("Date index has missing dates based on expected frequency.", sys)
            logger.info("Date column format and frequency validated.")
            
            logger.info("Data validation completed successfully.")
            os.remove(self.file_path)  # Remove original file after validation
            self.file_path = self.df.to_csv(f"data/{self.file_path.split('/')[-1].replace('.csv', '_validated.csv')}", index=False)
            return self.file_path

        except Exception as e:
            logger.error("Data validation failed.", exc_info=True)
            raise CustomException(str(e), sys) 