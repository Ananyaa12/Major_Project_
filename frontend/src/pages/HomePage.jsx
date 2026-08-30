/**
 * Home Page
 * Landing page with hero and features
 */

import React from 'react'
import Hero from '../components/Hero'
import { motion } from 'framer-motion'
import { FiCheck } from 'react-icons/fi'

const HomePage = () => {
    const features = [
        {
            title: 'Accurate Prediction',
            description: 'ML ensemble models with 99% accuracy',
            icon: '🎯',
        },
        {
            title: 'Explainable AI',
            description: 'SHAP-based explanation for every prediction',
            icon: '🔍',
        },
        {
            title: 'Fairness-Aware',
            description: 'Bias detection across demographic groups',
            icon: '⚖️',
        },
        {
            title: 'Personalized Recommendations',
            description: 'Tailored lifestyle and clinical recommendations',
            icon: '💡',
        },
        {
            title: 'Risk Stratification',
            description: 'Multi-level risk classification',
            icon: '📊',
        },
        {
            title: 'Clinical Support',
            description: 'Clinical decision support for healthcare providers',
            icon: '🏥',
        },
    ]

    return (
        <div>
            <Hero />

            {/* Features Section */}
            <section className="py-20 px-4 bg-slate-50">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-14">
                        <p className="text-blue-600 font-semibold uppercase tracking-[0.3em] text-sm mb-3">Why it stands out</p>
                        <h2 className="text-4xl font-bold text-slate-900">Key Features</h2>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        {features.map((feature, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                viewport={{ once: true }}
                                className="p-8 rounded-3xl border border-slate-200 bg-white shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all"
                            >
                                <div className="text-4xl mb-4">{feature.icon}</div>
                                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                                <p className="text-gray-600">{feature.description}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Research Stats */}
            <section className="py-20 px-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600">
                <div className="max-w-4xl mx-auto text-center text-white">
                    <h2 className="text-4xl font-bold mb-12">Research Impact</h2>

                    <div className="grid md:grid-cols-4 gap-8">
                        <div>
                            <div className="text-4xl font-bold mb-2">250K+</div>
                            <div>Patient Records</div>
                        </div>
                        <div>
                            <div className="text-4xl font-bold mb-2">11</div>
                            <div>ML Models</div>
                        </div>
                        <div>
                            <div className="text-4xl font-bold mb-2">99%</div>
                            <div>Accuracy</div>
                        </div>
                        <div>
                            <div className="text-4xl font-bold mb-2">4</div>
                            <div>Fairness Metrics</div>
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works */}
            <section className="py-20 px-4 bg-white">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-14">
                        <p className="text-blue-600 font-semibold uppercase tracking-[0.3em] text-sm mb-3">Simple workflow</p>
                        <h2 className="text-4xl font-bold text-slate-900">How It Works</h2>
                    </div>

                    <div className="grid md:grid-cols-4 gap-8">
                        {[
                            { step: '1', title: 'Input Data', desc: 'Enter your health metrics' },
                            { step: '2', title: 'Prediction', desc: 'ML model predicts risk level' },
                            { step: '3', title: 'Explanation', desc: 'SHAP explains the prediction' },
                            { step: '4', title: 'Recommendations', desc: 'Get personalized advice' },
                        ].map((item, i) => (
                            <div key={i} className="relative">
                                <div className="absolute -left-4 -top-4 w-10 h-10 bg-gradient-to-br from-blue-600 to-violet-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
                                    {item.step}
                                </div>
                                <div className="pl-8 pt-4">
                                    <h3 className="text-lg font-bold mb-2">{item.title}</h3>
                                    <p className="text-gray-600">{item.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    )
}

export default HomePage
