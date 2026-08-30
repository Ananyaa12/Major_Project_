"""
Fairness Module
Evaluates and mitigates bias across demographic groups.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import Dict, List, Tuple


class FairnessEvaluator:
    """Evaluate fairness metrics across demographic groups."""
    
    # Demographic columns from BRFSS dataset
    DEMOGRAPHIC_COLUMNS = {
        'Sex': {0: 'Female', 1: 'Male'},
        'Age': {1: '18-24', 2: '25-29', 3: '30-34', 4: '35-39', 5: '40-44', 
                6: '45-49', 7: '50-54', 8: '55-59', 9: '60-64', 10: '65-69', 
                11: '70-74', 12: '75-79', 13: '80 or older'},
        'Education': {1: 'Never attended school', 2: 'Grades 1-8', 
                     3: 'Grades 9-11', 4: 'Grade 12', 5: '1 year college', 
                     6: 'College 2 years or more'},
        'Income': {1: 'Less than $10k', 2: '$10k - $15k', 3: '$15k - $20k',
                  4: '$20k - $25k', 5: '$25k - $35k', 6: '$35k - $50k',
                  7: '$50k - $75k', 8: 'More than $75k'},
    }
    
    def __init__(self, model, feature_names: list, demographic_features: list = None):
        """
        Initialize fairness evaluator.
        
        Args:
            model: Trained prediction model
            feature_names: List of all feature names
            demographic_features: Demographic features to evaluate ('Sex', 'Age', etc.)
        """
        self.model = model
        self.feature_names = feature_names
        self.demographic_features = demographic_features or ['Sex', 'Age', 'Education', 'Income']
        self.fairness_metrics = {}
        
    def get_demographic_indices(self) -> Dict[str, int]:
        """Get indices of demographic features in the feature list."""
        indices = {}
        for demo in self.demographic_features:
            if demo in self.feature_names:
                indices[demo] = self.feature_names.index(demo)
        return indices
    
    def stratify_by_demographic(self, X: np.ndarray, y_true: np.ndarray, 
                               demographic_feature: str) -> Dict[str, Tuple]:
        """
        Stratify dataset by demographic feature.
        
        Args:
            X: Features
            y_true: True labels
            demographic_feature: Name of demographic feature
            
        Returns:
            Dictionary mapping demographic groups to (X, y) tuples
        """
        indices = self.get_demographic_indices()
        
        if demographic_feature not in indices:
            raise ValueError(f"{demographic_feature} not found in features")
        
        demo_idx = indices[demographic_feature]
        groups = {}
        
        for group_value in np.unique(X[:, demo_idx]):
            mask = X[:, demo_idx] == group_value
            groups[str(int(group_value))] = (X[mask], y_true[mask])
        
        return groups
    
    def evaluate_group_metrics(self, X: np.ndarray, y_true: np.ndarray, 
                              demographic_feature: str) -> pd.DataFrame:
        """
        Evaluate metrics for each demographic group.
        
        Args:
            X: Features
            y_true: True labels
            demographic_feature: Demographic feature to evaluate
            
        Returns:
            DataFrame with metrics for each group
        """
        groups = self.stratify_by_demographic(X, y_true, demographic_feature)
        results = []
        
        for group_id, (X_group, y_group) in groups.items():
            if len(y_group) == 0:
                continue
            
            y_pred = self.model.predict(X_group)
            y_pred_proba = self.model.predict_proba(X_group)
            
            # For multi-class, use weighted average
            accuracy = accuracy_score(y_group, y_pred)
            precision = precision_score(y_group, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_group, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_group, y_pred, average='weighted', zero_division=0)
            
            group_label = self.DEMOGRAPHIC_COLUMNS.get(demographic_feature, {}).get(int(group_id), str(group_id))
            
            results.append({
                'Group': group_label,
                'Size': len(y_group),
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1,
            })
        
        df_results = pd.DataFrame(results)
        print(f"\n{demographic_feature} Group Metrics:")
        print(df_results.to_string(index=False))
        
        return df_results
    
    def calculate_demographic_parity_difference(self, X: np.ndarray, y_true: np.ndarray,
                                               demographic_feature: str, 
                                               favorable_outcome: int = 0) -> float:
        """
        Calculate Demographic Parity Difference.
        Measures if prediction probability differs by demographic group.
        
        Args:
            X: Features
            y_true: True labels
            demographic_feature: Demographic feature
            favorable_outcome: Class considered favorable
            
        Returns:
            Demographic Parity Difference (0 is perfect fairness)
        """
        groups = self.stratify_by_demographic(X, y_true, demographic_feature)
        favorable_rates = []
        
        for group_id, (X_group, y_group) in groups.items():
            y_pred = self.model.predict(X_group)
            favorable_rate = np.mean(y_pred == favorable_outcome)
            favorable_rates.append(favorable_rate)
        
        dpd = np.max(favorable_rates) - np.min(favorable_rates)
        return dpd
    
    def calculate_equal_opportunity_difference(self, X: np.ndarray, y_true: np.ndarray,
                                              demographic_feature: str,
                                              positive_class: int = 1) -> float:
        """
        Calculate Equal Opportunity Difference.
        Measures if true positive rates differ by demographic group.
        
        Args:
            X: Features
            y_true: True labels
            demographic_feature: Demographic feature
            positive_class: Class considered positive
            
        Returns:
            Equal Opportunity Difference (0 is perfect fairness)
        """
        groups = self.stratify_by_demographic(X, y_true, demographic_feature)
        tpr_values = []
        
        for group_id, (X_group, y_group) in groups.items():
            y_pred = self.model.predict(X_group)
            
            # Calculate TPR for positive class
            tp = np.sum((y_pred == positive_class) & (y_group == positive_class))
            fn = np.sum((y_pred != positive_class) & (y_group == positive_class))
            
            if tp + fn > 0:
                tpr = tp / (tp + fn)
                tpr_values.append(tpr)
        
        if tpr_values:
            eod = np.max(tpr_values) - np.min(tpr_values)
            return eod
        return 0
    
    def calculate_disparate_impact_ratio(self, X: np.ndarray, y_true: np.ndarray,
                                        demographic_feature: str,
                                        favorable_outcome: int = 0) -> float:
        """
        Calculate Disparate Impact Ratio (80% rule).
        Ratio should be >= 0.8 for groups to be considered fairly treated.
        
        Args:
            X: Features
            y_true: True labels
            demographic_feature: Demographic feature
            favorable_outcome: Class considered favorable
            
        Returns:
            Disparate Impact Ratio
        """
        groups = self.stratify_by_demographic(X, y_true, demographic_feature)
        favorable_rates = {}
        
        for group_id, (X_group, y_group) in groups.items():
            y_pred = self.model.predict(X_group)
            favorable_rate = np.mean(y_pred == favorable_outcome)
            favorable_rates[group_id] = favorable_rate
        
        rates = list(favorable_rates.values())
        if len(rates) >= 2 and min(rates) > 0:
            dir_ratio = min(rates) / max(rates)
            return dir_ratio
        return 1.0
    
    def evaluate_fairness(self, X: np.ndarray, y_true: np.ndarray) -> Dict[str, Dict]:
        """
        Comprehensively evaluate fairness across all demographic groups.
        
        Args:
            X: Features
            y_true: True labels
            
        Returns:
            Dictionary with fairness metrics for each demographic
        """
        print("\n=== Fairness Evaluation ===\n")
        
        fairness_results = {}
        
        for demographic in self.demographic_features:
            print(f"\nEvaluating {demographic}...")
            
            group_metrics = self.evaluate_group_metrics(X, y_true, demographic)
            dpd = self.calculate_demographic_parity_difference(X, y_true, demographic)
            eod = self.calculate_equal_opportunity_difference(X, y_true, demographic)
            dir_ratio = self.calculate_disparate_impact_ratio(X, y_true, demographic)
            
            fairness_results[demographic] = {
                'group_metrics': group_metrics,
                'demographic_parity_difference': dpd,
                'equal_opportunity_difference': eod,
                'disparate_impact_ratio': dir_ratio,
            }
            
            print(f"  Demographic Parity Difference: {dpd:.4f}")
            print(f"  Equal Opportunity Difference: {eod:.4f}")
            print(f"  Disparate Impact Ratio: {dir_ratio:.4f}")
            
            # Flag if biased
            if dpd > 0.1:
                print(f"  ⚠ WARNING: Significant bias detected (DPD > 0.1)")
            if dir_ratio < 0.8:
                print(f"  ⚠ WARNING: Disparate impact detected (DIR < 0.8)")
        
        self.fairness_metrics = fairness_results
        return fairness_results
    
    def get_fairness_report(self) -> str:
        """Generate a text report of fairness evaluation."""
        if not self.fairness_metrics:
            return "No fairness evaluation conducted yet."
        
        report = "\n" + "="*60 + "\n"
        report += "FAIRNESS EVALUATION REPORT\n"
        report += "="*60 + "\n\n"
        
        for demographic, metrics in self.fairness_metrics.items():
            report += f"\n{demographic.upper()}\n"
            report += "-" * 40 + "\n"
            
            report += "\nGroup Performance Metrics:\n"
            report += metrics['group_metrics'].to_string(index=False) + "\n"
            
            report += f"\nDemographic Parity Difference: {metrics['demographic_parity_difference']:.4f}\n"
            report += f"Equal Opportunity Difference: {metrics['equal_opportunity_difference']:.4f}\n"
            report += f"Disparate Impact Ratio: {metrics['disparate_impact_ratio']:.4f}\n"
            
            # Recommendations
            if metrics['demographic_parity_difference'] > 0.1:
                report += "⚠ Recommendation: Implement fairness-aware preprocessing\n"
            if metrics['disparate_impact_ratio'] < 0.8:
                report += "⚠ Recommendation: Consider retraining with fairness constraints\n"
        
        report += "\n" + "="*60 + "\n"
        return report
