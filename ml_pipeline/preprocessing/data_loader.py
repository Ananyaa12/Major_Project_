"""
Data Loader Module
Handles loading and basic exploration of the BRFSS 2015 diabetes dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple


class DataLoader:
    """Load and explore the BRFSS diabetes dataset."""
    
    def __init__(self, csv_path: str):
        """
        Initialize the DataLoader.
        
        Args:
            csv_path: Path to the diabetes CSV file
        """
        self.csv_path = Path(csv_path)
        self.df = None
        self.feature_columns = None
        self.target_column = 'Diabetes_012'
        
    def load_data(self) -> pd.DataFrame:
        """
        Load the CSV dataset.
        
        Returns:
            DataFrame with all data
        """
        self.df = pd.read_csv(self.csv_path)
        print(f"Dataset loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        print(f"Target distribution:\n{self.df[self.target_column].value_counts().sort_index()}")
        return self.df
    
    def get_feature_columns(self) -> list:
        """Get all feature column names (excluding target)."""
        if self.feature_columns is None:
            self.feature_columns = [col for col in self.df.columns 
                                   if col != self.target_column]
        return self.feature_columns
    
    def get_X_y(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Get features and target separately.
        
        Returns:
            Tuple of (X features DataFrame, y target Series)
        """
        X = self.df[self.get_feature_columns()]
        y = self.df[self.target_column]
        return X, y
    
    def get_data_info(self) -> dict:
        """Get comprehensive dataset information."""
        X, y = self.get_X_y()
        return {
            'shape': self.df.shape,
            'n_features': len(self.get_feature_columns()),
            'n_samples': len(self.df),
            'target_classes': sorted(y.unique()),
            'class_distribution': y.value_counts().to_dict(),
            'missing_values': self.df.isna().sum().sum(),
            'feature_dtypes': X.dtypes.to_dict(),
        }
