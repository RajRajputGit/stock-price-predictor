import yfinance as yf
import numpy as np
import pandas as pd 
import os 
from datetime import datetime
from logger import logger
from components.data_validate import DataValidation

class DataIngestionConfig:
    def __init__(self):
        self.stock_symbol = input("Enter Stock Ticker Symbol (e.g., AAPL for Apple Inc.): ")
        self.start_date = datetime.strptime(input("Enter Start Date (DD-MM-YYYY): "), "%d-%m-%Y")
        self.end_date = datetime.strptime(input("Enter End Date (DD-MM-YYYY): "), "%d-%m-%Y")
        os.makedirs("data",exist_ok=True)

class DataIngestion:

    def __init__(self):
        logger.info("Data Ingestion component initialized.")
        self.config = DataIngestionConfig()

    def fetch_data(self) -> str : 
        logger.info("Fetching stock data for symbol {0} from date {1} to date {2}".format(self.config.stock_symbol,self.config.start_date,self.config.end_date))

        # data idempotency check - if data already exists delete and re-download to ensure we have the latest data for the specified date range

        validated_path = f"data/{self.config.stock_symbol}_stockdata_validated.csv"
        
        if os.path.exists(validated_path):
            logger.info(f"Old validated data found. Deleting for idempotency: {validated_path}")
            os.remove(validated_path)

        df = yf.download(self.config.stock_symbol,start=self.config.start_date,end=self.config.end_date)
        df.to_csv(f"data/{self.config.stock_symbol}_stockdata.csv")
    
        return f"data/{self.config.stock_symbol}_stockdata.csv"


if __name__ == "__main__":
    data_ingestion = DataIngestion()
    file_path = data_ingestion.fetch_data()

    data_validation = DataValidation(file_path)
    validated_file_path = data_validation.validate_data(data_validation.df)
    logger.info(f"Validated data saved at: {validated_file_path}")
