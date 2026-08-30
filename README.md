# Diabetes Risk Prediction Project

This project is a complete end-to-end diabetes risk prediction system. It starts with data preprocessing and machine learning, then adds explainability, fairness analysis, recommendations, and a working web application.

## What we performed

We built the project step by step:

1. Data understanding
   - Used the BRFSS 2015 diabetes health indicators dataset.
   - Prepared the dataset for training.

2. Model building
   - Trained multiple machine learning models for diabetes risk classification.
   - Compared accuracy, precision, recall, and F1-score.

3. Model comparison
   - Tested several algorithms and selected the best-performing approach for the final demo.

4. Explainability
   - Added SHAP-based explanation to show which features influenced the prediction.

5. Fairness analysis
   - Checked whether the model performed fairly across different groups.
   - Added fairness reports and evaluation metrics.

6. Recommendations
   - Built a recommendation module that suggests health and lifestyle actions based on risk level.

7. Backend API
   - Created a Flask backend to serve predictions and project outputs.

8. Frontend UI
   - Built a modern React + Vite interface with pages for home, prediction, dashboard, analytics, and fairness.
   - Added dark mode and a better user experience.

## Models used

We used and compared these models:

- Logistic Regression
- Decision Tree
- Random Forest
- SVM
- K-Nearest Neighbors
- Naive Bayes
- AdaBoost
- Gradient Boosting
- XGBoost
- LightGBM
- CatBoost

We also tested ensemble methods:

- Soft Voting
- Hard Voting
- Stacking

## Main tools and libraries

### Python
- pandas
- numpy
- scikit-learn
- xgboost
- lightgbm
- catboost
- imbalanced-learn
- shap
- joblib
- flask

### Frontend
- React
- Vite
- Tailwind CSS
- Framer Motion
- React Router
- Axios
- React Icons

## Project structure

- train_pipeline.py - full training pipeline
- train_quick.py - quick training script for the demo
- backend/app.py - Flask backend
- frontend/src - React frontend pages and components
- ml_pipeline - preprocessing, model training, explainability, fairness, and recommendations
- ml_pipeline/results - generated evaluation outputs
- ml_pipeline/trained_models - saved trained models

## How to run

### 1. Install Python packages
```bash
pip install -r requirements.txt
```

### 2. Train the model
```bash
python train_quick.py
```

Or use:
```bash
python train_pipeline.py
```

### 3. Start the backend
```bash
cd backend
python app.py
```

### 4. Start the frontend
```bash
cd frontend
npm install
npm run dev
```

Open:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## What this project demonstrates

This project shows:
- end-to-end machine learning workflow
- model training and comparison
- explainable AI
- fairness evaluation
- full-stack web integration
- a practical healthcare prediction demo

## Final outcome

The project successfully combines:
- machine learning
- explainability
- fairness analysis
- web-based prediction UI
- a complete academic and practical project experience
