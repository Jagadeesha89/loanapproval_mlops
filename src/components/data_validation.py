import os
import sys
from src.exception.exception import LoanapprovalException
from src.logging.logger import logging
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from src.constant.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd
from scipy.stats import ks_2samp
from src.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema =read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            logging.info(f"Reading data from {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
    def validate_data(self,dataframe:pd.DataFrame)->bool:
        try:
            logging.info("Enters data validation methond")
            number_of_columns = len([list(item.keys())[0] for item in self.schema["columns"]])
            logging.info(f"Number of columns required: {number_of_columns}")
            logging.info(f"NUmber of columns in dataframe: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
    def detect_data_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dict = ks_2samp(d1,d2)
                if threshold < is_sample_dict.pvalue:
                    is_found =False
                else:
                    is_found = True
                    status = False
                report.update({
                    column:{
                        "p_value": float(is_sample_dict.pvalue),
                        "drift_status": is_found
                    }
                })

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,content=report)
            logging.info(f"Drift report file saved at {drift_report_file_path}")
        except Exception as e:
            raise LoanapprovalException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info("Started data validation process")
            trained_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            train_dataframe=DataValidation.read_data(file_path=trained_file_path)
            test_dataframe =DataValidation.read_data(file_path=test_file_path)

            status=self.validate_data(train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contains all columns,\n"

            status=self.validate_data(test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contains all columns,\n"
            
            status = self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            logging.info(f"Valid train and test file saved")

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise LoanapprovalException(e,sys)