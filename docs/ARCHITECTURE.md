# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       Users                                  │
│                  (Healthcare, Patients)                      │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                  Frontend Layer (Vercel)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  React + Vite + Tailwind CSS                        │   │
│  │  - Landing Page                                     │   │
│  │  - Prediction Form                                  │   │
│  │  - Dashboard & Analytics                           │   │
│  │  - Fairness Reports                                │   │
│  │  - Model Comparison                                │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │ REST API + JWT
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                  Backend Layer (Render)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Flask REST API                                     │   │
│  │  - Authentication (JWT)                            │   │
│  │  - Prediction Endpoint                             │   │
│  │  - SHAP Explanations                               │   │
│  │  - Fairness Metrics                                │   │
│  │  - Analytics                                       │   │
│  │  - Recommendation Engine                           │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │ Query/Read
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                ML Pipeline Layer (Backend)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Training Pipeline (Scikit-Learn, XGBoost, etc.)   │   │
│  │  ✓ Data Preprocessing                              │   │
│  │  ✓ Model Training                                  │   │
│  │  ✓ Ensemble Building                               │   │
│  │  ✓ SHAP Explainability                             │   │
│  │  ✓ Fairness Evaluation                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Trained Models (Joblib Serialized)                │   │
│  │  - Random Forest                                   │   │
│  │  - XGBoost, LightGBM, CatBoost                     │   │
│  │  - Ensemble Models (Voting, Stacking)             │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │ Read/Write
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              Database Layer (MongoDB Atlas)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Collections:                                       │   │
│  │  - users (Authentication & profiles)              │   │
│  │  - predictions (User predictions)                  │   │
│  │  - recommendations (Personalized advice)          │   │
│  │  - feedback (User feedback)                        │   │
│  │  - reports (Generated reports)                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Frontend Architecture

```
Frontend (React + Vite)
│
├── Pages (Route Handlers)
│   ├── HomePage - Landing page
│   ├── LoginPage - Authentication
│   ├── DashboardPage - User analytics
│   ├── PredictionPage - Risk prediction
│   ├── FairnessPage - Fairness report
│   ├── AnalyticsPage - Model comparison
│   └── AboutPage - Project info
│
├── Components (Reusable UI)
│   ├── Navigation - Header/navbar
│   ├── Hero - Landing hero section
│   └── [Other components]
│
├── Services
│   └── api.js - Axios HTTP client
│       ├── authService
│       ├── predictionService
│       ├── explainabilityService
│       ├── fairnessService
│       └── analyticsService
│
├── Context (State Management)
│   └── AuthContext - User auth state
│
└── Utils
    └── Styling (Tailwind CSS, CSS)
```

### 2. Backend Architecture

```
Backend (Flask)
│
├── app.py (Main Flask Application)
│   └── CORS enabled for cross-origin requests
│
├── Routes (API Endpoints)
│   ├── Authentication Routes
│   │   ├── POST /api/auth/login
│   │   └── POST /api/auth/logout
│   │
│   ├── Prediction Routes
│   │   ├── POST /api/predict
│   │   └── POST /api/predict/batch
│   │
│   ├── Explainability Routes
│   │   └── GET /api/explainability/feature-importance
│   │
│   ├── Fairness Routes
│   │   └── GET /api/fairness/report
│   │
│   └── Analytics Routes
│       ├── GET /api/analytics/dashboard
│       └── GET /api/analytics/predictions
│
├── Middleware
│   └── JWT Authentication decorator
│
└── Model Loading
    └── Joblib (loads trained models)
```

### 3. ML Pipeline Architecture

```
ML Pipeline
│
├── Data Loading
│   └── DataLoader - BRFSS CSV loading
│
├── Preprocessing
│   ├── Preprocessor
│   │   ├── Missing value handling
│   │   ├── Outlier detection
│   │   ├── Feature scaling
│   │   ├── SMOTE (class balancing)
│   │   └── Train-test split
│   │
│   └── FeatureEngineer
│       ├── Correlation analysis
│       ├── Feature selection (SelectKBest)
│       ├── PCA analysis
│       ├── Interaction features
│       └── Polynomial features
│
├── Model Training
│   └── ModelTrainer
│       ├── Base Models (11 types)
│       │   ├── Logistic Regression
│       │   ├── Decision Tree
│       │   ├── Random Forest
│       │   ├── SVM
│       │   ├── KNN
│       │   ├── Naive Bayes
│       │   ├── XGBoost
│       │   ├── LightGBM
│       │   ├── CatBoost
│       │   ├── AdaBoost
│       │   └── Gradient Boosting
│       │
│       └── Ensemble Models (3 types)
│           ├── Soft Voting
│           ├── Hard Voting
│           └── Stacking
│
├── Explainability (SHAP)
│   └── SHAPExplainer
│       ├── Global explanations
│       ├── Local explanations
│       ├── Feature importance
│       ├── Summary plots
│       ├── Waterfall plots
│       ├── Force plots
│       └── Dependence plots
│
├── Fairness Evaluation
│   └── FairnessEvaluator
│       ├── Demographic Parity Difference
│       ├── Equal Opportunity Difference
│       ├── Disparate Impact Ratio
│       ├── Group accuracy metrics
│       └── Bias detection
│
└── Recommendations
    └── RecommendationEngine
        ├── Risk classification
        ├── Diet recommendations
        ├── Exercise plans
        ├── Weight management
        ├── Clinical guidance
        ├── Monitoring schedule
        ├── Preventive measures
        └── Emergency guidelines
```

## Data Flow Diagrams

### 1. Prediction Flow

```
User Input (21 Features)
    ↓
Frontend Form Validation
    ↓
HTTP POST /api/predict
    ↓
Backend JWT Validation
    ↓
Load Trained Model
    ↓
Feature Preprocessing
    ↓
ML Model Prediction
    ↓
Generate Prediction
├─ Risk Level (0, 1, 2)
├─ Confidence Score
├─ Probability Distribution
└─ SHAP Explanation
    ↓
Generate Recommendations
├─ Diet Plan
├─ Exercise Plan
├─ Weight Management
├─ Clinical Guidance
├─ Monitoring Schedule
└─ Preventive Measures
    ↓
Save to Database
    ↓
Return JSON Response
    ↓
Frontend Display
```

### 2. Model Training Flow

```
BRFSS Dataset (250K samples)
    ↓
Data Loading (21 features)
    ↓
Preprocessing
├─ Handle missing values
├─ Detect outliers
├─ Scale features
└─ SMOTE balancing
    ↓
Train-Test Split (80-20)
    ↓
Train Base Models (11 types)
├─ Parallel training
└─ Save checkpoints
    ↓
Evaluate Base Models
├─ Accuracy, Precision, Recall, F1
└─ ROC-AUC
    ↓
Build Ensemble Models (3 types)
├─ Voting ensemble
└─ Stacking ensemble
    ↓
Evaluate Ensembles
    ↓
SHAP Explainability Analysis
├─ Global feature importance
└─ Local explanations
    ↓
Fairness Evaluation
├─ Demographic group analysis
├─ Bias detection
└─ Fairness metrics
    ↓
Model Selection
├─ Choose best performing
└─ Save with Joblib
    ↓
Generate Results Report
├─ Model comparison
├─ Performance metrics
└─ Fairness report
```

### 3. Authentication Flow

```
User Credentials (email, password)
    ↓
POST /api/auth/login
    ↓
Validate credentials
    ↓
Generate JWT Token
    ↓
Return token to frontend
    ↓
Frontend stores token in localStorage
    ↓
For protected endpoints:
    ├─ Include token in header
    ├─ Backend validates token
    ├─ Extract user info from JWT
    └─ Proceed with request
    ↓
Token expires after 24 hours
    ↓
Redirect to login on expiration
```

## Database Schema (MongoDB)

```
users
├─ _id (ObjectId)
├─ username (string)
├─ email (string, unique)
├─ password_hash (string)
├─ created_at (timestamp)
├─ updated_at (timestamp)
└─ profile
   ├─ full_name
   ├─ age
   ├─ gender
   └─ phone

predictions
├─ _id (ObjectId)
├─ user_id (ObjectId, ref: users)
├─ features (object) - All 21 BRFSS features
├─ prediction (int) - 0, 1, or 2
├─ risk_level (string) - Low/Moderate/High
├─ probability (object)
│  ├─ low_risk
│  ├─ moderate_risk
│  └─ high_risk
├─ confidence (float)
├─ shap_explanation (object)
├─ created_at (timestamp)
└─ updated_at (timestamp)

recommendations
├─ _id (ObjectId)
├─ prediction_id (ObjectId, ref: predictions)
├─ user_id (ObjectId, ref: users)
├─ risk_level (string)
├─ diet_plan (array)
├─ exercise_plan (array)
├─ weight_management (array)
├─ clinical_recommendations (array)
├─ monitoring_schedule (object)
├─ preventive_measures (array)
├─ emergency_guidelines (array)
└─ created_at (timestamp)

feedback
├─ _id (ObjectId)
├─ user_id (ObjectId, ref: users)
├─ prediction_id (ObjectId, ref: predictions)
├─ rating (int) - 1-5
├─ comment (string)
├─ created_at (timestamp)

reports
├─ _id (ObjectId)
├─ user_id (ObjectId, ref: users)
├─ prediction_id (ObjectId, ref: predictions)
├─ report_type (string) - pdf, csv, json
├─ content (binary or string)
├─ generated_at (timestamp)
```

## Scalability Considerations

### Horizontal Scaling

```
Frontend (Vercel)
├─ Auto-scales with traffic
├─ Global CDN
└─ No additional setup needed

Backend (Render/Kubernetes)
├─ Multi-instance deployment
├─ Load balancing
├─ Database connection pooling
└─ Horizontal pod autoscaling

Database (MongoDB)
├─ Replication sets
├─ Sharding
├─ Read replicas
└─ Backup strategy
```

### Performance Optimization

1. **Caching**: Redis cache for predictions
2. **Batch Predictions**: Optimize for multiple users
3. **Model Optimization**: Model quantization, pruning
4. **Database Indexing**: Indexes on frequent queries
5. **API Optimization**: Response compression, pagination

## Security Architecture

```
Security Layers:
│
├─ Network Layer
│  ├─ HTTPS/TLS encryption
│  ├─ CORS policy
│  └─ Rate limiting
│
├─ Authentication Layer
│  ├─ JWT tokens (24h expiration)
│  ├─ Password hashing (bcrypt)
│  └─ Secure session management
│
├─ Authorization Layer
│  ├─ Role-based access control
│  ├─ Resource-level permissions
│  └─ User data isolation
│
├─ Data Layer
│  ├─ Input validation
│  ├─ SQL injection prevention
│  └─ MongoDB injection prevention
│
└─ Infrastructure Layer
   ├─ Environment variables (secrets)
   ├─ Firewall rules
   ├─ IP whitelisting (MongoDB)
   └─ Regular security audits
```

## Deployment Architecture

```
Development Environment
├─ Local machine
├─ Git repository (GitHub)
└─ Local testing

Staging Environment (Optional)
├─ Similar to production
├─ Pre-deployment testing
└─ Performance validation

Production Environment
├─ Frontend → Vercel
├─ Backend → Render
└─ Database → MongoDB Atlas
```

## Monitoring & Observability

```
Monitoring Stack:
│
├─ Error Tracking
│  ├─ Sentry (exceptions)
│  └─ Application logs
│
├─ Performance Monitoring
│  ├─ Response times
│  ├─ Throughput
│  └─ Resource usage
│
├─ Health Checks
│  ├─ API health endpoint
│  ├─ Database connectivity
│  └─ External service status
│
└─ Alerting
   ├─ Error rate threshold
   ├─ Performance degradation
   ├─ Uptime monitoring
   └─ Resource constraints
```

---

This architecture ensures:
✅ Scalability
✅ Reliability
✅ Security
✅ Maintainability
✅ Performance
