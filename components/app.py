from logger import logger
from components.data_ingestion import DataIngestion
from components.data_validate import DataValidation
from components.data_versoning import DataVersioning
from components.data_transformation import DataTransformation

def main():
    logger.info("Starting Stock Price Pipeline...")

    data_ingestion = DataIngestion()
    file_path = data_ingestion.fetch_data()

    logger.info(f"Data fetched at: {file_path}")

    data_validation = DataValidation(file_path)
    validated_file_path = data_validation.validate_data(data_validation.df)

    logger.info(f"Validated data saved at: {validated_file_path}")


    data_version = DataVersioning(validated_file_path)
    data_version.version_data()

    logger.info("Pipeline completed successfully.")

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation()

if __name__ == "__main__":
    main()