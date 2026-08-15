"""Model evaluation: Metrics, ROC, confusion matrix."""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report,
    mean_squared_error, r2_score, mean_absolute_error
)
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class Evaluation:
    """Model evaluation metrics."""

    @staticmethod
    def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray,
                       task: str = 'classification') -> Dict[str, float]:
        """Compute evaluation metrics.
        
        Args:
            y_true: Ground truth
            y_pred: Predictions
            task: 'classification' or 'regression'
            
        Returns:
            Dict of metrics
        """
        if task == 'classification':
            return {
                'accuracy': accuracy_score(y_true, y_pred),
                'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
                'f1': f1_score(y_true, y_pred, average='weighted', zero_division=0),
            }
        else:  # regression
            return {
                'mse': mean_squared_error(y_true, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
                'mae': mean_absolute_error(y_true, y_pred),
                'r2': r2_score(y_true, y_pred),
            }

    @staticmethod
    def get_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """Get confusion matrix.
        
        Args:
            y_true: Ground truth
            y_pred: Predictions
            
        Returns:
            Dict with confusion matrix and derived metrics
        """
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
        
        return {
            'confusion_matrix': cm,
            'true_negative': tn,
            'false_positive': fp,
            'false_negative': fn,
            'true_positive': tp,
            'specificity': tn / (tn + fp) if (tn + fp) > 0 else 0,
            'sensitivity': tp / (tp + fn) if (tp + fn) > 0 else 0,
        }

    @staticmethod
    def get_roc_curve(y_true: np.ndarray, y_scores: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
        """Get ROC curve.
        
        Args:
            y_true: Ground truth (binary)
            y_scores: Prediction scores
            
        Returns:
            (fpr, tpr, auc)
        """
        fpr, tpr, _ = roc_curve(y_true, y_scores)
        auc = roc_auc_score(y_true, y_scores)
        return fpr, tpr, auc

    @staticmethod
    def get_report(y_true: np.ndarray, y_pred: np.ndarray) -> str:
        """Get detailed classification report.
        
        Args:
            y_true: Ground truth
            y_pred: Predictions
            
        Returns:
            Report string
        """
        return classification_report(y_true, y_pred)
