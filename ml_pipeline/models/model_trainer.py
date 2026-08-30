"""
Model Training Module
Trains multiple base models and builds ensemble models.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, StackingClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
    roc_curve, auc
)
import joblib
from pathlib import Path
from typing import Dict, Any, Tuple


class ModelTrainer:
    """Train multiple base models and build ensemble models."""
    
    def __init__(self, random_state: int = 42, verbose: int = 1):
        """
        Initialize the model trainer.
        
        Args:
            random_state: Random state for reproducibility
            verbose: Verbosity level
        """
        self.random_state = random_state
        self.verbose = verbose
        self.base_models = {}
        self.ensemble_models = {}
        self.best_model = None
        self.best_model_name = None
        self.model_results = {}
        
    def build_base_models(self) -> Dict[str, Any]:
        """
        Build all base models for ensemble.
        
        Returns:
            Dictionary of base models
        """
        self.base_models = {
            'logistic_regression': LogisticRegression(
                max_iter=1000, random_state=self.random_state
            ),
            'decision_tree': DecisionTreeClassifier(
                random_state=self.random_state, max_depth=15
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100, random_state=self.random_state,
                n_jobs=-1, max_depth=15
            ),
            'svm': SVC(kernel='rbf', probability=True, random_state=self.random_state),
            'knn': KNeighborsClassifier(n_neighbors=5),
            'naive_bayes': GaussianNB(),
            'xgboost': XGBClassifier(
                n_estimators=100, random_state=self.random_state,
                use_label_encoder=False, eval_metric='mlogloss', verbosity=0
            ),
            'lightgbm': LGBMClassifier(
                n_estimators=100, random_state=self.random_state,
                verbose=-1, num_leaves=31
            ),
            'catboost': CatBoostClassifier(
                iterations=100, random_state=self.random_state,
                verbose=0, thread_count=-1
            ),
            'adaboost': AdaBoostClassifier(
                n_estimators=100, random_state=self.random_state
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100, random_state=self.random_state,
                max_depth=5
            ),
        }
        
        print(f"Built {len(self.base_models)} base models")
        return self.base_models
    
    def train_base_models(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, Dict]:
        """
        Train all base models and evaluate on test set.
        
        Args:
            X_train: Training features
            y_train: Training target
            
        Returns:
            Dictionary with training results for each model
        """
        if not self.base_models:
            self.build_base_models()
        
        for name, model in self.base_models.items():
            print(f"\nTraining {name}...")
            model.fit(X_train, y_train)
            print(f"{name} training completed.")
        
        return self.base_models
    
    def evaluate_models(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Dict]:
        """
        Evaluate all trained models on test set.
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary with evaluation metrics for each model
        """
        self.model_results = {}
        
        for name, model in self.base_models.items():
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            results = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision_weighted': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                'recall_weighted': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                'f1_weighted': f1_score(y_test, y_pred, average='weighted', zero_division=0),
                'confusion_matrix': confusion_matrix(y_test, y_pred),
                'classification_report': classification_report(y_test, y_pred),
            }
            
            # ROC-AUC for multi-class (one-vs-rest)
            try:
                roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='weighted')
                results['roc_auc'] = roc_auc
            except:
                results['roc_auc'] = None
            
            self.model_results[name] = results
            
            print(f"\n{name}:")
            print(f"  Accuracy: {results['accuracy']:.4f}")
            print(f"  Precision: {results['precision_weighted']:.4f}")
            print(f"  Recall: {results['recall_weighted']:.4f}")
            print(f"  F1 Score: {results['f1_weighted']:.4f}")
        
        return self.model_results
    
    def select_best_model(self, metric: str = 'f1_weighted') -> Tuple[str, Dict]:
        """
        Select the best performing model.
        
        Args:
            metric: Metric to use for selection
            
        Returns:
            Tuple of (best model name, best model results)
        """
        if not self.model_results:
            raise ValueError("Models not evaluated yet. Call evaluate_models first.")
        
        scores = {name: results[metric] for name, results in self.model_results.items()}
        self.best_model_name = max(scores, key=scores.get)
        self.best_model = self.base_models[self.best_model_name]
        
        print(f"\nBest model: {self.best_model_name} (Score: {scores[self.best_model_name]:.4f})")
        
        return self.best_model_name, self.model_results[self.best_model_name]
    
    def create_voting_ensemble(self, voting: str = 'soft') -> VotingClassifier:
        """
        Create a soft or hard voting ensemble.
        
        Args:
            voting: 'soft' or 'hard'
            
        Returns:
            VotingClassifier ensemble
        """
        estimators = list(self.base_models.items())
        ensemble = VotingClassifier(estimators=estimators, voting=voting, n_jobs=-1)
        
        self.ensemble_models[f'voting_{voting}'] = ensemble
        print(f"Created {voting} voting ensemble with {len(estimators)} models")
        
        return ensemble
    
    def create_stacking_ensemble(self, final_estimator=None) -> StackingClassifier:
        """
        Create a stacking ensemble.
        
        Args:
            final_estimator: Final estimator for stacking (default: LogisticRegression)
            
        Returns:
            StackingClassifier ensemble
        """
        if final_estimator is None:
            final_estimator = LogisticRegression(random_state=self.random_state)
        
        # Select subset of models for stacking to reduce complexity
        base_estimators = [
            ('rf', self.base_models['random_forest']),
            ('xgb', self.base_models['xgboost']),
            ('lgb', self.base_models['lightgbm']),
            ('cat', self.base_models['catboost']),
        ]
        
        ensemble = StackingClassifier(
            estimators=base_estimators,
            final_estimator=final_estimator,
            cv=5
        )
        
        self.ensemble_models['stacking'] = ensemble
        print("Created stacking ensemble")
        
        return ensemble
    
    def train_ensemble_models(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict:
        """
        Train all ensemble models.
        
        Args:
            X_train: Training features
            y_train: Training target
            
        Returns:
            Dictionary of trained ensemble models
        """
        print("\n=== Training Ensemble Models ===\n")
        
        # Voting ensembles
        for voting_type in ['soft', 'hard']:
            ensemble = self.create_voting_ensemble(voting=voting_type)
            print(f"Training {voting_type} voting ensemble...")
            ensemble.fit(X_train, y_train)
        
        # Stacking ensemble
        stacking = self.create_stacking_ensemble()
        print("Training stacking ensemble...")
        stacking.fit(X_train, y_train)
        
        return self.ensemble_models
    
    def evaluate_ensemble_models(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Evaluate all trained ensemble models.
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary with ensemble model results
        """
        print("\n=== Evaluating Ensemble Models ===\n")
        
        for name, model in self.ensemble_models.items():
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            results = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision_weighted': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                'recall_weighted': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                'f1_weighted': f1_score(y_test, y_pred, average='weighted', zero_division=0),
                'confusion_matrix': confusion_matrix(y_test, y_pred),
            }
            
            try:
                roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='weighted')
                results['roc_auc'] = roc_auc
            except:
                results['roc_auc'] = None
            
            self.model_results[name] = results
            
            print(f"\n{name}:")
            print(f"  Accuracy: {results['accuracy']:.4f}")
            print(f"  Precision: {results['precision_weighted']:.4f}")
            print(f"  Recall: {results['recall_weighted']:.4f}")
            print(f"  F1 Score: {results['f1_weighted']:.4f}")
        
        return self.model_results
    
    def get_model_comparison(self) -> pd.DataFrame:
        """
        Get comparison of all models.
        
        Returns:
            DataFrame with model comparison
        """
        comparison_data = []
        
        for model_name, results in self.model_results.items():
            comparison_data.append({
                'Model': model_name,
                'Accuracy': results['accuracy'],
                'Precision': results['precision_weighted'],
                'Recall': results['recall_weighted'],
                'F1-Score': results['f1_weighted'],
                'ROC-AUC': results.get('roc_auc', None),
            })
        
        df_comparison = pd.DataFrame(comparison_data).sort_values('F1-Score', ascending=False)
        
        print("\n=== Model Comparison ===")
        print(df_comparison.to_string(index=False))
        
        return df_comparison
    
    def save_model(self, model_name: str, filepath: str):
        """
        Save a trained model using joblib.
        
        Args:
            model_name: Name of the model to save
            filepath: Path to save the model
        """
        if model_name in self.base_models:
            model = self.base_models[model_name]
        elif model_name in self.ensemble_models:
            model = self.ensemble_models[model_name]
        else:
            raise ValueError(f"Model {model_name} not found")
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, filepath)
        print(f"Saved {model_name} to {filepath}")
    
    def save_all_models(self, directory: str):
        """
        Save all trained models.
        
        Args:
            directory: Directory to save models
        """
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        for name in self.base_models.keys():
            self.save_model(name, f"{directory}/{name}.pkl")
        
        for name in self.ensemble_models.keys():
            self.save_model(name, f"{directory}/{name}.pkl")
        
        print(f"Saved all models to {directory}")
    
    def load_model(self, filepath: str):
        """
        Load a trained model from disk.
        
        Args:
            filepath: Path to the saved model
            
        Returns:
            Loaded model
        """
        model = joblib.load(filepath)
        print(f"Loaded model from {filepath}")
        return model
