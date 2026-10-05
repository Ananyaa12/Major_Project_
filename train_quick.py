"""Train the six-feature diabetes model on the complete BRFSS dataset."""
import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib


DATA_PATH = Path("diabetes_012_health_indicators_BRFSS2015.csv")
OUT_DIR = Path("ml_pipeline")
MODEL_DIR = OUT_DIR / "trained_models"
RESULTS_DIR = OUT_DIR / "results"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


SELECTED_FEATURES = ['BMI', 'Age', 'Income', 'GenHlth', 'PhysHlth', 'Education']


def load_dataset():
    return pd.read_csv(DATA_PATH)


def preprocess(df):
    target_col = 'Diabetes_012'
    X = df[SELECTED_FEATURES].astype(float)
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
        'feature_names': SELECTED_FEATURES,
        'scaler': scaler,
    }


def calculate_metrics(y_true, y_pred):
    return {
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'precision': float(precision_score(y_true, y_pred, average='weighted', zero_division=0)),
        'recall': float(recall_score(y_true, y_pred, average='weighted', zero_division=0)),
        'f1_score': float(f1_score(y_true, y_pred, average='weighted', zero_division=0)),
    }


def train_and_save():
    print('Loading complete dataset...')
    df = load_dataset()
    print(f'Loaded {len(df):,} rows and using six features: {SELECTED_FEATURES}')
    proc = preprocess(df)

    print('Training holdout RandomForest for evaluation...')
    evaluation_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, max_depth=18)
    evaluation_model.fit(proc['X_train'], proc['y_train'])

    holdout_pred = evaluation_model.predict(proc['X_test'])
    holdout_metrics = calculate_metrics(proc['y_test'], holdout_pred)

    print('Training final RandomForest on all dataset rows...')
    final_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, max_depth=18)
    X_all_scaled = proc['scaler'].fit_transform(df[SELECTED_FEATURES].astype(float))
    y_all = df['Diabetes_012'].astype(int).to_numpy()
    final_model.fit(X_all_scaled, y_all)
    full_pred = final_model.predict(X_all_scaled)
    full_metrics = calculate_metrics(y_all, full_pred)

    # Save model and scaler
    model_path = MODEL_DIR / 'random_forest.pkl'
    scaler_path = MODEL_DIR / 'scaler.pkl'
    joblib.dump(final_model, model_path)
    joblib.dump(proc['scaler'], scaler_path)

    # Feature importance (quick)
    try:
        importances = final_model.feature_importances_
        fi = [ {'feature': name, 'importance': float(imp)} for name, imp in zip(proc['feature_names'], importances) ]
        fi_sorted = sorted(fi, key=lambda x: x['importance'], reverse=True)
    except Exception:
        fi_sorted = []

    # Save results JSON and minimal CSV
    results = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'best_model': 'random_forest',
        'model_performance': holdout_metrics,
        'holdout_performance': holdout_metrics,
        'full_dataset_performance': full_metrics,
        'feature_importance': fi_sorted,
        'test_set_size': int(len(proc['y_test'])),
        'dataset_size': int(len(df)),
        'feature_names': proc['feature_names'],
        'evaluation_confusion_matrix': confusion_matrix(proc['y_test'], holdout_pred).tolist(),
        'full_dataset_confusion_matrix': confusion_matrix(y_all, full_pred).tolist(),
    }

    with open(RESULTS_DIR / 'pipeline_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    comp_df = pd.DataFrame([{
        'Model': 'random_forest',
        'Accuracy': holdout_metrics['accuracy'],
        'Precision': holdout_metrics['precision'],
        'Recall': holdout_metrics['recall'],
        'F1-Score': holdout_metrics['f1_score'],
        'ROC-AUC': None,
    }])
    comp_df.to_csv(RESULTS_DIR / 'model_comparison.csv', index=False)

    with open(RESULTS_DIR / 'fairness_report.txt', 'w') as f:
        f.write(
            'Full dataset training report\n'
            f'Rows used: {len(df):,}\n'
            f'Features used: {", ".join(SELECTED_FEATURES)}\n'
            f'Holdout metrics: {holdout_metrics}\n'
            f'Full dataset fit metrics: {full_metrics}\n'
            'Note: full dataset fit metrics are descriptive and should not be used as an unbiased estimate.\n'
        )

    print('Full dataset training complete. Model saved to', model_path)
    print('Holdout performance:', holdout_metrics)
    print('Full dataset fit performance:', full_metrics)


if __name__ == '__main__':
    train_and_save()
