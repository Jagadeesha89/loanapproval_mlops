import os,sys
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from src.exception.exception import LoanapprovalException
from src.logging.logger import logging

from src.utils.main_utils.utils import save_object, load_object,load_numpy_array_data,evaluate_models
from src.utils.ml_utlis.model.estimator import LoanApprovalModel
from src.utils.ml_utlis.metrics.calssification_metrics import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier)
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        self.model_trainer_config=model_trainer_config
        self.data_transformation_artifact=data_transformation_artifact

    def train_model(self,x_train,y_train,x_test,y_test):
        models={
            "Random Forest":RandomForestClassifier(verbose=1),
            "Decision Tree":DecisionTreeClassifier(),
            "Logistic Regression":LogisticRegression(verbose=1),
            "Adaboost Classifier":AdaBoostClassifier(),
            "Gradient Classifier":GradientBoostingClassifier(verbose=1)
        }
        params={
            "Decision Tree":{
                'criterion':['gini', 'entropy', 'log_loss'],
                #'splitter':['best','random'],
                #'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                #'criterion':['gini', 'entropy', 'log_loss'],
                #'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Classifier":{
                #'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                #'criterion':['squared_error', 'friedman_mse'],
                #'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "Adaboost Classifier":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }

        }

        model_report:dict=evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,
                                          models=models,param=params)
        best_model_score=max(sorted(model_report.values()))

        best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        logging.info(f"Trained model {best_model_name} has achived score of {best_model_score}")

        best_model=models[best_model_name]

        y_train_predict=best_model.predict(x_train)
        classification_train_metrics=get_classification_score(y_true=y_train,y_pred=y_train_predict)

        y_test_predict=best_model.predict(x_test)
        classification_test_metrics=get_classification_score(y_true=y_test,y_pred=y_test_predict)

        preprocesser=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        loanapproval_model=LoanApprovalModel(preprocesser=preprocesser,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=loanapproval_model)

        model_trainer_artifact=ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metrics=classification_train_metrics,
            test_metric=classification_test_metrics
        )
        return model_trainer_artifact
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            trainfile_path=self.data_transformation_artifact.transformed_train_file_path
            testfile_path=self.data_transformation_artifact.transformed_test_file_path

            train_array=load_numpy_array_data(trainfile_path)
            test_arry=load_numpy_array_data(testfile_path)

            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_arry[:,:-1],
                test_arry[:,-1]
            )

            model_train_artifact=self.train_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)

            return model_train_artifact
        except Exception as e:
            raise LoanapprovalException(e,sys)





    