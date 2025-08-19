from src.entity.artifact_entity import ClassificationMetricArtifact
from src.exception.exception import LoanapprovalException
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
import sys,os

def get_classification_score(y_true,y_pred):
    try:
        model_f1_score = f1_score(y_true,y_pred)
        model_accuracy_score = accuracy_score(y_true,y_pred)
        model_precision_score =precision_score(y_true,y_pred)
        model_recall_score= recall_score(y_true,y_pred)

        classification_metric=ClassificationMetricArtifact(
            f1score=model_f1_score,
            accuracy_score= model_accuracy_score,
            recall_score = model_recall_score,
            precision_score= model_precision_score
        )

        return classification_metric
    except Exception as e:
        raise LoanapprovalException(e,sys)