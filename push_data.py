import os
import sys

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL=os.getenv("MOGODB_URL")
print(MONGODB_URL)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from src.logging.logger import logging
from src.exception.exception import LoanapprovalException

class LoanapprovalDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
    def convert_csv_to_dict(self,file_path):
        try:
            df=pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records=df.to_dict(orient='records')
            return records
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_client=pymongo.MongoClient(MONGODB_URL)
            self.db=self.mongo_client[self.database]
            self.collection=self.db[self.collection]
            self.collection.insert_many(self.records)
            logging.info(f"Data inserted to {self.database}.{self.collection} sucessfully")
            return len(self.records)
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH= "loan_approvaldata\loanapproval.csv"
    DATABASE = "JAGA"
    Collection = "LoanapprovalData"
    loanapprovalobj=LoanapprovalDataExtract()
    records=loanapprovalobj.convert_csv_to_dict(file_path=FILE_PATH)
    print(records)
    no_of_records=loanapprovalobj.insert_data_to_mongodb(records=records,database=DATABASE,collection=Collection)
    print(f"Number of records inserted:{no_of_records}")



        
