"""
SHAP Explainability Module
Provides SHAP-based explanations for model predictions.
"""

import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple


class SHAPExplainer:
    """Generate SHAP-based explanations for model predictions."""
    
    def __init__(self, model, X_train: np.ndarray, feature_names: list):
        """
        Initialize SHAP explainer.
        
        Args:
            model: Trained model
            X_train: Training data for background
            feature_names: List of feature names
        """
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        self.explainer = None
        self.shap_values = None
        
    def create_explainer(self, explainer_type: str = 'tree') -> shap.Explainer:
        """
        Create a SHAP explainer based on model type.
        
        Args:
            explainer_type: Type of explainer ('tree', 'kernel', 'gradient')
            
        Returns:
            SHAP explainer object
        """
        try:
            # Try to use TreeExplainer for tree-based models
            self.explainer = shap.TreeExplainer(self.model)
            print("Created TreeExplainer")
        except:
            try:
                # Fallback to KernelExplainer for other models
                self.explainer = shap.KernelExplainer(
                    self.model.predict_proba, 
                    shap.sample(self.X_train, 100)
                )
                print("Created KernelExplainer")
            except:
                # Use permutation explainer as last resort
                self.explainer = shap.Explainer(self.model)
                print("Created Explainer (default)")
        
        return self.explainer
    
    def get_global_explanations(self, X: np.ndarray, max_display: int = 10) -> np.ndarray:
        """
        Get global SHAP explanations (feature importance).
        
        Args:
            X: Data to explain
            max_display: Maximum features to display
            
        Returns:
            SHAP values
        """
        if self.explainer is None:
            self.create_explainer()
        
        self.shap_values = self.explainer.shap_values(X)
        
        # For multi-class, take mean across classes
        if isinstance(self.shap_values, list):
            shap_values_mean = np.mean(np.abs(self.shap_values), axis=0).mean(axis=0)
        else:
            shap_values_mean = np.abs(self.shap_values).mean(axis=0)
        
        return shap_values_mean
    
    def get_feature_importance(self, X: np.ndarray, top_n: int = 10) -> pd.DataFrame:
        """
        Get feature importance ranking based on SHAP values.
        
        Args:
            X: Data to explain
            top_n: Number of top features to return
            
        Returns:
            DataFrame with feature importance
        """
        shap_values = self.get_global_explanations(X)
        
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': shap_values
        }).sort_values('Importance', ascending=False)
        
        print(f"Top {top_n} important features:")
        print(importance_df.head(top_n).to_string(index=False))
        
        return importance_df.head(top_n)
    
    def explain_prediction(self, X_sample: np.ndarray, sample_index: int = 0) -> Dict[str, Any]:
        """
        Explain a single prediction using SHAP.
        
        Args:
            X_sample: Sample data containing the instance to explain
            sample_index: Index of the instance to explain
            
        Returns:
            Dictionary with explanation details
        """
        if self.explainer is None:
            self.create_explainer()
        
        shap_values = self.explainer.shap_values(X_sample)
        
        # Handle multi-class case
        if isinstance(shap_values, list):
            # For multi-class, explain the prediction class
            prediction = self.model.predict(X_sample[sample_index:sample_index+1])[0]
            shap_values_instance = shap_values[int(prediction)][sample_index]
        else:
            shap_values_instance = shap_values[sample_index]
        
        # Get base value
        if isinstance(self.explainer.expected_value, list):
            base_value = self.explainer.expected_value[0]
        else:
            base_value = self.explainer.expected_value
        
        # Create feature contribution data
        feature_contributions = pd.DataFrame({
            'Feature': self.feature_names,
            'Value': X_sample[sample_index],
            'SHAP Value': shap_values_instance,
            'Abs SHAP Value': np.abs(shap_values_instance)
        }).sort_values('Abs SHAP Value', ascending=False)
        
        return {
            'base_value': base_value,
            'feature_contributions': feature_contributions,
            'prediction': self.model.predict(X_sample[sample_index:sample_index+1])[0],
            'prediction_proba': self.model.predict_proba(X_sample[sample_index:sample_index+1])[0],
        }
    
    def create_summary_plot(self, X: np.ndarray, save_path: str = None):
        """
        Create SHAP summary plot.
        
        Args:
            X: Data to explain
            save_path: Path to save the plot
        """
        if self.shap_values is None:
            self.get_global_explanations(X)
        
        plt.figure(figsize=(10, 8))
        
        if isinstance(self.shap_values, list):
            shap_values = self.shap_values[0]
        else:
            shap_values = self.shap_values
        
        shap.summary_plot(shap_values, X, feature_names=self.feature_names, show=False)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Summary plot saved to {save_path}")
        
        plt.close()
    
    def create_waterfall_plot(self, X_sample: np.ndarray, sample_index: int = 0, 
                             save_path: str = None):
        """
        Create SHAP waterfall plot for a single prediction.
        
        Args:
            X_sample: Sample data
            sample_index: Index of instance to explain
            save_path: Path to save the plot
        """
        if self.explainer is None:
            self.create_explainer()
        
        shap_values = self.explainer.shap_values(X_sample)
        
        if isinstance(shap_values, list):
            prediction = self.model.predict(X_sample[sample_index:sample_index+1])[0]
            shap_values_instance = shap_values[int(prediction)]
        else:
            shap_values_instance = shap_values
        
        plt.figure(figsize=(10, 6))
        shap.plots._waterfall.waterfall_legacy(
            self.explainer.expected_value[0] if isinstance(self.explainer.expected_value, list) else self.explainer.expected_value,
            shap_values_instance[sample_index],
            X_sample[sample_index],
            feature_names=self.feature_names,
            show=False
        )
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Waterfall plot saved to {save_path}")
        
        plt.close()
    
    def create_force_plot(self, X_sample: np.ndarray, sample_index: int = 0):
        """
        Create SHAP force plot for a single prediction.
        
        Args:
            X_sample: Sample data
            sample_index: Index of instance to explain
        """
        if self.explainer is None:
            self.create_explainer()
        
        shap_values = self.explainer.shap_values(X_sample)
        
        if isinstance(shap_values, list):
            prediction = self.model.predict(X_sample[sample_index:sample_index+1])[0]
            shap_values_instance = shap_values[int(prediction)]
        else:
            shap_values_instance = shap_values
        
        return shap.force_plot(
            self.explainer.expected_value[0] if isinstance(self.explainer.expected_value, list) else self.explainer.expected_value,
            shap_values_instance[sample_index],
            X_sample[sample_index],
            feature_names=self.feature_names,
            matplotlib=False
        )
    
    def create_dependence_plot(self, X: np.ndarray, feature_name: str, save_path: str = None):
        """
        Create SHAP dependence plot for a feature.
        
        Args:
            X: Data to explain
            feature_name: Feature to plot
            save_path: Path to save the plot
        """
        if self.shap_values is None:
            self.get_global_explanations(X)
        
        if feature_name not in self.feature_names:
            raise ValueError(f"Feature {feature_name} not found in features")
        
        feature_idx = self.feature_names.index(feature_name)
        
        plt.figure(figsize=(10, 6))
        
        if isinstance(self.shap_values, list):
            shap_values = self.shap_values[0]
        else:
            shap_values = self.shap_values
        
        shap.dependence_plot(feature_idx, shap_values, X, 
                            feature_names=self.feature_names, show=False)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Dependence plot saved to {save_path}")
        
        plt.close()
    
    def get_prediction_explanation(self, X_sample: np.ndarray, 
                                  prediction_class: int) -> Dict[str, Any]:
        """
        Get detailed explanation for a prediction.
        
        Args:
            X_sample: Single sample (1D array or DataFrame row)
            prediction_class: Class predicted
            
        Returns:
            Dictionary with explanation
        """
        explanation = self.explain_prediction(X_sample.reshape(1, -1), sample_index=0)
        
        top_contributing = explanation['feature_contributions'].head(5)
        
        return {
            'prediction': explanation['prediction'],
            'prediction_proba': explanation['prediction_proba'].tolist(),
            'base_value': float(explanation['base_value']),
            'top_contributing_features': top_contributing.to_dict('records'),
        }
