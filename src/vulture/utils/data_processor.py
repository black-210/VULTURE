"""
VULTURE Data Processor Module
=============================
High-performance data processing utilities for batch operations,
transformations, and data normalization with validation.

Features:
    - Batch data processing
    - Data validation and cleaning
    - Efficient transformations
    - Format conversion
    - Data streaming
    - Error recovery
"""

import numpy as np
import pandas as pd
from typing import Any, List, Dict, Optional, Union, Callable, Tuple
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    """Result of data processing"""
    success: bool
    data: Optional[Any] = None
    errors: List[str] = None
    warnings: List[str] = None
    stats: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.stats is None:
            self.stats = {}


class DataValidator:
    """Data validation and quality checks"""
    
    @staticmethod
    def validate_array(data: Any, expected_dtype: Optional[type] = None,
                      min_value: Optional[float] = None,
                      max_value: Optional[float] = None) -> Tuple[bool, List[str]]:
        """Validate array"""
        errors = []
        
        if not isinstance(data, np.ndarray):
            errors.append("Data must be numpy array")
            return False, errors
        
        if data.size == 0:
            errors.append("Array is empty")
            return False, errors
        
        if expected_dtype and not np.issubdtype(data.dtype, expected_dtype):
            errors.append(f"Expected dtype {expected_dtype}, got {data.dtype}")
        
        if not np.isfinite(data).all():
            errors.append("Array contains NaN or infinity values")
        
        if min_value is not None and np.min(data) < min_value:
            errors.append(f"Array contains values below minimum ({min_value})")
        
        if max_value is not None and np.max(data) > max_value:
            errors.append(f"Array contains values above maximum ({max_value})")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: Optional[List[str]] = None,
                          no_nulls: bool = False) -> Tuple[bool, List[str]]:
        """Validate dataframe"""
        errors = []
        
        if not isinstance(df, pd.DataFrame):
            errors.append("Data must be pandas DataFrame")
            return False, errors
        
        if df.empty:
            errors.append("DataFrame is empty")
            return False, errors
        
        if required_columns:
            missing = set(required_columns) - set(df.columns)
            if missing:
                errors.append(f"Missing columns: {missing}")
        
        if no_nulls and df.isnull().any().any():
            errors.append("DataFrame contains null values")
        
        return len(errors) == 0, errors


class DataCleaner:
    """Data cleaning and preprocessing"""
    
    @staticmethod
    def remove_outliers(data: np.ndarray, method: str = 'iqr',
                       threshold: float = 1.5) -> np.ndarray:
        """Remove outliers"""
        if method == 'iqr':
            Q1 = np.percentile(data, 25)
            Q3 = np.percentile(data, 75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
            return data[(data >= lower) & (data <= upper)]
        
        elif method == 'zscore':
            z_scores = np.abs((data - np.mean(data)) / np.std(data))
            return data[z_scores < threshold]
        
        return data
    
    @staticmethod
    def fill_missing(data: np.ndarray, method: str = 'mean') -> np.ndarray:
        """Fill missing values"""
        mask = np.isnan(data)
        
        if not mask.any():
            return data
        
        if method == 'mean':
            fill_value = np.nanmean(data)
        elif method == 'median':
            fill_value = np.nanmedian(data)
        elif method == 'forward':
            data = pd.Series(data).fillna(method='ffill').values
            return data
        else:
            fill_value = 0
        
        data[mask] = fill_value
        return data
    
    @staticmethod
    def remove_duplicates(data: np.ndarray, tolerance: float = 1e-9) -> np.ndarray:
        """Remove duplicate values"""
        if len(data) == 0:
            return data
        
        sorted_indices = np.argsort(data)
        sorted_data = data[sorted_indices]
        
        mask = np.append([True], np.abs(np.diff(sorted_data)) > tolerance)
        
        return sorted_data[mask]


class DataTransformer:
    """Data transformation operations"""
    
    @staticmethod
    def normalize(data: np.ndarray, method: str = 'minmax') -> np.ndarray:
        """Normalize data"""
        if method == 'minmax':
            min_val = np.min(data)
            max_val = np.max(data)
            if max_val - min_val == 0:
                return np.zeros_like(data)
            return (data - min_val) / (max_val - min_val)
        
        elif method == 'zscore':
            mean = np.mean(data)
            std = np.std(data)
            if std == 0:
                return np.zeros_like(data)
            return (data - mean) / std
        
        elif method == 'log':
            return np.log1p(np.abs(data))
        
        return data
    
    @staticmethod
    def decimate(data: np.ndarray, factor: int) -> np.ndarray:
        """Decimate data"""
        if factor <= 1:
            return data
        
        return data[::factor]
    
    @staticmethod
    def interpolate(data: np.ndarray, new_length: int, method: str = 'linear') -> np.ndarray:
        """Interpolate data"""
        old_indices = np.linspace(0, len(data) - 1, len(data))
        new_indices = np.linspace(0, len(data) - 1, new_length)
        
        return np.interp(new_indices, old_indices, data)
    
    @staticmethod
    def to_complex(real: np.ndarray, imag: np.ndarray) -> np.ndarray:
        """Convert to complex numbers"""
        return real + 1j * imag
    
    @staticmethod
    def to_polar(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Convert to polar coordinates"""
        magnitude = np.abs(data)
        phase = np.angle(data)
        return magnitude, phase


class BatchProcessor:
    """Process data in batches"""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
    
    def process(self, data: Any, processor_func: Callable) -> ProcessingResult:
        """Process data in batches"""
        try:
            if isinstance(data, np.ndarray):
                return self._process_array(data, processor_func)
            elif isinstance(data, pd.DataFrame):
                return self._process_dataframe(data, processor_func)
            else:
                return self._process_list(data, processor_func)
        except Exception as e:
            logger.error(f"Batch processing error: {e}")
            return ProcessingResult(success=False, errors=[str(e)])
    
    def _process_array(self, data: np.ndarray, func: Callable) -> ProcessingResult:
        """Process numpy array in batches"""
        results = []
        errors = []
        
        for i in range(0, len(data), self.batch_size):
            batch = data[i:i + self.batch_size]
            try:
                result = func(batch)
                results.append(result)
            except Exception as e:
                errors.append(f"Batch {i//self.batch_size}: {str(e)}")
        
        if results:
            combined = np.concatenate(results) if isinstance(results[0], np.ndarray) else results
            return ProcessingResult(success=True, data=combined, errors=errors)
        
        return ProcessingResult(success=False, errors=errors)
    
    def _process_dataframe(self, df: pd.DataFrame, func: Callable) -> ProcessingResult:
        """Process dataframe in batches"""
        results = []
        errors = []
        
        for i in range(0, len(df), self.batch_size):
            batch = df.iloc[i:i + self.batch_size]
            try:
                result = func(batch)
                results.append(result)
            except Exception as e:
                errors.append(f"Batch {i//self.batch_size}: {str(e)}")
        
        if results:
            combined = pd.concat(results, ignore_index=True)
            return ProcessingResult(success=True, data=combined, errors=errors)
        
        return ProcessingResult(success=False, errors=errors)
    
    def _process_list(self, data: List, func: Callable) -> ProcessingResult:
        """Process list in batches"""
        results = []
        errors = []
        
        for i in range(0, len(data), self.batch_size):
            batch = data[i:i + self.batch_size]
            try:
                result = func(batch)
                results.append(result)
            except Exception as e:
                errors.append(f"Batch {i//self.batch_size}: {str(e)}")
        
        if results:
            combined = sum(results, []) if isinstance(results[0], list) else results
            return ProcessingResult(success=True, data=combined, errors=errors)
        
        return ProcessingResult(success=False, errors=errors)


class DataPipeline:
    """Composable data processing pipeline"""
    
    def __init__(self):
        self.steps: List[Tuple[str, Callable]] = []
    
    def add_step(self, name: str, func: Callable) -> 'DataPipeline':
        """Add processing step"""
        self.steps.append((name, func))
        return self
    
    def execute(self, data: Any) -> ProcessingResult:
        """Execute pipeline"""
        current_data = data
        warnings = []
        
        for step_name, func in self.steps:
            try:
                logger.info(f"Executing step: {step_name}")
                current_data = func(current_data)
            except Exception as e:
                error_msg = f"Step '{step_name}' failed: {str(e)}"
                logger.error(error_msg)
                return ProcessingResult(success=False, errors=[error_msg])
        
        return ProcessingResult(success=True, data=current_data, warnings=warnings)
