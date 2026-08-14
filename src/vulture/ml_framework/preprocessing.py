"""Data preprocessing for ML."""
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging
logger = logging.getLogger(__name__)
class Preprocessing:
    @staticmethod
    def normalize(data, method='standard'):
        if method == 'standard':
            scaler = StandardScaler()
            return scaler.fit_transform(data.reshape(-1, 1)).flatten()
        elif method == 'minmax':
            scaler = MinMaxScaler()
            return scaler.fit_transform(data.reshape(-1, 1)).flatten()
        return data
    @staticmethod
    def remove_outliers(data, threshold=3):
        mean, std = np.mean(data), np.std(data)
        mask = np.abs(data - mean) < threshold * std
        return data[mask]
    @staticmethod
    def split_data(X, y, test_size=0.2, random_state=42):
        from sklearn.model_selection import train_test_split
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    @staticmethod
    def augment_data(data, num_augmentations=5):
        augmented = [data]
        for _ in range(num_augmentations):
            noise = np.random.normal(0, 0.01, data.shape)
            augmented.append(data + noise)
        return np.vstack(augmented)