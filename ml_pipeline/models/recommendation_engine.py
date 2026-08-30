"""
Personalized Recommendation Engine
Generates lifestyle recommendations based on risk level and health metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class RecommendationEngine:
    """Generate personalized health recommendations."""
    
    def __init__(self):
        """Initialize recommendation engine with medical guidelines."""
        self.risk_levels = {
            0: 'Low Risk',
            1: 'Moderate Risk',
            2: 'High Risk',
            3: 'Critical Risk',
        }
        
    def classify_risk_level(self, prediction_proba: np.ndarray, 
                           prediction: int) -> Dict[str, Any]:
        """
        Classify risk level based on prediction and probability.
        
        Args:
            prediction_proba: Predicted probabilities for each class
            prediction: Predicted class
            
        Returns:
            Dictionary with risk classification
        """
        confidence = np.max(prediction_proba)
        
        # Map 0, 1, 2 to risk levels
        if prediction == 0:
            risk_level = 'Low Risk'
            risk_score = int(confidence * 30)
            severity = 1
        elif prediction == 1:
            risk_level = 'Moderate Risk'
            risk_score = 30 + int(confidence * 35)
            severity = 2
        else:  # prediction == 2
            risk_level = 'High Risk'
            risk_score = 65 + int(confidence * 35)
            severity = 3
        
        return {
            'risk_level': risk_level,
            'risk_score': min(100, risk_score),
            'severity': severity,
            'confidence': float(confidence),
            'prediction_proba': prediction_proba.tolist(),
        }
    
    def generate_diet_plan(self, bmi: float, income: int, 
                          fruit_intake: int, veggie_intake: int,
                          risk_level: str) -> List[str]:
        """
        Generate personalized diet recommendations.
        
        Args:
            bmi: Body Mass Index
            income: Income level
            fruit_intake: Current fruit consumption
            veggie_intake: Current vegetable consumption
            risk_level: Risk classification
            
        Returns:
            List of diet recommendations
        """
        recommendations = []
        
        # BMI-based recommendations
        if bmi >= 30:
            recommendations.append("🍎 Focus on calorie-controlled, nutrient-dense foods")
            recommendations.append("🥗 Increase fiber intake - aim for 25-30g daily")
            recommendations.append("🚫 Reduce sugar and refined carbohydrates")
            recommendations.append("🥤 Replace sugary drinks with water or unsweetened beverages")
        elif bmi >= 25:
            recommendations.append("⚖️ Maintain balanced macronutrient distribution")
            recommendations.append("🥗 Include whole grains in 50% of your meals")
        
        # Fruit and vegetable intake
        if fruit_intake == 0:
            recommendations.append("🍌 Start consuming 1-2 servings of fruit daily")
            recommendations.append("🍊 Include variety: berries, citrus, apples")
        
        if veggie_intake == 0:
            recommendations.append("🥦 Start with 2-3 servings of vegetables daily")
            recommendations.append("🥕 Choose colorful vegetables for variety and nutrients")
        
        # Risk-specific recommendations
        if risk_level in ['High Risk', 'Critical Risk']:
            recommendations.append("🏥 Consult a registered dietitian for personalized meal plan")
            recommendations.append("📊 Monitor daily carbohydrate intake")
            recommendations.append("🧂 Reduce sodium intake to <2300mg per day")
        
        # Income-aware recommendations
        if income <= 3:  # Lower income groups
            recommendations.append("💰 Look for affordable whole grains and frozen vegetables")
            recommendations.append("🏪 Buy seasonal produce for better prices")
            recommendations.append("🎯 Focus on nutrient-dense budget-friendly foods: beans, lentils, eggs")
        
        return recommendations
    
    def generate_exercise_plan(self, physical_activity: int, age: int, 
                              general_health: int, risk_level: str) -> List[str]:
        """
        Generate personalized exercise recommendations.
        
        Args:
            physical_activity: Current physical activity level
            age: Age group
            general_health: General health rating
            risk_level: Risk classification
            
        Returns:
            List of exercise recommendations
        """
        recommendations = []
        
        # Age-based base recommendations
        if age >= 8:  # Age 60+
            recommendations.append("🚶 Start with 20-30 minutes of moderate walking daily")
            recommendations.append("💪 Include strength training 2-3 times per week")
            recommendations.append("⚠️ Consult doctor before starting new exercise program")
        else:
            recommendations.append("🏃 Aim for 150 minutes of moderate aerobic activity weekly")
            recommendations.append("💪 Include resistance training 2-3 times per week")
        
        # Based on current activity level
        if physical_activity == 0:
            recommendations.append("⭐ Start small: Begin with 10-15 minute walks")
            recommendations.append("📈 Gradually increase duration by 5 minutes weekly")
            recommendations.append("🎯 Set realistic goals - consistency matters more than intensity")
        else:
            recommendations.append("✅ Continue maintaining regular physical activity")
            recommendations.append("🔄 Mix cardio and strength training for best results")
        
        # Health status considerations
        if general_health >= 4:  # Fair or poor health
            recommendations.append("🏥 Consult healthcare provider about exercise safety")
            recommendations.append("🧘 Consider low-impact exercises: swimming, cycling, yoga")
        
        # Risk-specific
        if risk_level in ['High Risk', 'Critical Risk']:
            recommendations.append("⚠️ Start exercise under medical supervision")
            recommendations.append("📱 Monitor heart rate and stop if experiencing chest pain/dizziness")
            recommendations.append("🚑 Have emergency contact information readily available")
        
        return recommendations
    
    def generate_weight_management_plan(self, bmi: float, age: int, 
                                       general_health: int) -> List[str]:
        """
        Generate weight management recommendations.
        
        Args:
            bmi: Current BMI
            age: Age group
            general_health: General health rating
            
        Returns:
            List of weight management recommendations
        """
        recommendations = []
        
        if bmi < 18.5:
            recommendations.append("↗️ Your BMI is underweight - focus on balanced nutrition")
            recommendations.append("🥗 Consult doctor to rule out health concerns")
        elif bmi < 25:
            recommendations.append("✅ Your BMI is in the healthy range")
            recommendations.append("🎯 Focus on maintaining current weight through balanced lifestyle")
        elif bmi < 30:
            recommendations.append("⚖️ Your BMI indicates overweight status")
            recommendations.append("📉 Aim to lose 5-10% of body weight gradually (0.5-1 lb/week)")
            recommendations.append("🍽️ Create a 500 calorie daily deficit through diet and exercise")
        else:
            recommendations.append("🚨 Your BMI indicates obesity")
            recommendations.append("📉 Target weight loss of 1-2 lbs per week")
            recommendations.append("🏥 Consider working with a healthcare team for weight management")
            recommendations.append("💊 Discuss medical weight loss options with your doctor")
        
        # Age-specific considerations
        if age >= 8:  # 60+
            recommendations.append("👵 Older adults: Preserve muscle mass during weight loss")
            recommendations.append("🥛 Ensure adequate protein intake: 1.2-1.6g per kg body weight")
        
        return recommendations
    
    def generate_clinical_recommendations(self, risk_level: str, 
                                         high_bp: int, stroke: int, 
                                         heart_disease: int) -> List[str]:
        """
        Generate clinical recommendations for healthcare providers.
        
        Args:
            risk_level: Diabetes risk classification
            high_bp: High blood pressure status
            stroke: Previous stroke status
            heart_disease: Heart disease status
            
        Returns:
            List of clinical recommendations
        """
        recommendations = []
        
        # Risk-based recommendations
        if risk_level in ['High Risk', 'Critical Risk']:
            recommendations.append("🏥 Schedule comprehensive diabetes screening")
            recommendations.append("🧪 Order HbA1c test (>6.5% indicates diabetes)")
            recommendations.append("🧬 Perform full metabolic panel including fasting glucose")
        elif risk_level == 'Moderate Risk':
            recommendations.append("📋 Screen for prediabetes (5.7-6.4% HbA1c)")
            recommendations.append("⏰ Recheck every 3-6 months")
        
        # Comorbidity considerations
        if high_bp == 1:
            recommendations.append("💊 Monitor blood pressure regularly (<130/80 mmHg)")
            recommendations.append("🧂 Reinforce DASH diet and sodium restriction")
        
        if stroke == 1 or heart_disease == 1:
            recommendations.append("⚠️ High cardiovascular risk")
            recommendations.append("🏥 Consider statin therapy")
            recommendations.append("💓 Refer to cardiologist if not already managed")
        
        recommendations.append("📅 Schedule follow-up appointment in 3 months")
        recommendations.append("📱 Encourage use of patient portal for test result access")
        
        return recommendations
    
    def generate_monitoring_schedule(self, risk_level: str) -> Dict[str, str]:
        """
        Generate recommended monitoring schedule.
        
        Args:
            risk_level: Diabetes risk level
            
        Returns:
            Dictionary with monitoring recommendations
        """
        schedules = {
            'Low Risk': {
                'doctor_visit': 'Annually',
                'glucose_check': 'Every 3 years',
                'blood_pressure': 'Annually',
                'weight_check': 'Monthly (self)',
                'physical_activity': 'Daily',
            },
            'Moderate Risk': {
                'doctor_visit': 'Every 6 months',
                'glucose_check': 'Annually',
                'blood_pressure': 'Every 3 months',
                'weight_check': 'Weekly',
                'physical_activity': 'Daily (150 min/week)',
            },
            'High Risk': {
                'doctor_visit': 'Every 3 months',
                'glucose_check': 'Every 3 months',
                'blood_pressure': 'Monthly',
                'weight_check': 'Twice weekly',
                'physical_activity': 'Daily (150 min/week minimum)',
            },
            'Critical Risk': {
                'doctor_visit': 'Monthly',
                'glucose_check': 'Monthly or as ordered',
                'blood_pressure': 'Weekly or more',
                'weight_check': 'Twice weekly',
                'physical_activity': 'Daily with medical supervision',
            },
        }
        
        return schedules.get(risk_level, schedules['Low Risk'])
    
    def generate_preventive_measures(self, risk_level: str, 
                                    smoking: int, alcohol: int) -> List[str]:
        """
        Generate preventive health measures.
        
        Args:
            risk_level: Diabetes risk level
            smoking: Smoking status
            alcohol: Alcohol consumption status
            
        Returns:
            List of preventive measures
        """
        recommendations = []
        
        # Universal preventive measures
        recommendations.append("💉 Get annual flu vaccination")
        recommendations.append("🦴 Discuss osteoporosis screening if applicable")
        recommendations.append("😴 Aim for 7-9 hours of quality sleep nightly")
        recommendations.append("🧠 Manage stress through meditation or counseling")
        
        # Smoking cessation
        if smoking == 1:
            recommendations.append("🚬 SMOKING CESSATION: Quit smoking to reduce diabetes risk by 50%")
            recommendations.append("📞 Use smoking cessation hotline: 1-800-QUIT-NOW")
            recommendations.append("💊 Ask doctor about nicotine replacement therapy")
        
        # Alcohol moderation
        if alcohol == 1:
            recommendations.append("🍷 REDUCE alcohol consumption")
            recommendations.append("📏 Women: ≤1 drink/day; Men: ≤2 drinks/day")
            recommendations.append("⚠️ Avoid alcohol on empty stomach")
        
        # Risk-specific prevention
        if risk_level in ['High Risk', 'Critical Risk']:
            recommendations.append("🧪 Consider diabetes prevention program")
            recommendations.append("👥 Join support group for peer motivation")
            recommendations.append("📱 Use health tracking app for accountability")
        
        return recommendations
    
    def generate_emergency_recommendations(self, risk_level: str) -> List[str]:
        """
        Generate emergency warning signs and recommendations.
        
        Args:
            risk_level: Diabetes risk level
            
        Returns:
            List of emergency recommendations
        """
        recommendations = []
        
        recommendations.append("🚨 SEEK EMERGENCY CARE (Call 911) if experiencing:")
        recommendations.append("  • Chest pain or pressure")
        recommendations.append("  • Shortness of breath")
        recommendations.append("  • Sudden severe headache or confusion")
        recommendations.append("  • Slurred speech or facial drooping")
        recommendations.append("  • Severe hypoglycemia symptoms: seizures, loss of consciousness")
        
        if risk_level in ['High Risk', 'Critical Risk']:
            recommendations.append("\n⚠️ URGENT CARE for:")
            recommendations.append("  • Persistent chest discomfort")
            recommendations.append("  • Severe fatigue or weakness")
            recommendations.append("  • Blurred vision changes")
            recommendations.append("  • Frequent urination with thirst")
        
        recommendations.append("\n📞 Keep emergency contacts readily available")
        recommendations.append("🆔 Wear medical alert identification")
        
        return recommendations
    
    def generate_full_recommendations(self, features_dict: Dict, 
                                     risk_level: str, 
                                     prediction_proba: np.ndarray) -> Dict[str, Any]:
        """
        Generate comprehensive personalized recommendations.
        
        Args:
            features_dict: Dictionary mapping feature names to values
            risk_level: Classified risk level
            prediction_proba: Prediction probabilities
            
        Returns:
            Comprehensive recommendation package
        """
        return {
            'risk_classification': self.classify_risk_level(prediction_proba, 2 if risk_level == 'High Risk' else 1 if risk_level == 'Moderate Risk' else 0),
            'diet_plan': self.generate_diet_plan(
                bmi=features_dict.get('BMI', 25),
                income=features_dict.get('Income', 4),
                fruit_intake=features_dict.get('Fruits', 1),
                veggie_intake=features_dict.get('Veggies', 1),
                risk_level=risk_level
            ),
            'exercise_plan': self.generate_exercise_plan(
                physical_activity=features_dict.get('PhysActivity', 1),
                age=features_dict.get('Age', 5),
                general_health=features_dict.get('GenHlth', 3),
                risk_level=risk_level
            ),
            'weight_management': self.generate_weight_management_plan(
                bmi=features_dict.get('BMI', 25),
                age=features_dict.get('Age', 5),
                general_health=features_dict.get('GenHlth', 3),
            ),
            'clinical_recommendations': self.generate_clinical_recommendations(
                risk_level=risk_level,
                high_bp=features_dict.get('HighBP', 1),
                stroke=features_dict.get('Stroke', 0),
                heart_disease=features_dict.get('HeartDiseaseorAttack', 0),
            ),
            'monitoring_schedule': self.generate_monitoring_schedule(risk_level),
            'preventive_measures': self.generate_preventive_measures(
                risk_level=risk_level,
                smoking=features_dict.get('Smoker', 0),
                alcohol=features_dict.get('HvyAlcoholConsump', 0),
            ),
            'emergency_guidelines': self.generate_emergency_recommendations(risk_level),
        }
