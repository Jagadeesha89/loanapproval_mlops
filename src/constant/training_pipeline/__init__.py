import os
import sys
import numpy as np
import pandas as pd

"""
Defining common constant variables for the training pipeline

"""

TARGET_COLUMN = "loan_status"
PIPELINE_NAME:str = "Loanapproval"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAEM:str = "loan_approval.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH:str = os.path.join('data_schema','schema.yaml')
SAVED_MODEL_DIR:str  = os.path.join("saved_models")
MODEL_FILE_NAME:str = "model.pkl"




"""
Data ingestion related constants start with data_ingestion VAR Name

"""

DATA_INGESTION_COLLECTION_NAME:str = "LoanapprovalData"
DATA_INGESTION_DATABASE_NAME:str = "JAGA"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

"""
Data Validtion related contsants statrt with data_validation VAR Name

"""
DATA_VALIDATION_DIR:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str ="validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "data_drift_repot"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "drift_report.yaml"

"""
Data Tranfromation related constant start with data_transfromation VAR name

"""
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT: str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocesser.pkl"

"""
Model traniner realted constant start with model trainer VAR Name

"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float = 0.05
