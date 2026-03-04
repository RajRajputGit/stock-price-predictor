import os
import subprocess
import sys
import pathlib
from logger import logger
from exception.custom_exception import CustomException


class DataVersioning:
    """
    This class handles data versioning using DVC.
    It does NOT process data.
    It only tells DVC what to track and when.
    """

    def __init__(self, data_path: str):
        """
        data_path: path of data folder or file to be tracked
        Example: data/ or data/AAPL_stockdata_validated.csv
        """
        self.data_path = data_path

    def run_command(self, command: str):
        """
        Utility method to run shell commands safely
        """
        try:
            logger.info(f"Running command: {command}")
            subprocess.run(command, shell=True, check=True, cwd=os.getcwd())
        except Exception as e:
            raise CustomException(e)

    def version_data(self):

        logger.info(f"Starting data versioning for: {self.data_path}")
        """
        Core method that versions data using DVC
        """
        
        try:
            # Step 1: Add data to DVC
            self.run_command(f"dvc add {self.data_path}")

            # Step 2: Git add the generated .dvc file
            self.run_command("git add .")

            # Step 3: Commit data version
            self.run_command(
                f'git commit -m "Data versioned for {self.data_path}"'
            )

            # Step 4: Push data to DVC remote
            self.run_command("dvc push")

            logger.info("Data versioning completed successfully.")

        except Exception as e:
            raise CustomException(str(e) , sys)
