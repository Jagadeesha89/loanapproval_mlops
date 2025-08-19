import os
import sys
import numpy as np
import pandas as pd
import pymongo
from src.exception.exception import LoanapprovalException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL =os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def export_collection_as_dataframe(self):
        try:
            logging.info(f"Exporting Collection {self.data_ingestion_config.collection_name} as DataFrame")
        
            database_name=self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection =self.mongo_client[database_name][collection_name]

            df= pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"],inplace=True) 
                df=df[:10000]
            logging.info(f"Successfuly Exported Collection as DataFrame with rows {df.shape[0]} and columns {df.shape[1]}")
            return df
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            features_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(features_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(features_store_file_path,index=False,header=True)
            logging.info(f"Exported DataFrame to Feature store at {features_store_file_path}")
            return dataframe
        except Exception as e:
            raise LoanapprovalException(e,sys)

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set =train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info(f"Train test split done with train set rows {train_set.shape[0]} and test set rows {test_set.shape[0]}")

            dir_path =os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train set and test set")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Train set and Test set expoted sucessfully")

        except Exception as e:
            raise LoanapprovalException(e,sys)

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("started data Ingestion")
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_to_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f'Data Ingestion done sucessfully')
            return data_ingestion_artifact
        except Exception as e:
            raise LoanapprovalException(e,sys)




