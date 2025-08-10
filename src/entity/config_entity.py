from datetime import datetime
import os
from src.constant import training_pipeline

print(training_pipeline.ARTIFACT_DIR)
print(training_pipeline.PIPELINE_NAME)

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name =training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.arifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestamp:str=timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_congig:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_congig.arifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path =os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                                                   training_pipeline.FILE_NAEM)
        self.training_file_path =os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                              training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                              training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio:float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name =training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name =training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    def __init__(self, training_pipeline_congig:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_congig.arifact_dir,training_pipeline.DATA_VALIDATION_DIR)
        self.valid_data_dir = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path =  os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path = os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path = os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path =os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                   training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,)
