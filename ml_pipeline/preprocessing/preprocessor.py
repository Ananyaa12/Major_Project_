"""
Data Preprocessing Module
Handles missing values, outlier detection, feature scaling, and SMOTE.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from typing import Tuple, Dict, Any


class Preprocessor:
    """
    Comprehensive data preprocessing pipeline.
    
    Steps:
    1. Handle missing values
    2. Outlier detection
    3. Feature scaling
    4. SMOTE for class imbalance
    5. Train-test split
    """
    
    def __init__(self, test_size: float = 0.2, random_state: int = 42):
        """
        Initialize the preprocessor.
        
        Args:
            test_size: Proportion of dataset to use as test set
            random_state: Random state for reproducibility
        """
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.X_scaler = None
        self.y_scaler = None
        
    def handle_missing_values(self, X: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            X: Feature matrix
            strategy: 'mean', 'median', or 'drop'
            
        Returns:
            DataFrame with missing values handled
        """
        X = X.copy()
        missing_count = X.isna().sum().sum()
        
        if missing_count == 0:
            print("No missing values detected.")
            return X
        
        print(f"Found {missing_count} missing values.")
        
        if strategy == 'mean':
            X = X.fillna(X.mean())
        elif strategy == 'median':
            X = X.fillna(X.median())
        elif strategy == 'drop':
            X = X.dropna()
        
        print(f"Missing values handled using {strategy} strategy.")
        return X
    
    def detect_outliers_iqr(self, X: pd.DataFrame, multiplier: float = 1.5) -> np.ndarray:
        """
        Detect outliers using Interquartile Range (IQR) method.
        
        Args:
            X: Feature matrix
            multiplier: IQR multiplier for outlier threshold
            
        Returns:
            Boolean array where True indicates an outlier
        """
        Q1 = X.quantile(0.25)
        Q3 = X.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outliers = ((X < lower_bound) | (X > upper_bound)).any(axis=1)
        print(f"Detected {outliers.sum()} outliers using IQR method.")
        
        return outliers
    
    def remove_outliers(self, X: pd.DataFrame, y: pd.Series = None, 
                       multiplier: float = 1.5) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Remove detected outliers from the dataset.
        
        Args:
            X: Feature matrix
            y: Target variable (optional)
            multiplier: IQR multiplier
            
        Returns:
            Cleaned X and y (if provided)
        """
        outlier_mask = self.detect_outliers_iqr(X, multiplier)
        X_clean = X[~outlier_mask].reset_index(drop=True)
        
        if y is not None:
            y_clean = y[~outlier_mask].reset_index(drop=True)
            print(f"Removed {outlier_mask.sum()} outlier rows.")
            return X_clean, y_clean
        
        return X_clean, None
    
    def scale_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame = None,
                      method: str = 'standard') -> Tuple[np.ndarray, np.ndarray]:
        """
        Scale features using StandardScaler or MinMaxScaler.
        
        Args:
            X_train: Training feature matrix
            X_test: Test feature matrix (optional)
            method: 'standard' or 'minmax'
            
        Returns:
            Scaled X_train and X_test (if provided)
        """
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled, None
    
    def apply_smote(self, X_train: np.ndarray, y_train: np.ndarray,
                   random_state: int = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply SMOTE to handle class imbalance in training data.
        
        Args:
            X_train: Training feature matrix
            y_train: Training target variable
            random_state: Random state for reproducibility
            
        Returns:
            Balanced X_train and y_train
        """
        if random_state is None:
            random_state = self.random_state
        
        print(f"Class distribution before SMOTE: {np.bincount(y_train.astype(int))}")
        
        smote = SMOTE(random_state=random_state, k_neighbors=5)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        
        print(f"Class distribution after SMOTE: {np.bincount(y_train_balanced.astype(int))}")
        
        return X_train_balanced, y_train_balanced
    
    def preprocess(self, X: pd.DataFrame, y: pd.Series, 
                  apply_smote: bool = True, remove_outliers_flag: bool = True,
                  scale_method: str = 'standard') -> Dict[str, Any]:
        """
        Complete preprocessing pipeline.
        
        Args:
            X: Feature matrix
            y: Target variable
            apply_smote: Whether to apply SMOTE
            remove_outliers_flag: Whether to remove outliers
            scale_method: Scaling method to use
            
        Returns:
            Dictionary with train and test sets
        """
        # Handle missing values
        X = self.handle_missing_values(X)
        
        # Remove outliers if requested
        if remove_outliers_flag:
            X, y = self.remove_outliers(X, y)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y
        )
        
        print(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
        
        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test, scale_method)
        
        # Apply SMOTE if requested
        if apply_smote:
            X_train_scaled, y_train = self.apply_smote(X_train_scaled, y_train.values)
        else:
            y_train = y_train.values
        
        y_test = y_test.values
        
        return {
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train,
            'y_test': y_test,
            'X_train_orig': X_train,
            'X_test_orig': X_test,
            'feature_names': X_train.columns.tolist(),
            'scaler': self.scaler,
        }
