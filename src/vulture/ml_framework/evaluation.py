"""Model evaluation metrics."""
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, roc_curve
import logging
logger = logging.getLogger(__name__)
class ModelEvaluation:
    @staticmethod
    def evaluate_classification(y_true, y_pred, y_proba=None):
        results = {'accuracy': accuracy_score(y_true, y_pred), 'precision': precision_score(y_true, y_pred, average='weighted'), 'recall': recall_score(y_true, y_pred, average='weighted'), 'f1': f1_score(y_true, y_pred, average='weighted')}
        if y_proba is not None:
            results['auc'] = roc_auc_score(y_true, y_proba, multi_class='ovr')
        return results
    @staticmethod
    def get_confusion_matrix(y_true, y_pred):
        return confusion_matrix(y_true, y_pred)
    @staticmethod
    def get_roc_curve(y_true, y_proba):
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        return fpr, tpr
    @staticmethod
    def evaluate_regression(y_true, y_pred):
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        return {'mse': mean_squared_error(y_true, y_pred), 'mae': mean_absolute_error(y_true, y_pred), 'r2': r2_score(y_true, y_pred)}