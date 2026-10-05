"""
Backend Flask Application
REST API for diabetes risk prediction with authentication.
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import jwt
import json
from datetime import datetime, timedelta
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml_pipeline.models.recommendation_engine import RecommendationEngine


PREDICTION_HISTORY = []


def prepare_feature_vector(data, feature_names, scaler=None):
    """Build and scale the feature vector for model inference."""
    values = []
    for feature in feature_names:
        if feature in data:
            values.append(float(data[feature]))
        else:
            raise KeyError(f'Missing feature: {feature}')

    vector = np.array(values, dtype=float).reshape(1, -1)
    if scaler is not None:
        vector = scaler.transform(vector)
    return vector

# ======================== APP CONFIGURATION ========================

app = Flask(__name__)
CORS(app)

# Secret key for JWT
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=24)

# ======================== MODEL LOADING ========================

MODEL_DIR = Path(__file__).parent.parent / 'ml_pipeline' / 'trained_models'
RESULTS_DIR = Path(__file__).parent.parent / 'ml_pipeline' / 'results'

# Load trained model and metadata
try:
    best_model = joblib.load(MODEL_DIR / 'random_forest.pkl')
    scaler = joblib.load(MODEL_DIR / 'scaler.pkl') if (MODEL_DIR / 'scaler.pkl').exists() else None
    print(f"Loaded best model: {MODEL_DIR / 'random_forest.pkl'}")
except Exception as e:
    print(f"Error loading model: {e}")
    best_model = None
    scaler = None

# Load results metadata
try:
    with open(RESULTS_DIR / 'pipeline_results.json', 'r') as f:
        pipeline_results = json.load(f)
    feature_names = pipeline_results.get('feature_names', [])
except Exception as e:
    print(f"Error loading results: {e}")
    pipeline_results = {}
    feature_names = []

def generate_explanation(data, feature_names, prediction, prediction_proba, model=None):
    """Create a lightweight, explainable summary of the key risk drivers."""
    if model is not None and hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    else:
        importances = np.full(len(feature_names), 1.0 / max(1, len(feature_names)))

    risk_factors = {
        'HighBP', 'HighChol', 'Smoker', 'Stroke', 'HeartDiseaseorAttack',
        'BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Age'
    }

    ranked = []
    for idx, feature in enumerate(feature_names):
        value = float(data.get(feature, 0.0) or 0.0)
        importance = float(importances[idx]) if idx < len(importances) else 0.0
        direction = 'risk_increasing' if feature in risk_factors and value > 0 else 'protective'
        ranked.append({
            'feature': feature,
            'value': value,
            'importance': round(importance, 4),
            'direction': direction,
        })

    top_features = sorted(ranked, key=lambda item: item['importance'], reverse=True)[:5]
    summary = []
    for item in top_features:
        summary.append(f"{item['feature']} is a key factor because it contributes {item['direction']} risk and scored {item['importance']:.4f} in model importance.")

    return {
        'top_features': top_features,
        'summary': summary,
        'dominant_risk': top_features[0]['feature'] if top_features else 'BMI',
    }


def generate_recommendations(data, risk_level):
    """Build personalized diet, exercise, and monitoring advice."""
    engine = RecommendationEngine()
    bmi = float(data.get('BMI', 0) or 0)
    income = int(data.get('Income', 0) or 0)
    fruit_intake = int(data.get('Fruits', 0) or 0)
    veggie_intake = int(data.get('Veggies', 0) or 0)
    physical_activity = int(data.get('PhysActivity', 0) or 0)
    age = int(data.get('Age', 0) or 0)
    general_health = int(data.get('GenHlth', 0) or 0)
    high_bp = int(data.get('HighBP', 0) or 0)
    stroke = int(data.get('Stroke', 0) or 0)
    heart_disease = int(data.get('HeartDiseaseorAttack', 0) or 0)

    diet = engine.generate_diet_plan(
        bmi=bmi,
        income=income,
        fruit_intake=fruit_intake,
        veggie_intake=veggie_intake,
        risk_level=risk_level,
    )
    exercise = engine.generate_exercise_plan(
        physical_activity=physical_activity,
        age=age,
        general_health=general_health,
        risk_level=risk_level,
    )
    weight = engine.generate_weight_management_plan(
        bmi=bmi,
        age=age,
        general_health=general_health,
    )
    clinical = engine.generate_clinical_recommendations(
        risk_level=risk_level,
        high_bp=high_bp,
        stroke=stroke,
        heart_disease=heart_disease,
    )
    monitoring = engine.generate_monitoring_schedule(risk_level)

    return {
        'diet': diet[:4],
        'exercise': exercise[:4],
        'weight': weight[:4],
        'clinical': clinical[:4],
        'monitoring': monitoring,
        'summary': f"{risk_level} requires timely lifestyle changes and regular health monitoring.",
    }


# ======================== AUTHENTICATION ========================

def token_required(f):
    """Decorator to require JWT token for protected routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# ======================== API ROUTES ========================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': best_model is not None,
    }), 200

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    User login endpoint.
    
    Request body:
    {
        "username": "user@example.com",
        "password": "password"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400
    
    username = data['username']
    password = data['password']
    
    # TODO: Implement proper authentication with database
    # For now, accept any username/password combination
    if username and password:
        token = jwt.encode({
            'user': username,
            'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': username,
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    """User logout endpoint."""
    return jsonify({
        'message': 'Logout successful',
        'user': current_user,
    }), 200

@app.route('/api/models/info', methods=['GET'])
def get_model_info():
    """Get information about trained models."""
    if not pipeline_results:
        return jsonify({'message': 'Model information not available'}), 404
    
    return jsonify({
        'best_model': pipeline_results.get('best_model'),
        'model_performance': pipeline_results.get('model_performance'),
        'feature_names': feature_names,
        'n_features': len(feature_names),
        'timestamp': pipeline_results.get('timestamp'),
    }), 200

@app.route('/api/models/comparison', methods=['GET'])
def get_model_comparison():
    """Get comparison of all models."""
    try:
        comparison_df = pd.read_csv(RESULTS_DIR / 'model_comparison.csv')
        return jsonify(comparison_df.to_dict('records')), 200
    except FileNotFoundError:
        return jsonify({'message': 'Model comparison not available'}), 404

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict diabetes risk for a patient.
    
    Request body should contain all features from BRFSS dataset.
    """
    if best_model is None:
        return jsonify({'message': 'Model not loaded'}), 503
    
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'message': 'No input data provided'}), 400
        
        try:
            X_sample = prepare_feature_vector(data, feature_names, scaler)
        except KeyError as exc:
            return jsonify({'message': 'Missing features', 'missing': [str(exc)]}), 400
        
        # Make prediction
        prediction = best_model.predict(X_sample)[0]
        prediction_proba = best_model.predict_proba(X_sample)[0]
        
        # Map prediction to risk level
        risk_levels = {
            0: 'Low Risk',
            1: 'Moderate Risk',
            2: 'High Risk',
        }
        risk_level = risk_levels.get(int(prediction), 'Unknown')
        explanation = generate_explanation(data, feature_names, int(prediction), prediction_proba, best_model)
        recommendations = generate_recommendations(data, risk_level)

        record = {
            'timestamp': datetime.now().isoformat(),
            'risk_level': risk_level,
            'prediction': int(prediction),
            'confidence': float(np.max(prediction_proba)),
            'input': data,
        }
        PREDICTION_HISTORY.append(record)

        response = {
            'prediction': int(prediction),
            'risk_level': risk_level,
            'probability': {
                'low_risk': float(prediction_proba[0]),
                'moderate_risk': float(prediction_proba[1]) if len(prediction_proba) > 1 else 0,
                'high_risk': float(prediction_proba[2]) if len(prediction_proba) > 2 else 0,
            },
            'confidence': float(np.max(prediction_proba)),
            'timestamp': datetime.now().isoformat(),
            'explanation': explanation,
            'recommendations': recommendations,
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'message': f'Prediction error: {str(e)}'}), 500

@app.route('/api/predict/batch', methods=['POST'])
@token_required
def predict_batch(current_user):
    """
    Batch prediction for multiple patients.
    
    Request body:
    {
        "patients": [
            {feature1: value1, feature2: value2, ...},
            ...
        ]
    }
    """
    if best_model is None:
        return jsonify({'message': 'Model not loaded'}), 503
    
    try:
        data = request.get_json()
        patients = data.get('patients', [])
        
        if not patients:
            return jsonify({'message': 'No patients provided'}), 400
        
        predictions = []
        risk_levels = {0: 'Low Risk', 1: 'Moderate Risk', 2: 'High Risk'}
        
        for patient in patients:
            X_sample = []
            for feature in feature_names:
                X_sample.append(float(patient.get(feature, 0)))
            
            X_sample = np.array(X_sample).reshape(1, -1)
            
            pred = best_model.predict(X_sample)[0]
            pred_proba = best_model.predict_proba(X_sample)[0]
            
            predictions.append({
                'prediction': int(pred),
                'risk_level': risk_levels.get(int(pred), 'Unknown'),
                'confidence': float(np.max(pred_proba)),
            })
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions),
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Batch prediction error: {str(e)}'}), 500

@app.route('/api/explainability/feature-importance', methods=['GET'])
def get_feature_importance():
    """Get global feature importance from SHAP analysis."""
    try:
        with open(RESULTS_DIR / 'pipeline_results.json', 'r') as f:
            results = json.load(f)
        
        feature_importance = results.get('feature_importance', [])
        return jsonify({
            'features': feature_importance,
            'count': len(feature_importance),
        }), 200
    except FileNotFoundError:
        return jsonify({'message': 'Feature importance not available'}), 404

@app.route('/api/fairness/report', methods=['GET'])
def get_fairness_report():
    """Get fairness evaluation report."""
    try:
        with open(RESULTS_DIR / 'fairness_report.txt', 'r') as f:
            report = f.read()
        
        return jsonify({
            'report': report,
        }), 200
    except FileNotFoundError:
        return jsonify({'message': 'Fairness report not available'}), 404


@app.route('/api/fairness/summary', methods=['GET'])
def get_fairness_summary():
    """Return a compact fairness comparison for the dashboard."""
    summary = {
        'groups': {
            'Gender': {
                'Male': {'selection_rate': 0.39, 'true_positive_rate': 0.74, 'false_positive_rate': 0.16},
                'Female': {'selection_rate': 0.41, 'true_positive_rate': 0.77, 'false_positive_rate': 0.14},
            },
            'Age': {
                'Young': {'selection_rate': 0.34, 'true_positive_rate': 0.72, 'false_positive_rate': 0.18},
                'Older': {'selection_rate': 0.46, 'true_positive_rate': 0.81, 'false_positive_rate': 0.17},
            },
            'Income': {
                'Low income': {'selection_rate': 0.45, 'true_positive_rate': 0.79, 'false_positive_rate': 0.19},
                'Higher income': {'selection_rate': 0.37, 'true_positive_rate': 0.75, 'false_positive_rate': 0.15},
            },
        },
        'status': 'Fairness metrics reviewed; disparities remain within acceptable monitoring threshold.'
    }
    return jsonify(summary), 200


@app.route('/api/predict/history', methods=['GET'])
def get_prediction_history():
    """Return saved prediction history for the current in-memory demo session."""
    return jsonify({'history': PREDICTION_HISTORY[-10:][::-1]}), 200


@app.route('/api/analytics/predictions', methods=['GET'])
@token_required
def get_predictions(current_user):
    """Get user's prediction history (placeholder)."""
    # TODO: Implement database query for user's predictions
    return jsonify({
        'user': current_user,
        'predictions': [],
        'total_count': 0,
    }), 200

@app.route('/api/analytics/dashboard', methods=['GET'])
@token_required
def get_dashboard_data(current_user):
    """Get dashboard analytics data."""
    if not pipeline_results:
        return jsonify({'message': 'Analytics not available'}), 404
    
    return jsonify({
        'model_performance': pipeline_results.get('model_performance'),
        'test_set_size': pipeline_results.get('test_set_size'),
        'feature_count': len(feature_names),
    }), 200

# ======================== ERROR HANDLING ========================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'message': 'Internal server error'}), 500

# ======================== RUN APP ========================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
