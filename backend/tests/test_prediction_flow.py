import numpy as np
from sklearn.preprocessing import StandardScaler

from backend.app import app, prepare_feature_vector, generate_recommendations


def test_prepare_feature_vector_scales_input_with_scaler():
    scaler = StandardScaler().fit(np.array([[0.0, 2.0], [1.0, 4.0]]))
    feature_names = ['feature_a', 'feature_b']
    payload = {'feature_a': 5.0, 'feature_b': 6.0}

    transformed = prepare_feature_vector(payload, feature_names, scaler)

    assert transformed.shape == (1, 2)
    np.testing.assert_allclose(transformed[0], scaler.transform([[5.0, 6.0]])[0])


def test_predict_endpoint_accepts_demo_request_without_auth():
    client = app.test_client()
    payload = {
        'HighBP': 1,
        'HighChol': 1,
        'CholCheck': 1,
        'BMI': 32.5,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 0,
        'PhysActivity': 0,
        'Fruits': 0,
        'Veggies': 0,
        'HvyAlcoholConsump': 0,
        'AnyHealthcare': 1,
        'NoDocbcCost': 0,
        'GenHlth': 4,
        'MentHlth': 10,
        'PhysHlth': 15,
        'DiffWalk': 1,
        'Sex': 0,
        'Age': 6,
        'Education': 4,
        'Income': 7,
    }

    response = client.post('/api/predict', json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert 'risk_level' in data
    assert 'probability' in data
    assert 'explanation' in data
    assert 'recommendations' in data


def test_generate_recommendations_returns_actionable_list():
    summary = generate_recommendations({
        'BMI': 31,
        'PhysActivity': 0,
        'Fruits': 0,
        'Veggies': 0,
        'Age': 7,
        'HighBP': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 0,
        'GenHlth': 4,
        'Income': 2,
    }, 'High Risk')

    assert isinstance(summary, dict)
    assert 'diet' in summary
    assert 'exercise' in summary
    assert 'monitoring' in summary
    assert len(summary['diet']) >= 2


def test_history_endpoint_returns_prediction_records():
    client = app.test_client()
    response = client.get('/api/predict/history')

    assert response.status_code == 200
    data = response.get_json()
    assert 'history' in data
    assert isinstance(data['history'], list)
