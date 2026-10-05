# DiabetesAI - Explainable Diabetes Risk Prediction

This project is a complete end-to-end diabetes risk prediction system that combines machine learning, model explainability, fairness analysis, health recommendations, and a web application. The system is designed to predict diabetes risk from BRFSS-style health indicators and present results in a user-friendly dashboard.

## Project goal

The goal of this project was to build a full-stack AI healthcare demo that shows:

- how a diabetes risk model is trained
- how predictions are explained to users
- how fairness is evaluated across groups
- how recommendation logic supports the user
- how a frontend and backend connect in a real application

---

## What I implemented

### 1. Machine learning pipeline

I built the core ML workflow for the diabetes classification problem.

- Data loading and preprocessing in the ml_pipeline package
- Training scripts for quick and full pipeline runs
- Model evaluation and comparison
- Saved trained model artifacts in ml_pipeline/trained_models
- Result export to ml_pipeline/results

Files involved:
- train_quick.py
- train_pipeline.py
- ml_pipeline/preprocessing/
- ml_pipeline/models/
- ml_pipeline/results/

### 2. Model training and comparison

The project includes a model comparison workflow for multiple classifiers and supports evaluating metrics such as:

- Accuracy
- Precision
- Recall
- F1-score

The generated comparison results are stored in:
- ml_pipeline/results/model_comparison.csv

### 3. Explainability with SHAP

I added explainability so a user can understand why the model gave a given prediction.

This includes:
- SHAP-based feature importance logic
- explanation summaries for each prediction
- top contributing factors returned by the backend

Files involved:
- ml_pipeline/explainability/shap_explainer.py
- backend/app.py
- frontend/src/pages/PredictionPage.jsx
- frontend/src/pages/AnalyticsPage.jsx

### 4. Recommendation engine

I implemented a recommendation module that generates personalized suggestions based on risk level and health profile.

Examples include:
- diet suggestions
- exercise suggestions
- weight management advice
- clinical follow-up recommendations
- monitoring schedule

Files involved:
- ml_pipeline/models/recommendation_engine.py
- backend/app.py

### 5. Fairness evaluation

I included fairness analysis so the system checks whether predictions differ across demographic groups.

This covers:
- fairness summary data
- group-based comparison metrics
- reporting section for fairness interpretation

Files involved:
- ml_pipeline/fairness/fairness_evaluator.py
- ml_pipeline/results/fairness_report.txt
- backend/app.py
- frontend/src/pages/FairnessPage.jsx

### 6. Backend API

The backend is a Flask application that serves the trained model and provides REST endpoints for prediction and analytics.

Implemented API areas:
- health check
- authentication mock flow
- prediction engine
- prediction history
- model comparison
- feature importance
- fairness summary
- dashboard data

Main backend file:
- backend/app.py

### 7. Frontend pages and UI

I built a complete React + Vite frontend with multiple pages for different project functions.

#### Home page
File:
- frontend/src/pages/HomePage.jsx

What it does:
- landing page
- hero section
- feature highlights
- project overview

#### About page
File:
- frontend/src/pages/AboutPage.jsx

What it does:
- project description
- methodology overview
- explainability and fairness context

#### Dashboard page
File:
- frontend/src/pages/DashboardPage.jsx

What it does:
- model summary cards
- performance metrics
- dataset snapshot
- operational model overview

#### Prediction page
File:
- frontend/src/pages/PredictionPage.jsx

What it does:
- patient feature form
- live diabetes prediction
- probability bars
- SHAP insight panel
- personal recommendations
- recent prediction history
- export report as text file

#### Fairness page
File:
- frontend/src/pages/FairnessPage.jsx

What it does:
- fairness group comparison
- metric display
- fairness status note
- report formatting

#### Analytics page
File:
- frontend/src/pages/AnalyticsPage.jsx

What it does:
- model comparison table
- top feature importance visualization
- explainable AI analysis summary

#### Login page
File:
- frontend/src/pages/LoginPage.jsx

What it does:
- login form for app access

#### Main app router
File:
- frontend/src/App.jsx

What it does:
- route setup for all pages
- navigation and page structure

### 8. Navigation and theme system

I also implemented a responsive navigation and theme selector.

Files:
- frontend/src/components/Navigation.jsx

Features:
- desktop and mobile navigation
- login/logout state handling
- theme switching

---

## Project structure

```text
Major_Project/
├── backend/
│   ├── app.py
│   ├── __init__.py
│   ├── tests/
│   │   └── test_prediction_flow.py
│   └── ...
├── docs/
│   ├── ARCHITECTURE.md
│   ├── BACKEND_API_SETUP.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── FRONTEND_SETUP.md
│   └── ML_PIPELINE_SETUP.md
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── ...
├── ml_pipeline/
│   ├── explainability/
│   ├── fairness/
│   ├── models/
│   ├── preprocessing/
│   ├── results/
│   ├── trained_models/
│   └── visualizations/
├── diabetes_012_health_indicators_BRFSS2015.csv
├── inspect_dataset.py
├── predict_test.py
├── requirements.txt
├── train_pipeline.py
├── train_quick.py
├── README.md
└── README_new.md (removed)
```

---

## Main technologies used

### Python stack
- pandas
- numpy
- scikit-learn
- joblib
- shap
- flask
- flask-cors
- pyjwt
- imbalanced-learn
- fairlearn
- xgboost
- lightgbm
- catboost

### Frontend stack
- React
- Vite
- Tailwind CSS
- Framer Motion
- React Router
- Axios
- React Icons

---

## What I did by page

### Home page
Created a polished landing page with feature highlights and healthcare-focused messaging.

### About page
Added project explanation and context about the AI healthcare workflow.

### Dashboard page
Built a live dashboard showing model metrics and training outcomes.

### Prediction page
Created the main interaction area where users enter health indicators and receive:
- prediction label
- confidence score
- class probabilities
- explanation summary
- recommendation guidance
- report export
- prediction history

### Fairness page
Added demographic fairness comparison and explanation of model behavior across groups.

### Analytics page
Added a model comparison table and top feature importance view for model introspection.

### Login page
Added a starter authentication flow for app access.

---

## Backend API highlights

Implemented endpoints include:

- GET /api/health
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/models/info
- GET /api/models/comparison
- POST /api/predict
- GET /api/predict/history
- GET /api/explainability/feature-importance
- GET /api/fairness/report
- GET /api/fairness/summary
- GET /api/analytics/dashboard

---

## Run the project

### 1. Install Python dependencies

```bash
cd "c:\Users\DELL\Desktop\Major_Project"
"C:\Users\DELL\AppData\Local\Programs\Python\Python311\python.exe" -m pip install -r requirements.txt
```

### 2. Train the model

```bash
cd "c:\Users\DELL\Desktop\Major_Project"
"C:\Users\DELL\AppData\Local\Programs\Python\Python311\python.exe" train_quick.py
```

### 3. Start the backend

```bash
cd "c:\Users\DELL\Desktop\Major_Project\backend"
"C:\Users\DELL\AppData\Local\Programs\Python\Python311\python.exe" app.py
```

### 4. Start the frontend

```bash
cd "c:\Users\DELL\Desktop\Major_Project\frontend"
npm install
npm run dev -- --host 0.0.0.0
```

Then open:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

---

## Final summary

This project now includes a functional diabetes risk prediction system with:

- machine learning model training
- explainability and SHAP-style interpretation
- recommendation generation
- fairness analysis
- Flask backend API
- modern React frontend
- prediction history and report export
- responsive dashboard and analytics pages

This is a complete demonstration of an end-to-end AI healthcare application from model to user-facing interface.
