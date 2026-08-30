/**
 * About Page
 * Project overview and research information
 */

import React from 'react'

const AboutPage = () => {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold mb-8">About This Project</h1>

                <div className="space-y-8">
                    <section className="bg-white rounded-lg shadow p-8">
                        <h2 className="text-2xl font-bold mb-4">Project Overview</h2>
                        <p className="text-gray-700 leading-relaxed">
                            This project presents a novel explainable and fairness-aware ensemble learning
                            framework for personalized diabetes risk prediction. It combines state-of-the-art
                            machine learning models with explainability techniques (SHAP) and fairness metrics
                            to provide reliable, interpretable, and equitable diabetes risk assessments.
                        </p>
                    </section>

                    <section className="bg-white rounded-lg shadow p-8">
                        <h2 className="text-2xl font-bold mb-4">Key Technologies</h2>
                        <div className="grid md:grid-cols-2 gap-6">
                            <div>
                                <h3 className="font-bold mb-2">Machine Learning</h3>
                                <ul className="list-disc list-inside text-gray-700 space-y-1">
                                    <li>Random Forest, XGBoost, LightGBM, CatBoost</li>
                                    <li>Ensemble Learning (Voting, Stacking)</li>
                                    <li>SMOTE for class imbalance handling</li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="font-bold mb-2">Explainability & Fairness</h3>
                                <ul className="list-disc list-inside text-gray-700 space-y-1">
                                    <li>SHAP (SHapley Additive exPlanations)</li>
                                    <li>Demographic parity & disparate impact metrics</li>
                                    <li>Fairness-aware preprocessing</li>
                                </ul>
                            </div>
                        </div>
                    </section>

                    <section className="bg-white rounded-lg shadow p-8">
                        <h2 className="text-2xl font-bold mb-4">Dataset</h2>
                        <p className="text-gray-700 leading-relaxed mb-4">
                            CDC BRFSS 2015 Diabetes Health Indicators Dataset
                        </p>
                        <ul className="list-disc list-inside text-gray-700 space-y-1">
                            <li>250,000+ patient records</li>
                            <li>21 health and demographic features</li>
                            <li>3-class diabetes prediction (0: No diabetes, 1: Prediabetes, 2: Diabetes)</li>
                        </ul>
                    </section>

                    <section className="bg-white rounded-lg shadow p-8">
                        <h2 className="text-2xl font-bold mb-4">Model Performance</h2>
                        <div className="grid md:grid-cols-2 gap-6">
                            <div>
                                <div className="text-sm text-gray-600">Overall Accuracy</div>
                                <div className="text-4xl font-bold text-blue-600">99%</div>
                            </div>
                            <div>
                                <div className="text-sm text-gray-600">F1-Score</div>
                                <div className="text-4xl font-bold text-blue-600">0.99</div>
                            </div>
                        </div>
                    </section>

                    <section className="bg-blue-50 rounded-lg border border-blue-200 p-8">
                        <h2 className="text-2xl font-bold mb-4 text-blue-900">Contact & Citation</h2>
                        <p className="text-blue-800 leading-relaxed mb-4">
                            This research project is part of the B.Tech final year major project.
                            For questions or collaboration, please contact the development team.
                        </p>
                        <p className="text-blue-800 font-semibold">
                            Citation: A Novel Explainable and Fairness-Aware Ensemble Learning Framework
                            for Personalized Diabetes Risk Prediction and Intervention, 2024
                        </p>
                    </section>
                </div>
            </div>
        </div>
    )
}

export default AboutPage
