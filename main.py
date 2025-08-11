from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.exception.exception import LoanapprovalException
from src.logging.logger import logging
from src.entity.config_entity import TrainingPipelineConfig
from src.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
import sys

if __name__ == "__main__":
    try:
        trainig_pipeline_config= TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_congig=trainig_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiating Data Ingestion")
        data_ingestion_artifact =data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion Completed")
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(training_pipeline_congig=trainig_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
        logging.info(f"Initiating Data Validation")
        data_validation_artifact =data_validation.initiate_data_validation()
        logging.info(f"Data Validation Completed")
        print(data_validation_artifact)
        logging.info(f"Data Transformation started")
        data_transformation_config = DataTransformationConfig(training_pipeline_config=trainig_pipeline_config)
        data_transformation=DataTransformation(data_tranformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info(f"Data Transfromation completed")

    except Exception as e:
        raise LoanapprovalException(e,sys)