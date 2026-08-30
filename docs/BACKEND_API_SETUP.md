# Backend Flask API Setup & Deployment

## Prerequisites

- Python 3.8+
- Flask, Flask-CORS, PyJWT
- Trained ML models (from ML pipeline)

## Installation

### 1. Install Backend Dependencies

```bash
pip install flask flask-cors pyjwt joblib numpy pandas scikit-learn
```

### 2. Ensure ML Models are Trained

```bash
python train_pipeline.py
```

This generates:
- `ml_pipeline/trained_models/` - All trained models
- `ml_pipeline/results/pipeline_results.json` - Model metadata
- `ml_pipeline/results/model_comparison.csv` - Performance comparison

### 3. Set Environment Variables

```bash
# On Windows
set FLASK_ENV=development
set SECRET_KEY=your-secret-key-change-in-production
set FLASK_DEBUG=1

# On macOS/Linux
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-change-in-production
export FLASK_DEBUG=1
```

### 4. Run Flask API

```bash
cd backend
python app.py
```

API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

#### Login
```
POST /api/auth/login
Body: {
  "username": "user@example.com",
  "password": "password"
}
Returns: {
  "token": "JWT_TOKEN",
  "user": "user@example.com"
}
```

#### Logout
```
POST /api/auth/logout
Headers: Authorization: Bearer JWT_TOKEN
```

### Health Check

```
GET /api/health
Returns: {
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000",
  "model_loaded": true
}
```

### Model Information

#### Get Model Info
```
GET /api/models/info
Returns: {
  "best_model": "random_forest",
  "model_performance": {...},
  "feature_names": [...],
  "n_features": 21
}
```

#### Get Model Comparison
```
GET /api/models/comparison
Returns: [
  {
    "Model": "random_forest",
    "Accuracy": 0.99,
    "Precision": 0.99,
    "Recall": 0.99,
    "F1-Score": 0.99,
    "ROC-AUC": 0.99
  },
  ...
]
```

### Predictions

#### Single Prediction
```
POST /api/predict
Headers: Authorization: Bearer JWT_TOKEN
Body: {
  "HighBP": 1,
  "HighChol": 1,
  "CholCheck": 1,
  "BMI": 40,
  ... (all 21 features)
}
Returns: {
  "prediction": 1,
  "risk_level": "Moderate Risk",
  "probability": {
    "low_risk": 0.2,
    "moderate_risk": 0.6,
    "high_risk": 0.2
  },
  "confidence": 0.6
}
```

#### Batch Prediction
```
POST /api/predict/batch
Headers: Authorization: Bearer JWT_TOKEN
Body: {
  "patients": [
    {"HighBP": 1, "HighChol": 1, ...},
    {"HighBP": 0, "HighChol": 0, ...}
  ]
}
Returns: {
  "predictions": [...],
  "count": 2
}
```

### Explainability

#### Get Feature Importance
```
GET /api/explainability/feature-importance
Returns: {
  "features": [
    {"Feature": "BMI", "Importance": 0.15},
    ...
  ],
  "count": 21
}
```

### Fairness

#### Get Fairness Report
```
GET /api/fairness/report
Returns: {
  "report": "FAIRNESS EVALUATION REPORT\n..."
}
```

### Analytics

#### Get Predictions (user's history)
```
GET /api/analytics/predictions
Headers: Authorization: Bearer JWT_TOKEN
Returns: {
  "user": "user@example.com",
  "predictions": [],
  "total_count": 0
}
```

#### Get Dashboard Data
```
GET /api/analytics/dashboard
Headers: Authorization: Bearer JWT_TOKEN
Returns: {
  "model_performance": {...},
  "test_set_size": 51350,
  "feature_count": 21
}
```

## Error Handling

All errors return JSON format:
```json
{
  "message": "Error description"
}
```

HTTP Status Codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
- 503: Service Unavailable

## Testing the API

### Using cURL

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com",
    "password": "password123"
  }'

# Get Token
TOKEN="your_token_here"

# Make Prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "HighBP": 1,
    "HighChol": 1,
    ... (all features)
  }'
```

### Using Python

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "test@example.com", "password": "password123"}
)
token = response.json()["token"]

# Make Prediction
headers = {"Authorization": f"Bearer {token}"}
features = {
    "HighBP": 1,
    "HighChol": 1,
    ... # all 21 features
}

response = requests.post(
    f"{BASE_URL}/predict",
    headers=headers,
    json=features
)
print(response.json())
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

### Using Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]
```

Build and run:
```bash
docker build -t diabetes-api .
docker run -p 5000:5000 diabetes-api
```

### Security Considerations

1. Change SECRET_KEY in production
2. Use environment variables for configuration
3. Implement rate limiting
4. Add input validation (already present)
5. Use HTTPS in production
6. Implement proper authentication with database
7. Log all API requests
8. Use API keys instead of username/password for production

## Monitoring

Add logging:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

## Deployment on Render

1. Push to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set environment variables:
   - FLASK_ENV=production
   - SECRET_KEY=your-secret
5. Deploy

See DEPLOYMENT_GUIDE.md for full deployment instructions.
