# Diabetes Risk Prediction - ML Pipeline Installation & Setup

## Prerequisites

- Python 3.8+
- pip or conda
- 8GB RAM minimum
- 2GB disk space

## Installation Steps

### 1. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Dataset

Ensure `diabetes_012_health_indicators_BRFSS2015.csv` is in the project root directory.

### 4. Run ML Pipeline

```bash
# This will:
# - Load and preprocess data
# - Train 11 base models
# - Build 3 ensemble models
# - Evaluate all models
# - Generate SHAP explanations
# - Evaluate fairness metrics
# - Save all results

python train_pipeline.py
```

### 5. Expected Output

After running the pipeline, you should see:
- ✅ Model training logs
- ✅ Performance comparison table
- ✅ SHAP feature importance
- ✅ Fairness evaluation report
- ✅ Saved models in `ml_pipeline/trained_models/`
- ✅ Results in `ml_pipeline/results/`

## Project Structure

```
├── diabetes_012_health_indicators_BRFSS2015.csv  # Dataset
├── train_pipeline.py                               # Main ML pipeline
├── ml_pipeline/
│   ├── preprocessing/
│   │   ├── data_loader.py
│   │   ├── preprocessor.py
│   │   └── feature_engineering.py
│   ├── models/
│   │   ├── model_trainer.py
│   │   └── recommendation_engine.py
│   ├── explainability/
│   │   └── shap_explainer.py
│   ├── fairness/
│   │   └── fairness_evaluator.py
│   ├── trained_models/              # Saved models (after training)
│   └── results/                      # Pipeline results (after training)
├── backend/
│   ├── app.py                        # Flask REST API
│   ├── config.py
│   └── __init__.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   ├── postcss.config.js
│   └── package.json
├── database/                         # MongoDB schemas
├── docs/                             # Documentation
└── requirements.txt                  # Python dependencies
```

## Model Training Details

### Base Models (11 total)
1. Logistic Regression
2. Decision Tree
3. Random Forest
4. Support Vector Machine (SVM)
5. K-Nearest Neighbors (KNN)
6. Naive Bayes
7. XGBoost
8. LightGBM
9. CatBoost
10. AdaBoost
11. Gradient Boosting

### Ensemble Models (3 total)
1. Soft Voting Ensemble
2. Hard Voting Ensemble
3. Stacking Ensemble

### Performance Metrics
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-Score (weighted)
- ROC-AUC (one-vs-rest)

## Preprocessing Steps

1. **Missing Value Handling**: Mean imputation
2. **Outlier Detection**: IQR method
3. **Feature Scaling**: StandardScaler
4. **Class Imbalance**: SMOTE
5. **Train-Test Split**: 80-20 stratified split

## Explainability (SHAP)

The pipeline generates SHAP explanations including:
- Global feature importance
- Individual prediction explanations
- Summary plots
- Waterfall plots
- Force plots
- Dependence plots

## Fairness Evaluation

Fairness metrics evaluated across demographic groups (Gender, Age, Education, Income):
- Demographic Parity Difference (DPD)
- Equal Opportunity Difference (EOD)
- Disparate Impact Ratio (DIR)
- Group-level accuracy, precision, recall, F1

## Troubleshooting

### Issue: ModuleNotFoundError
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: CUDA/GPU not found
The pipeline runs on CPU by default. For GPU support, install CUDA-compatible versions:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Issue: Memory error during SHAP
Reduce the number of samples:
```python
# In train_pipeline.py, modify the SHAP line:
explainer.get_feature_importance(X_test[:5000], top_n=10)
```

## Performance Optimization

- **Parallel Processing**: Models are trained in parallel using n_jobs=-1
- **Sampling**: Use subset of data for SHAP if memory is limited
- **Model Selection**: Top performing models are used for ensemble

## Next Steps

1. Start the backend Flask API
2. Launch the frontend React application
3. Configure MongoDB for production
4. Deploy to Render (backend) and Vercel (frontend)

See DEPLOYMENT_GUIDE.md for detailed deployment instructions.
