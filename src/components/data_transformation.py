import sys,os
from src.exception.exception import LoanapprovalException
from src.logging.logger import logging

from src.constant.training_pipeline import TARGET_COLUMN,SCHEMA_FILE_PATH
from src.entity.artifact_entity import (DataValidationArtifact,DataTransformationArtifact)
from src.entity.config_entity import DataTransformationConfig

import numpy as np
import pandas as pd
from src.utils.main_utils.utils import read_yaml_file,save_numpy_array,save_object

from sklearn.preprocessing import LabelEncoder,StandardScaler,OneHotEncoder,OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator,TransformerMixin

##For label encoding
class Multicolumnlabelencoder(BaseEstimator,TransformerMixin):
    def __init__(self,columns=None):
        self.columns = columns
        self.encoder= {}

    def fit(self,X,y=None):
        X=pd.DataFrame(X)
        for col in self.columns:
            le=LabelEncoder()
            le.fit(X[col].astype(str))
            self.encoder[col]= le
        return self
    
    def transform(self,X):
        X=pd.DataFrame(X).copy()
        for col in self.columns:
            X[col]=self.encoder[col].transform(X[col].astype(str))
        return X

    def inverse_transform(self,X):
        X=pd.DataFrame(X).copy()
        for col in self.columns:
            X[col]=self.encoder[col].inverse_transform(X[col])
        return X



class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_tranformation_config:DataTransformationConfig):
        self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
        self.data_transformation_config:DataTransformationConfig = data_tranformation_config
        self.schema_config= read_yaml_file(file_path=SCHEMA_FILE_PATH)

    @staticmethod
    def read_csv(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
    def get_data_transformer(self)->Pipeline:
        logging.info(f"Enter the get data  tranformer stage")
        try:
            lebl_encod_col = self.schema_config.get('label_encod',[])
            one_ht_encod_col=self.schema_config.get('one_hot_encode',[])
            ord_encod_col=self.schema_config.get('ord_encod',[])
            stand_sclare_col=self.schema_config.get('stand_scaler',[])

            preprocesser = ColumnTransformer(
                transformers=[
                    ("LabelEncoder",Multicolumnlabelencoder(columns=lebl_encod_col),lebl_encod_col),
                    ("OnehotEncoder",OneHotEncoder(),one_ht_encod_col),
                    ("OrdinalEncoder",OrdinalEncoder(),ord_encod_col),
                    ("StandardScaler",StandardScaler(),stand_sclare_col)
                ]
            )

            return preprocesser
        except Exception as e:
            raise LoanapprovalException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info(f"Enter the initiation of data tranformation stage")
        try:
            logging.info(f"Starting Data Transformation")
            train_df=DataTransformation.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df =DataTransformation.read_csv(self.data_validation_artifact.valid_test_file_path)

            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            traget_feature_train_df = train_df[TARGET_COLUMN]
            input_feature_test_df= test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df =test_df[TARGET_COLUMN]

            preprocesser =self.get_data_transformer()
            preprocesser_object=preprocesser.fit(input_features_train_df)
            transformed_train_df = preprocesser_object.transform(input_features_train_df)
            transformed_test_df = preprocesser_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_train_df,np.array(traget_feature_train_df)]
            test_arr = np.c_[transformed_test_df,np.array(target_feature_test_df)]

            save_numpy_array(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path,obj=preprocesser_object,)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=  self.data_transformation_config.transformed_object_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise LoanapprovalException(e,sys)



        


