"""Data preprocessing: Normalization, augmentation, train/test split."""

import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class Preprocessing:
    """Production-grade data preprocessing."""

    @staticmethod
    def normalize(X: np.ndarray, method: str = 'standard') -> np.ndarray:
        """Normalize data.
        
        Args:
            X: Input data (n_samples, n_features)
            method: 'standard', 'minmax', 'robust'
            
        Returns:
            Normalized data
        """
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return scaler.fit_transform(X)

    @staticmethod
    def remove_outliers(X: np.ndarray, y: np.ndarray = None, 
                       method: str = 'iqr', threshold: float = 1.5) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Remove outliers.
        
        Args:
            X: Input data
            y: Labels (optional)
            method: 'iqr' or 'zscore'
            threshold: Outlier threshold
            
        Returns:
            (cleaned_X, cleaned_y)
        """
        if method == 'iqr':
            Q1 = np.percentile(X, 25, axis=0)
            Q3 = np.percentile(X, 75, axis=0)
            IQR = Q3 - Q1
            mask = np.all((X >= Q1 - threshold * IQR) & (X <= Q3 + threshold * IQR), axis=1)
        else:  # zscore
            from scipy import stats
            mask = np.all(np.abs(stats.zscore(X)) < threshold, axis=1)
        
        X_clean = X[mask]
        y_clean = y[mask] if y is not None else None
        
        logger.info(f"Removed {np.sum(~mask)} outliers ({method})")
        return X_clean, y_clean

    @staticmethod
    def train_test_split(X: np.ndarray, y: np.ndarray, test_size: float = 0.2,
                        random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split data into train/test.
        
        Args:
            X: Features
            y: Labels
            test_size: Test set fraction
            random_state: Random seed
            
        Returns:
            (X_train, X_test, y_train, y_test)
        """
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    @staticmethod
    def augment_data(X: np.ndarray, y: np.ndarray, factor: int = 2,
                    noise_level: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
        """Data augmentation via noise addition.
        
        Args:
            X: Input data
            y: Labels
            factor: Augmentation factor
            noise_level: Noise std relative to signal
            
        Returns:
            (augmented_X, augmented_y)
        """
        X_aug = [X]
        y_aug = [y]
        
        for _ in range(factor - 1):
            noise = np.random.normal(0, noise_level * np.std(X), X.shape)
            X_aug.append(X + noise)
            y_aug.append(y)
        
        return np.vstack(X_aug), np.concatenate(y_aug)

    @staticmethod
    def standardize(X: np.ndarray, mean: np.ndarray = None, 
                   std: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Standardize with stored mean/std.
        
        Args:
            X: Input data
            mean: Precomputed mean (if None, compute)
            std: Precomputed std (if None, compute)
            
        Returns:
            (standardized_X, mean, std)
        """
        if mean is None:
            mean = np.mean(X, axis=0)
        if std is None:
            std = np.std(X, axis=0)
        
        X_std = (X - mean) / (std + 1e-8)
        return X_std, mean, std
