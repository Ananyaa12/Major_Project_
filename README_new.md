# Diabetes Risk Prediction Project

This project is a complete end-to-end machine learning and web application built for diabetes risk prediction. It starts from data preprocessing and model training, then moves to explainability, fairness evaluation, recommendation generation, and finally a working frontend-backend demo.

## What we performed

We built the project in steps:

1. Data understanding
   - Used the BRFSS 2015 diabetes health indicators dataset.
   - Cleaned and prepared the data for training.

2. Machine learning model training
   - Trained multiple classification models for diabetes risk prediction.
   - Compared their performance using accuracy, precision, recall, and F1-score.

3. Model comparison and selection
   - Tested several models and selected the best-performing approach for the final demo.

4. Explainability with SHAP
   - Added explainable AI to show which features influenced the prediction.
   - This helps users understand why the model gave a certain result.

5. Fairness analysis
   - Checked whether the model behaves fairly across different demographic groups.
   - Added fairness metrics and reports.

6. Recommendation engine
   - Built a simple recommendation system that suggests lifestyle and health actions based on risk level.

7. Backend API
   - Created a Flask backend to serve predictions and model outputs.

8. Frontend UI
   - Built a modern React + Vite frontend with pages for home, prediction, dashboard, analytics, and fairness.
   - Added a polished UI with dark mode and better user experience.

## Models used

We used and compared several models:

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
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

- [train_pipeline.py](train_pipeline.py) - full training pipeline
- [train_quick.py](train_quick.py) - quick training script for local demo
- [backend/app.py](backend/app.py) - Flask backend
- [frontend/src](frontend/src) - React frontend pages and components
- [ml_pipeline](ml_pipeline) - preprocessing, training, explainability, fairness, and recommendation code
- [ml_pipeline/results](ml_pipeline/results) - generated evaluation reports and outputs
- [ml_pipeline/trained_models](ml_pipeline/trained_models) - saved trained models

## How to run the project

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model
```bash
python train_quick.py
```

Or for a fuller training run:
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

Then open:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## What this project demonstrates

This project shows:
- end-to-end machine learning workflow
- model training and comparison
- explainable AI
- fairness checking
- full-stack deployment style integration
- a working demo for healthcare risk prediction

## Final outcome

The project successfully combines:
- machine learning
- explainability
- fairness evaluation
- web-based prediction UI
- a practical demo for diabetes risk assessment

This is a complete academic and practical project that goes from a simple prediction model to a full real-world-style application.
