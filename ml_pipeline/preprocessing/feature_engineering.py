"""
Feature Engineering Module
Advanced feature engineering, selection, and correlation analysis.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Any
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


class FeatureEngineer:
    """Advanced feature engineering and selection."""
    
    @staticmethod
    def correlation_analysis(X: pd.DataFrame, y: pd.Series, top_n: int = 10) -> pd.DataFrame:
        """
        Analyze feature correlation with target variable.
        
        Args:
            X: Feature matrix
            y: Target variable
            top_n: Number of top correlated features to return
            
        Returns:
            DataFrame with feature correlations
        """
        X_with_target = X.copy()
        X_with_target['target'] = y
        
        correlation = X_with_target.corr()['target'].drop('target').abs().sort_values(ascending=False)
        
        print(f"Top {top_n} features by correlation with target:")
        print(correlation.head(top_n))
        
        return correlation.head(top_n)
    
    @staticmethod
    def select_features_kbest(X: pd.DataFrame, y: pd.Series, k: int = 15,
                             score_func=f_classif) -> Tuple[pd.DataFrame, list]:
        """
        Select k best features using SelectKBest.
        
        Args:
            X: Feature matrix
            y: Target variable
            k: Number of features to select
            score_func: Scoring function (f_classif or mutual_info_classif)
            
        Returns:
            DataFrame with selected features and their names
        """
        selector = SelectKBest(score_func=score_func, k=k)
        X_selected = selector.fit_transform(X, y)
        
        selected_features = X.columns[selector.get_support()].tolist()
        print(f"Selected {k} best features: {selected_features}")
        
        scores = pd.DataFrame({
            'feature': X.columns,
            'score': selector.scores_
        }).sort_values('score', ascending=False)
        
        print("\nFeature scores:")
        print(scores)
        
        return pd.DataFrame(X_selected, columns=selected_features), selected_features
    
    @staticmethod
    def pca_analysis(X: pd.DataFrame, n_components: int = None, 
                    variance_threshold: float = 0.95) -> Tuple[np.ndarray, object]:
        """
        Apply PCA for dimensionality reduction.
        
        Args:
            X: Feature matrix
            n_components: Number of components (if None, use variance_threshold)
            variance_threshold: Cumulative variance threshold
            
        Returns:
            Transformed data and PCA object
        """
        if n_components is None:
            pca = PCA(n_components=variance_threshold)
        else:
            pca = PCA(n_components=n_components)
        
        X_pca = pca.fit_transform(X)
        
        print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
        print(f"Cumulative variance: {np.cumsum(pca.explained_variance_ratio_)}")
        print(f"Using {pca.n_components_} components")
        
        return X_pca, pca
    
    @staticmethod
    def get_correlation_matrix(X: pd.DataFrame) -> pd.DataFrame:
        """
        Get correlation matrix between all features.
        
        Args:
            X: Feature matrix
            
        Returns:
            Correlation matrix
        """
        corr_matrix = X.corr()
        return corr_matrix
    
    @staticmethod
    def create_interaction_features(X: pd.DataFrame, 
                                   feature_pairs: list) -> pd.DataFrame:
        """
        Create interaction features between specified feature pairs.
        
        Args:
            X: Feature matrix
            feature_pairs: List of tuples with feature pairs to interact
            
        Returns:
            DataFrame with interaction features added
        """
        X_new = X.copy()
        
        for feat1, feat2 in feature_pairs:
            if feat1 in X.columns and feat2 in X.columns:
                interaction_name = f"{feat1}_x_{feat2}"
                X_new[interaction_name] = X[feat1] * X[feat2]
        
        print(f"Created {len(feature_pairs)} interaction features")
        return X_new
    
    @staticmethod
    def polynomial_features(X: pd.DataFrame, degree: int = 2,
                          selected_features: list = None) -> pd.DataFrame:
        """
        Create polynomial features (e.g., squared, cubed).
        
        Args:
            X: Feature matrix
            degree: Polynomial degree
            selected_features: Features to apply polynomial transformation to
            
        Returns:
            DataFrame with polynomial features added
        """
        X_new = X.copy()
        
        if selected_features is None:
            selected_features = X.columns.tolist()
        
        for col in selected_features:
            if col in X.columns:
                for d in range(2, degree + 1):
                    X_new[f"{col}_{d}"] = X[col] ** d
        
        print(f"Created polynomial features up to degree {degree}")
        return X_new
