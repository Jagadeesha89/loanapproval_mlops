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



"""
Data ingestion related constants start with data_ingestion VAR Name

"""

DATA_INGESTION_COLLECTION_NAME:str = "LoanapprovalData"
DATA_INGESTION_DATABASE_NAME:str = "JAGA"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float = 0.2