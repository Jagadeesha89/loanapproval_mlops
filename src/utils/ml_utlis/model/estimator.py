from src.exception.exception import LoanapprovalException
from src.logging.logger import logging

import sys,os

from src.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

class LoanApprovalModel:
    def __init__(self,preprocesser,model):
        try:
            self.preprocesser = preprocesser
            self.model = model
        except Exception as e:
            raise LoanapprovalException(e,sys)

    def predict(self,x):
        try:
            x_transform=self.preprocesser(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise LoanapprovalException(e,sys)