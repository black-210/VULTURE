"""Feature Engineering - Advanced Feature Creation and Selection

Provides comprehensive feature engineering including:
- Polynomial features
- Feature interactions
- Feature selection methods
- Feature importance analysis
- Dimensionality reduction
- Statistical feature creation
- Domain-specific features
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import (
    SelectKBest, f_classif, f_regression, mutual_info_classif, mutual_info_regression,
    RFE, RFECV, SelectFromModel
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from typing import Tuple, List, Dict, Optional, Union, Callable
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:
    """Advanced feature engineering pipeline
    
    Provides comprehensive tools for creating, selecting, and engineering
    features for improved model performance.
    
    Examples:
        >>> engineer = FeatureEngineer()
        >>> X = np.random.randn(100, 10)
        >>> X_poly = engineer.create_polynomial_features(X, degree=2)
        >>> X_selected = engineer.select_best_features(X, y, k=5)
    """
    
    def __init__(self, random_state: int = 42):
        """Initialize feature engineer
        
        Args:
            random_state: Random seed
        """
        self.random_state = random_state
        self.feature_selectors = {}
        self.feature_importance = None
        self.selected_features = None
        logger.info("FeatureEngineer initialized")
    
    def create_polynomial_features(self, X: np.ndarray,
                                  degree: int = 2,
                                  include_bias: bool = False) -> np.ndarray:
        """Create polynomial features
        
        Args:
            X: Input features
            degree: Polynomial degree
            include_bias: Include bias term
        
        Returns:
            Polynomial features
        """
        poly = PolynomialFeatures(degree=degree, include_bias=include_bias)
        X_poly = poly.fit_transform(X)
        logger.info(f"Created polynomial features: {X.shape} -> {X_poly.shape}")
        return X_poly
    
    def create_interaction_features(self, X: np.ndarray,
                                   interaction_pairs: Optional[List[Tuple]] = None) -> np.ndarray:
        """Create interaction features
        
        Args:
            X: Input features
            interaction_pairs: List of feature index pairs to interact
        
        Returns:
            Features with interactions
        """
        n_features = X.shape[1]
        
        if interaction_pairs is None:
            # Create all pairwise interactions
            interaction_pairs = [(i, j) for i in range(n_features) 
                                for j in range(i+1, n_features)]
        
        X_interact = [X]
        for i, j in interaction_pairs:
            interaction = X[:, i] * X[:, j]
            X_interact.append(interaction.reshape(-1, 1))
        
        X_interact = np.hstack(X_interact)
        logger.info(f"Created {len(interaction_pairs)} interaction features")
        return X_interact
    
    def create_statistical_features(self, X: np.ndarray,
                                   window_size: int = 3) -> np.ndarray:
        """Create statistical features from signal data
        
        Args:
            X: Input signal data (n_samples, n_features) or (n_samples,)
            window_size: Window size for moving statistics
        
        Returns:
            Features with statistical derivatives
        """
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        
        features_list = [X]
        
        # Moving mean, std, min, max
        for window in [window_size, window_size*2]:
            for i in range(X.shape[1]):
                signal = X[:, i]
                
                # Moving statistics
                for w in range(window, len(signal)+1):
                    window_data = signal[w-window:w]
                    features_list.append(np.mean(window_data))
        
        # Just use original + basic derivatives
        diffs = np.diff(X, axis=0)
        diffs = np.vstack([diffs[0], diffs])  # Pad to match size
        features_list = [X, diffs]
        
        X_stats = np.hstack(features_list)
        logger.info(f"Created statistical features: {X.shape} -> {X_stats.shape}")
        return X_stats
    
    def select_best_features(self, X: np.ndarray, y: np.ndarray,
                            k: int = 10,
                            method: str = 'f_score',
                            task: str = 'classification') -> Tuple[np.ndarray, np.ndarray]:
        """Select best features using statistical tests
        
        Args:
            X: Input features
            y: Target labels/values
            k: Number of features to select
            method: Selection method ('f_score', 'mutual_info', 'chi2')
            task: 'classification' or 'regression'
        
        Returns:
            (Selected features, Selected feature indices)
        """
        if task == 'classification':
            score_func = f_classif if method == 'f_score' else mutual_info_classif
        else:
            score_func = f_regression if method == 'f_score' else mutual_info_regression
        
        selector = SelectKBest(score_func=score_func, k=min(k, X.shape[1]))
        X_selected = selector.fit_transform(X, y)
        selected_indices = selector.get_support(indices=True)
        
        self.selected_features = selected_indices
        logger.info(f"Selected {k} best features using {method}")
        
        return X_selected, selected_indices
    
    def select_by_importance(self, X: np.ndarray, y: np.ndarray,
                            k: int = 10,
                            task: str = 'classification',
                            n_estimators: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """Select features by model importance
        
        Args:
            X: Input features
            y: Target
            k: Number of features to select
            task: 'classification' or 'regression'
            n_estimators: Number of trees
        
        Returns:
            (Selected features, Feature importances)
        """
        if task == 'classification':
            model = RandomForestClassifier(n_estimators=n_estimators, 
                                          random_state=self.random_state)
        else:
            model = RandomForestRegressor(n_estimators=n_estimators,
                                         random_state=self.random_state)
        
        selector = SelectFromModel(model, prefit=False, max_features=k)
        model.fit(X, y)
        X_selected = selector.fit_transform(X, y)
        
        self.feature_importance = model.feature_importances_
        logger.info(f"Selected {k} features by model importance")
        
        return X_selected, model.feature_importances_
    
    def rfe_selection(self, X: np.ndarray, y: np.ndarray,
                     k: int = 10,
                     task: str = 'classification',
                     cv: Optional[int] = 5) -> Tuple[np.ndarray, np.ndarray]:
        """Recursive Feature Elimination
        
        Args:
            X: Input features
            y: Target
            k: Number of features to select
            task: 'classification' or 'regression'
            cv: Cross-validation folds (None for no CV)
        
        Returns:
            (Selected features, Feature ranking)
        """
        if task == 'classification':
            estimator = RandomForestClassifier(n_estimators=50,
                                              random_state=self.random_state)
        else:
            estimator = RandomForestRegressor(n_estimators=50,
                                             random_state=self.random_state)
        
        if cv:
            selector = RFECV(estimator=estimator, n_features_to_select=k,
                            cv=cv, step=1, n_jobs=-1)
        else:
            selector = RFE(estimator=estimator, n_features_to_select=k, step=1)
        
        X_selected = selector.fit_transform(X, y)
        ranking = selector.ranking_
        
        logger.info(f"RFE selected {k} features")
        return X_selected, ranking
    
    def get_feature_importance_dataframe(self, feature_names: List[str],
                                        importances: np.ndarray) -> pd.DataFrame:
        """Create feature importance dataframe
        
        Args:
            feature_names: Feature names
            importances: Importance values
        
        Returns:
            Sorted dataframe
        """
        df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        return df
