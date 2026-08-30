"""Quick training script: trains a small RandomForest on a sample and saves artifacts.
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib


DATA_PATH = Path("diabetes_012_health_indicators_BRFSS2015.csv")
OUT_DIR = Path("ml_pipeline")
MODEL_DIR = OUT_DIR / "trained_models"
RESULTS_DIR = OUT_DIR / "results"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_sample(n_samples=10000, random_state=42):
    df = pd.read_csv(DATA_PATH)
    if n_samples and n_samples < len(df):
        df = df.sample(n_samples, random_state=random_state)
    return df


def quick_preprocess(df):
    target_col = 'Diabetes_012'
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols].astype(float)
    y = df[target_col].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return {
        'X_train': X_train_scaled,
        'X_test': X_test_scaled,
        'y_train': y_train.values,
        'y_test': y_test.values,
        'feature_names': feature_cols,
        'scaler': scaler,
    }


def train_and_save(sample_n=10000):
    print('Loading sample...')
    df = load_sample(n_samples=sample_n)
    proc = quick_preprocess(df)

    print('Training RandomForest (quick)...')
    rf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    rf.fit(proc['X_train'], proc['y_train'])

    y_pred = rf.predict(proc['X_test'])
    y_proba = rf.predict_proba(proc['X_test']) if hasattr(rf, 'predict_proba') else None

    perf = {
        'accuracy': float(accuracy_score(proc['y_test'], y_pred)),
        'precision': float(precision_score(proc['y_test'], y_pred, average='weighted', zero_division=0)),
        'recall': float(recall_score(proc['y_test'], y_pred, average='weighted', zero_division=0)),
        'f1_score': float(f1_score(proc['y_test'], y_pred, average='weighted', zero_division=0)),
    }

    # Save model and scaler
    model_path = MODEL_DIR / 'random_forest.pkl'
    scaler_path = MODEL_DIR / 'scaler.pkl'
    joblib.dump(rf, model_path)
    joblib.dump(proc['scaler'], scaler_path)

    # Feature importance (quick)
    try:
        importances = rf.feature_importances_
        fi = [ {'feature': name, 'importance': float(imp)} for name, imp in zip(proc['feature_names'], importances) ]
        fi_sorted = sorted(fi, key=lambda x: x['importance'], reverse=True)[:20]
    except Exception:
        fi_sorted = []

    # Save results JSON and minimal CSV
    results = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'best_model': 'random_forest',
        'model_performance': perf,
        'feature_importance': fi_sorted,
        'test_set_size': int(len(proc['y_test'])),
        'feature_names': proc['feature_names'],
    }

    with open(RESULTS_DIR / 'pipeline_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    comp_df = pd.DataFrame([{
        'Model': 'random_forest',
        'Accuracy': perf['accuracy'],
        'Precision': perf['precision'],
        'Recall': perf['recall'],
        'F1-Score': perf['f1_score'],
        'ROC-AUC': None,
    }])
    comp_df.to_csv(RESULTS_DIR / 'model_comparison.csv', index=False)

    with open(RESULTS_DIR / 'fairness_report.txt', 'w') as f:
        f.write('Quick training fairness report: not computed in quick mode. Run full pipeline for detailed fairness metrics.')

    print('Quick training complete. Model saved to', model_path)
    print('Performance:', perf)


if __name__ == '__main__':
    train_and_save(sample_n=8000)
