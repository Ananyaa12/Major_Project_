# MongoDB Database Schema & Design

## Overview

MongoDB collections design for the Diabetes Risk Prediction system using the BRFSS 2015 dataset.

## Collections

### 1. Users Collection

Stores user authentication and profile information.

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "password_hash", "created_at"],
      properties: {
        _id: { bsonType: "objectId" },
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
          description: "User email (unique)"
        },
        username: {
          bsonType: "string",
          minLength: 3,
          maxLength: 50,
          description: "Display name"
        },
        password_hash: {
          bsonType: "string",
          description: "Bcrypt hashed password"
        },
        role: {
          bsonType: "string",
          enum: ["user", "admin", "doctor"],
          description: "User role"
        },
        profile: {
          bsonType: "object",
          properties: {
            full_name: { bsonType: "string" },
            phone: { bsonType: "string" },
            age_group: { bsonType: "int" },
            gender: { bsonType: "string", enum: [0, 1] },
            address: { bsonType: "string" },
            medical_id: { bsonType: "string" },
            doctor_name: { bsonType: "string" }
          }
        },
        preferences: {
          bsonType: "object",
          properties: {
            language: { bsonType: "string", default: "en" },
            email_notifications: { bsonType: "bool", default: true },
            theme: { bsonType: "string", enum: ["light", "dark"] }
          }
        },
        is_active: { bsonType: "bool", default: true },
        last_login: { bsonType: "date" },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  }
})

// Indexes
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ username: 1 })
db.users.createIndex({ created_at: -1 })
```

### 2. Predictions Collection

Stores all predictions made by users.

```javascript
db.createCollection("predictions", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "features", "prediction", "confidence", "created_at"],
      properties: {
        _id: { bsonType: "objectId" },
        user_id: { bsonType: "objectId", description: "Reference to users collection" },
        
        // BRFSS 2015 Features
        features: {
          bsonType: "object",
          properties: {
            HighBP: { bsonType: "int" },
            HighChol: { bsonType: "int" },
            CholCheck: { bsonType: "int" },
            BMI: { bsonType: "double" },
            Smoker: { bsonType: "int" },
            Stroke: { bsonType: "int" },
            HeartDiseaseorAttack: { bsonType: "int" },
            PhysActivity: { bsonType: "int" },
            Fruits: { bsonType: "int" },
            Veggies: { bsonType: "int" },
            HvyAlcoholConsump: { bsonType: "int" },
            AnyHealthcare: { bsonType: "int" },
            NoDocbcCost: { bsonType: "int" },
            GenHlth: { bsonType: "int" },
            MentHlth: { bsonType: "int" },
            PhysHlth: { bsonType: "int" },
            DiffWalk: { bsonType: "int" },
            Sex: { bsonType: "int" },
            Age: { bsonType: "int" },
            Education: { bsonType: "int" },
            Income: { bsonType: "int" }
          }
        },
        
        // Prediction Results
        prediction: {
          bsonType: "int",
          enum: [0, 1, 2],
          description: "0: No Diabetes, 1: Prediabetes, 2: Diabetes"
        },
        risk_level: {
          bsonType: "string",
          enum: ["Low Risk", "Moderate Risk", "High Risk", "Critical Risk"]
        },
        risk_score: { bsonType: "int", minimum: 0, maximum: 100 },
        severity: { bsonType: "int", minimum: 1, maximum: 4 },
        
        // Probabilities
        probability: {
          bsonType: "object",
          properties: {
            low_risk: { bsonType: "double" },
            moderate_risk: { bsonType: "double" },
            high_risk: { bsonType: "double" }
          }
        },
        confidence: {
          bsonType: "double",
          minimum: 0,
          maximum: 1,
          description: "Maximum probability score"
        },
        
        // Model Information
        model_used: {
          bsonType: "string",
          description: "Name of model that made prediction"
        },
        model_version: { bsonType: "string" },
        
        // SHAP Explanation
        shap_explanation: {
          bsonType: "object",
          properties: {
            base_value: { bsonType: "double" },
            feature_contributions: {
              bsonType: "array",
              items: {
                bsonType: "object",
                properties: {
                  feature: { bsonType: "string" },
                  value: { bsonType: "double" },
                  shap_value: { bsonType: "double" },
                  rank: { bsonType: "int" }
                }
              }
            }
          }
        },
        
        // Metadata
        ip_address: { bsonType: "string" },
        user_agent: { bsonType: "string" },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  }
})

// Indexes
db.predictions.createIndex({ user_id: 1, created_at: -1 })
db.predictions.createIndex({ prediction: 1 })
db.predictions.createIndex({ risk_level: 1 })
db.predictions.createIndex({ created_at: -1 })
```

### 3. Recommendations Collection

Stores personalized recommendations for each prediction.

```javascript
db.createCollection("recommendations", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "prediction_id", "risk_level", "created_at"],
      properties: {
        _id: { bsonType: "objectId" },
        user_id: { bsonType: "objectId", description: "Reference to users" },
        prediction_id: { bsonType: "objectId", description: "Reference to predictions" },
        
        // Risk Classification
        risk_level: {
          bsonType: "string",
          enum: ["Low Risk", "Moderate Risk", "High Risk", "Critical Risk"]
        },
        
        // Recommendations
        diet_plan: {
          bsonType: "array",
          items: { bsonType: "string" },
          description: "Array of diet recommendations"
        },
        exercise_plan: {
          bsonType: "array",
          items: { bsonType: "string" },
          description: "Array of exercise recommendations"
        },
        weight_management: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        clinical_recommendations: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        
        // Monitoring
        monitoring_schedule: {
          bsonType: "object",
          properties: {
            doctor_visit: { bsonType: "string" },
            glucose_check: { bsonType: "string" },
            blood_pressure: { bsonType: "string" },
            weight_check: { bsonType: "string" },
            physical_activity: { bsonType: "string" }
          }
        },
        
        // Preventive Measures
        preventive_measures: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        emergency_guidelines: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        
        // Status
        acknowledged: { bsonType: "bool", default: false },
        acknowledged_at: { bsonType: "date" },
        
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  }
})

// Indexes
db.recommendations.createIndex({ user_id: 1, created_at: -1 })
db.recommendations.createIndex({ prediction_id: 1 })
db.recommendations.createIndex({ risk_level: 1 })
```

### 4. Feedback Collection

Stores user feedback on predictions and recommendations.

```javascript
db.createCollection("feedback", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "prediction_id", "rating", "created_at"],
      properties: {
        _id: { bsonType: "objectId" },
        user_id: { bsonType: "objectId" },
        prediction_id: { bsonType: "objectId" },
        
        // Rating
        rating: {
          bsonType: "int",
          minimum: 1,
          maximum: 5,
          description: "User satisfaction rating"
        },
        
        // Comments
        comment: { bsonType: "string" },
        helpful: { bsonType: "bool" },
        
        // Feedback Categories
        accuracy_feedback: { bsonType: "string" },
        recommendation_feedback: { bsonType: "string" },
        ui_feedback: { bsonType: "string" },
        
        created_at: { bsonType: "date" }
      }
    }
  }
})

// Indexes
db.feedback.createIndex({ user_id: 1, created_at: -1 })
db.feedback.createIndex({ prediction_id: 1 })
db.feedback.createIndex({ rating: 1 })
```

### 5. Reports Collection

Stores generated reports (PDF, CSV, etc.).

```javascript
db.createCollection("reports", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "report_type", "generated_at"],
      properties: {
        _id: { bsonType: "objectId" },
        user_id: { bsonType: "objectId" },
        prediction_id: { bsonType: "objectId" },
        
        // Report Details
        report_type: {
          bsonType: "string",
          enum: ["pdf", "csv", "json"],
          description: "Report format"
        },
        title: { bsonType: "string" },
        description: { bsonType: "string" },
        
        // Content (store reference or binary)
        file_url: { bsonType: "string" },
        file_size: { bsonType: "long" },
        
        // Report Contents
        includes_prediction: { bsonType: "bool" },
        includes_explanation: { bsonType: "bool" },
        includes_recommendations: { bsonType: "bool" },
        includes_fairness: { bsonType: "bool" },
        
        // Status
        status: {
          bsonType: "string",
          enum: ["generating", "ready", "failed"]
        },
        
        generated_at: { bsonType: "date" },
        expires_at: { bsonType: "date" },
        download_count: { bsonType: "int", default: 0 }
      }
    }
  }
})

// Indexes
db.reports.createIndex({ user_id: 1, generated_at: -1 })
db.reports.createIndex({ report_type: 1 })
db.reports.createIndex({ expires_at: 1 })
```

### 6. Analytics Collection

Aggregated analytics data for dashboards.

```javascript
db.createCollection("analytics", {
  properties: {
    _id: { bsonType: "objectId" },
    date: { bsonType: "date" },
    
    // Prediction Stats
    total_predictions: { bsonType: "long" },
    predictions_by_risk: {
      low_risk: { bsonType: "long" },
      moderate_risk: { bsonType: "long" },
      high_risk: { bsonType: "long" }
    },
    
    // User Stats
    active_users: { bsonType: "long" },
    new_users: { bsonType: "long" },
    
    // Model Performance
    average_confidence: { bsonType: "double" },
    average_rating: { bsonType: "double" },
    
    // Fairness Metrics
    fairness_metrics: {
      demographic_parity: { bsonType: "object" },
      equal_opportunity: { bsonType: "object" }
    }
  }
})

// Indexes
db.analytics.createIndex({ date: -1 })
```

## Sample Queries

### Find all predictions for a user
```javascript
db.predictions.find({ 
  user_id: ObjectId("...") 
}).sort({ created_at: -1 }).limit(10)
```

### Get high-risk predictions
```javascript
db.predictions.find({
  risk_level: "High Risk",
  created_at: { $gte: new Date(Date.now() - 30*24*60*60*1000) }
}).sort({ created_at: -1 })
```

### Get recommendations by risk level
```javascript
db.recommendations.aggregate([
  { $match: { risk_level: "Moderate Risk" } },
  { $group: {
    _id: "$risk_level",
    count: { $sum: 1 },
    avg_acknowledged: { $avg: { $cond: ["$acknowledged", 1, 0] } }
  }}
])
```

### Average confidence by prediction
```javascript
db.predictions.aggregate([
  { $group: {
    _id: "$prediction",
    avg_confidence: { $avg: "$confidence" },
    count: { $sum: 1 }
  }},
  { $sort: { _id: 1 } }
])
```

## Backup Strategy

### Automated Backups (MongoDB Atlas)
- Daily snapshots retained for 7 days
- Weekly snapshots retained for 4 weeks
- Monthly snapshots retained for 12 months

### Manual Backup Command
```bash
mongodump --uri "mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/diabetes_db"
```

### Restore from Backup
```bash
mongorestore --uri "mongodb+srv://user:password@cluster0.xxxxx.mongodb.net" ./dump
```

## Performance Optimization

### Indexing Strategy
```javascript
// Optimize common queries
db.predictions.createIndex({ user_id: 1, created_at: -1 })
db.recommendations.createIndex({ user_id: 1, risk_level: 1 })
db.feedback.createIndex({ prediction_id: 1 })

// TTL index for automatic report cleanup (30 days)
db.reports.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 })
```

## Data Privacy & Security

### Sensitive Data Handling
- Password hashes using bcrypt (never store plain text)
- Medical IDs encrypted at rest
- HIPAA compliance for healthcare data
- GDPR right-to-deletion support

### Retention Policies
- User data: Retained as long as account active + 1 year after deletion
- Predictions: Retained for 5 years (medical records)
- Reports: Auto-delete after 30 days unless saved
- Feedback: Retained for analysis (anonymized after 1 year)

## Disaster Recovery

### RTO (Recovery Time Objective): < 1 hour
### RPO (Recovery Point Objective): < 1 day

- Multi-region replication enabled
- Read replicas in secondary region
- Automated failover
- Point-in-time recovery capability
