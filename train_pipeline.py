"""
Main Training Script
Orchestrates the complete ML pipeline: preprocessing, training, evaluation, explainability, fairness.
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ml_pipeline.preprocessing import DataLoader, Preprocessor
from ml_pipeline.models import ModelTrainer
from ml_pipeline.explainability import SHAPExplainer
from ml_pipeline.fairness import FairnessEvaluator
from ml_pipeline.models.recommendation_engine import RecommendationEngine


def create_directories():
    """Create required output directories."""
    dirs = [
        'ml_pipeline/trained_models',
        'ml_pipeline/results',
        'ml_pipeline/visualizations',
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")


def main():
    """Execute the complete ML pipeline."""
    
    print("\n" + "="*80)
    print("DIABETES RISK PREDICTION - ML PIPELINE")
    print("="*80 + "\n")
    
    # ======================== STEP 1: DATA LOADING ========================
    print("STEP 1: DATA LOADING")
    print("-" * 80)
    
    data_loader = DataLoader('diabetes_012_health_indicators_BRFSS2015.csv')
    df = data_loader.load_data()
    
    data_info = data_loader.get_data_info()
    print(f"\nDataset Info:")
    print(f"  Shape: {data_info['shape']}")
    print(f"  Features: {data_info['n_features']}")
    print(f"  Samples: {data_info['n_samples']}")
    print(f"  Classes: {data_info['target_classes']}")
    print(f"  Class Distribution: {data_info['class_distribution']}")
    
    X, y = data_loader.get_X_y()
    feature_names = data_loader.get_feature_columns()
    
    # ======================== STEP 2: PREPROCESSING ========================
    print("\n\nSTEP 2: DATA PREPROCESSING")
    print("-" * 80)
    
    preprocessor = Preprocessor(test_size=0.2, random_state=42)
    processed_data = preprocessor.preprocess(X, y, apply_smote=True, 
                                            remove_outliers_flag=False,
                                            scale_method='standard')
    
    X_train = processed_data['X_train']
    X_test = processed_data['X_test']
    y_train = processed_data['y_train']
    y_test = processed_data['y_test']
    
    print(f"\nAfter preprocessing:")
    print(f"  X_train shape: {X_train.shape}")
    print(f"  X_test shape: {X_test.shape}")
    print(f"  y_train shape: {y_train.shape}")
    print(f"  y_test shape: {y_test.shape}")
    
    # ======================== STEP 3: MODEL TRAINING ========================
    print("\n\nSTEP 3: BASE MODEL TRAINING")
    print("-" * 80)
    
    trainer = ModelTrainer(random_state=42)
    trainer.build_base_models()
    trainer.train_base_models(X_train, y_train)
    
    # ======================== STEP 4: MODEL EVALUATION ========================
    print("\n\nSTEP 4: BASE MODEL EVALUATION")
    print("-" * 80)
    
    trainer.evaluate_models(X_test, y_test)
    best_model_name, best_model_results = trainer.select_best_model(metric='f1_weighted')
    
    # ======================== STEP 5: ENSEMBLE MODELS ========================
    print("\n\nSTEP 5: ENSEMBLE MODEL TRAINING & EVALUATION")
    print("-" * 80)
    
    trainer.train_ensemble_models(X_train, y_train)
    trainer.evaluate_ensemble_models(X_test, y_test)
    
    # ======================== STEP 6: MODEL COMPARISON ========================
    print("\n\nSTEP 6: MODEL COMPARISON")
    print("-" * 80)
    
    comparison_df = trainer.get_model_comparison()
    
    # Get the best overall model
    best_overall_model = comparison_df.iloc[0]['Model']
    print(f"\n✅ BEST OVERALL MODEL: {best_overall_model}")
    
    # ======================== STEP 7: SAVE MODELS ========================
    print("\n\nSTEP 7: SAVING MODELS")
    print("-" * 80)
    
    trainer.save_all_models('ml_pipeline/trained_models')
    
    # Get the best model object
    if best_overall_model in trainer.base_models:
        best_model = trainer.base_models[best_overall_model]
    else:
        best_model = trainer.ensemble_models[best_overall_model]
    
    # ======================== STEP 8: EXPLAINABILITY (SHAP) ========================
    print("\n\nSTEP 8: SHAP EXPLAINABILITY ANALYSIS")
    print("-" * 80)
    
    explainer = SHAPExplainer(best_model, X_test, feature_names)
    explainer.create_explainer()
    
    # Get feature importance
    feature_importance = explainer.get_feature_importance(X_test, top_n=10)
    
    print("\nTop 10 Most Important Features (SHAP):")
    print(feature_importance.to_string())
    
    # ======================== STEP 9: FAIRNESS EVALUATION ========================
    print("\n\nSTEP 9: FAIRNESS EVALUATION")
    print("-" * 80)
    
    fairness_evaluator = FairnessEvaluator(best_model, feature_names, 
                                          demographic_features=['Sex', 'Age', 'Education', 'Income'])
    fairness_results = fairness_evaluator.evaluate_fairness(X_test, y_test)
    
    fairness_report = fairness_evaluator.get_fairness_report()
    print(fairness_report)
    
    # ======================== STEP 10: SAVE RESULTS ========================
    print("\n\nSTEP 10: SAVING RESULTS")
    print("-" * 80)
    
    results_dict = {
        'timestamp': datetime.now().isoformat(),
        'best_model': best_overall_model,
        'model_performance': {
            'accuracy': float(comparison_df.iloc[0]['Accuracy']),
            'precision': float(comparison_df.iloc[0]['Precision']),
            'recall': float(comparison_df.iloc[0]['Recall']),
            'f1_score': float(comparison_df.iloc[0]['F1-Score']),
            'roc_auc': float(comparison_df.iloc[0]['ROC-AUC']) if pd.notna(comparison_df.iloc[0]['ROC-AUC']) else None,
        },
        'all_models_performance': comparison_df.to_dict('records'),
        'feature_importance': feature_importance.to_dict('records'),
        'test_set_size': len(y_test),
        'feature_names': feature_names,
    }
    
    # Save results as JSON
    with open('ml_pipeline/results/pipeline_results.json', 'w') as f:
        json.dump(results_dict, f, indent=2)
    
    # Save comparison as CSV
    comparison_df.to_csv('ml_pipeline/results/model_comparison.csv', index=False)
    
    # Save fairness report
    with open('ml_pipeline/results/fairness_report.txt', 'w') as f:
        f.write(fairness_report)
    
    print("✅ Results saved to ml_pipeline/results/")
    
    # ======================== SUMMARY ========================
    print("\n\n" + "="*80)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*80 + "\n")
    
    print(f"✅ Dataset loaded: {data_info['n_samples']} samples, {data_info['n_features']} features")
    print(f"✅ Data preprocessed with SMOTE balancing")
    print(f"✅ 11 base models trained and evaluated")
    print(f"✅ 3 ensemble models created (soft voting, hard voting, stacking)")
    print(f"✅ Best model: {best_overall_model}")
    print(f"   - Accuracy: {comparison_df.iloc[0]['Accuracy']:.4f}")
    print(f"   - Precision: {comparison_df.iloc[0]['Precision']:.4f}")
    print(f"   - Recall: {comparison_df.iloc[0]['Recall']:.4f}")
    print(f"   - F1-Score: {comparison_df.iloc[0]['F1-Score']:.4f}")
    print(f"\n✅ SHAP explainability analysis completed")
    print(f"✅ Fairness evaluation across 4 demographic groups completed")
    print(f"✅ All models saved and results exported")
    
    print("\n" + "="*80 + "\n")
    
    return {
        'best_model': best_model,
        'best_model_name': best_overall_model,
        'explainer': explainer,
        'fairness_evaluator': fairness_evaluator,
        'feature_names': feature_names,
        'scaler': processed_data['scaler'],
    }


if __name__ == '__main__':
    create_directories()
    pipeline_output = main()
