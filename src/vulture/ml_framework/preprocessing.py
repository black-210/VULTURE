"""Data Preprocessing - Comprehensive Data Preparation Pipeline

Provides comprehensive data preprocessing including:
- Missing value imputation
- Outlier detection and removal
- Scaling and normalization
- Encoding categorical variables
- Train/test splitting
- Cross-validation setup
- Data augmentation
- Handling imbalanced datasets
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler, QuantileTransformer,
    LabelEncoder, OneHotEncoder, OrdinalEncoder
)
from sklearn.model_selection import (
    train_test_split, cross_val_split, StratifiedKFold, KFold, TimeSeriesSplit
)
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.utils import resample
from typing import Tuple, List, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Comprehensive data preprocessing pipeline
    
    This class provides a complete suite of preprocessing operations
    for preparing raw data for machine learning models.
    
    Examples:
        >>> preprocessor = DataPreprocessor()
        >>> df = pd.read_csv('data.csv')
        >>> df_clean = preprocessor.handle_missing_values(df, strategy='mean')
        >>> df_scaled = preprocessor.scale_features(df_clean, method='standard')
    """
    
    def __init__(self, random_state: int = 42):
        """Initialize preprocessor
        
        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        self.feature_names = None
        self.categorical_features = []
        self.numerical_features = []
        logger.info("DataPreprocessor initialized")
    
    def handle_missing_values(self, data: Union[pd.DataFrame, np.ndarray],
                             strategy: str = 'mean',
                             threshold: float = 0.5) -> Union[pd.DataFrame, np.ndarray]:
        """Handle missing values in dataset
        
        Removes features with missing percentage > threshold and imputes
        remaining missing values using specified strategy.
        
        Args:
            data: Input data
            strategy: Imputation strategy ('mean', 'median', 'mode', 'forward_fill', 'knn')
            threshold: Maximum missing value percentage to keep feature
        
        Returns:
            Data with missing values handled
        
        Raises:
            ValueError: If strategy is invalid
        """
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)
        
        # Remove features with too many missing values
        missing_pct = data.isnull().sum() / len(data)
        cols_to_drop = missing_pct[missing_pct > threshold].index
        data = data.drop(cols_to_drop, axis=1)
        
        logger.info(f"Dropped {len(cols_to_drop)} features with >{threshold*100}% missing")
        
        if strategy == 'mean':
            imputer = SimpleImputer(strategy='mean')
        elif strategy == 'median':
            imputer = SimpleImputer(strategy='median')
        elif strategy == 'mode':
            imputer = SimpleImputer(strategy='most_frequent')
        elif strategy == 'forward_fill':
            return data.fillna(method='ffill').fillna(method='bfill')
        elif strategy == 'knn':
            imputer = KNNImputer(n_neighbors=5)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        # Apply imputation
        data_imputed = pd.DataFrame(
            imputer.fit_transform(data),
            columns=data.columns,
            index=data.index
        )
        
        self.imputers['default'] = imputer
        logger.info(f"Missing values handled using {strategy} strategy")
        
        return data_imputed
    
    def detect_outliers(self, data: Union[pd.DataFrame, np.ndarray],
                       method: str = 'iqr',
                       threshold: float = 3.0) -> Tuple[np.ndarray, np.ndarray]:
        """Detect outliers in dataset
        
        Supports multiple outlier detection methods including IQR,
        Z-score, and isolation forest approaches.
        
        Args:
            data: Input data
            method: Detection method ('iqr', 'zscore', 'mad', 'isolation_forest')
            threshold: Threshold for outlier detection
        
        Returns:
            (Outlier mask, Outlier indices)
        """
        if isinstance(data, pd.DataFrame):
            data_np = data.values
        else:
            data_np = data
        
        if method == 'iqr':
            Q1 = np.percentile(data_np, 25, axis=0)
            Q3 = np.percentile(data_np, 75, axis=0)
            IQR = Q3 - Q1
            outlier_mask = ((data_np < Q1 - 1.5 * IQR) | (data_np > Q3 + 1.5 * IQR)).any(axis=1)
        
        elif method == 'zscore':
            z_scores = np.abs((data_np - np.mean(data_np, axis=0)) / (np.std(data_np, axis=0) + 1e-10))
            outlier_mask = (z_scores > threshold).any(axis=1)
        
        elif method == 'mad':
            # Median Absolute Deviation
            median = np.median(data_np, axis=0)
            mad = np.median(np.abs(data_np - median), axis=0)
            modified_z = 0.6745 * (data_np - median) / (mad + 1e-10)
            outlier_mask = (np.abs(modified_z) > threshold).any(axis=1)
        
        elif method == 'isolation_forest':
            from sklearn.ensemble import IsolationForest
            iso_forest = IsolationForest(contamination=0.1, random_state=self.random_state)
            outlier_mask = iso_forest.fit_predict(data_np) == -1
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        outlier_indices = np.where(outlier_mask)[0]
        logger.info(f"Detected {len(outlier_indices)} outliers using {method}")
        
        return outlier_mask, outlier_indices
    
    def remove_outliers(self, data: Union[pd.DataFrame, np.ndarray],
                       method: str = 'iqr',
                       threshold: float = 3.0) -> Union[pd.DataFrame, np.ndarray]:
        """Remove outliers from dataset
        
        Args:
            data: Input data
            method: Detection method
            threshold: Threshold for detection
        
        Returns:
            Data without outliers
        """
        outlier_mask, indices = self.detect_outliers(data, method, threshold)
        
        if isinstance(data, pd.DataFrame):
            return data[~outlier_mask]
        else:
            return data[~outlier_mask]
    
    def scale_features(self, data: Union[pd.DataFrame, np.ndarray],
                      method: str = 'standard',
                      columns: Optional[List[str]] = None) -> Union[pd.DataFrame, np.ndarray]:
        """Scale/normalize features
        
        Supports multiple scaling methods for feature normalization.
        
        Args:
            data: Input data
            method: Scaling method ('standard', 'minmax', 'robust', 'quantile')
            columns: Specific columns to scale
        
        Returns:
            Scaled data
        
        Raises:
            ValueError: If method is invalid
        """
        is_dataframe = isinstance(data, pd.DataFrame)
        
        if is_dataframe:
            if columns is None:
                columns = data.columns.tolist()
            data_to_scale = data[columns].values
            data_other = data.drop(columns, axis=1) if len(data.columns) > len(columns) else None
        else:
            data_to_scale = data
            data_other = None
        
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        elif method == 'quantile':
            scaler = QuantileTransformer(output_distribution='normal')
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        data_scaled = scaler.fit_transform(data_to_scale)
        self.scalers[method] = scaler
        
        if is_dataframe:
            result = pd.DataFrame(data_scaled, columns=columns, index=data.index)
            if data_other is not None:
                result = pd.concat([result, data_other], axis=1)
            logger.info(f"Scaled {len(columns)} features using {method}")
            return result
        else:
            logger.info(f"Scaled {data.shape[1]} features using {method}")
            return data_scaled
    
    def encode_categorical(self, data: pd.DataFrame,
                          method: str = 'onehot',
                          columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Encode categorical variables
        
        Args:
            data: Input dataframe
            method: Encoding method ('onehot', 'ordinal', 'label')
            columns: Categorical columns to encode
        
        Returns:
            Data with encoded categorical features
        """
        if columns is None:
            columns = data.select_dtypes(include=['object']).columns.tolist()
        
        data_encoded = data.copy()
        
        if method == 'onehot':
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            encoded = encoder.fit_transform(data_encoded[columns])
            feature_names = encoder.get_feature_names_out(columns)
            data_encoded = data_encoded.drop(columns, axis=1)
            encoded_df = pd.DataFrame(encoded, columns=feature_names, index=data.index)
            data_encoded = pd.concat([data_encoded, encoded_df], axis=1)
        
        elif method == 'ordinal':
            encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
            data_encoded[columns] = encoder.fit_transform(data_encoded[columns])
        
        elif method == 'label':
            for col in columns:
                le = LabelEncoder()
                data_encoded[col] = le.fit_transform(data_encoded[col].astype(str))
                self.encoders[col] = le
        
        logger.info(f"Encoded {len(columns)} categorical features using {method}")
        return data_encoded
    
    def split_data(self, X: np.ndarray, y: np.ndarray,
                  test_size: float = 0.2,
                  stratify: bool = True,
                  shuffle: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split data into train and test sets
        
        Args:
            X: Features
            y: Labels
            test_size: Test set size ratio
            stratify: Use stratified split for classification
            shuffle: Shuffle data before split
        
        Returns:
            (X_train, X_test, y_train, y_test)
        """
        stratify_arg = y if stratify else None
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            stratify=stratify_arg,
            shuffle=shuffle,
            random_state=self.random_state
        )
        
        logger.info(f"Split data: {len(X_train)} train, {len(X_test)} test")
        return X_train, X_test, y_train, y_test
    
    def create_cross_validation_folds(self, n_samples: int,
                                     n_splits: int = 5,
                                     stratified: bool = True,
                                     y: Optional[np.ndarray] = None) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Create cross-validation folds
        
        Args:
            n_samples: Number of samples
            n_splits: Number of folds
            stratified: Use stratified k-fold
            y: Labels for stratification
        
        Returns:
            List of (train_indices, test_indices) tuples
        """
        if stratified and y is not None:
            cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)
            folds = list(cv.split(np.zeros(n_samples), y))
        else:
            cv = KFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)
            folds = list(cv.split(np.zeros(n_samples)))
        
        logger.info(f"Created {n_splits} cross-validation folds")
        return folds
    
    def handle_class_imbalance(self, X: np.ndarray, y: np.ndarray,
                              method: str = 'oversample') -> Tuple[np.ndarray, np.ndarray]:
        """Handle class imbalance
        
        Args:
            X: Features
            y: Labels
            method: Method to handle imbalance ('oversample', 'undersample', 'smote')
        
        Returns:
            (Balanced X, Balanced y)
        """
        unique_classes, class_counts = np.unique(y, return_counts=True)
        max_count = np.max(class_counts)
        
        X_balanced = []
        y_balanced = []
        
        if method == 'oversample':
            for cls in unique_classes:
                cls_indices = np.where(y == cls)[0]
                X_cls = X[cls_indices]
                y_cls = y[cls_indices]
                
                if len(cls_indices) < max_count:
                    indices = resample(cls_indices, n_samples=max_count, random_state=self.random_state)
                    X_cls = X[indices]
                    y_cls = y[indices]
                
                X_balanced.append(X_cls)
                y_balanced.append(y_cls)
        
        elif method == 'undersample':
            min_count = np.min(class_counts)
            for cls in unique_classes:
                cls_indices = np.where(y == cls)[0]
                indices = resample(cls_indices, n_samples=min_count, random_state=self.random_state)
                X_balanced.append(X[indices])
                y_balanced.append(y[indices])
        
        elif method == 'smote':
            from imblearn.over_sampling import SMOTE
            smote = SMOTE(random_state=self.random_state)
            X_balanced, y_balanced = smote.fit_resample(X, y)
            return X_balanced, y_balanced
        
        X_balanced = np.vstack(X_balanced)
        y_balanced = np.hstack(y_balanced)
        
        logger.info(f"Balanced dataset using {method}: new size {len(X_balanced)}")
        return X_balanced, y_balanced
    
    def get_feature_statistics(self, data: Union[pd.DataFrame, np.ndarray]) -> Dict:
        """Get comprehensive feature statistics
        
        Args:
            data: Input data
        
        Returns:
            Dictionary of statistics
        """
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)
        
        stats = {
            'shape': data.shape,
            'missing_values': data.isnull().sum().to_dict(),
            'dtypes': data.dtypes.to_dict(),
            'numeric_stats': data.describe().to_dict(),
            'categorical_counts': {col: data[col].value_counts().to_dict() 
                                   for col in data.select_dtypes(include=['object']).columns}
        }
        
        return stats
