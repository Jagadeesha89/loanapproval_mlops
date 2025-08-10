import yaml
from src.exception.exception import LoanapprovalException
from src.logging.logger  import logging
import os,sys
import pandas as pd
import pickle
from sklearn.metrics import f1_score,accuracy_score,recall_score,precision_score
from sklearn.model_selection import GridSearchCV

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise LoanapprovalException(e,sys)
    
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise LoanapprovalException(e,sys)