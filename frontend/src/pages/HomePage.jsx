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
            title: 'Prediction',
            description: 'Real-time diabetes risk scoring built on robust ML models.',
            icon: '🎯',
        },
        {
            title: 'Explainable AI',
            description: 'Interactive feature contributions that reveal model reasoning.',
            icon: '🔍',
        },
        {
            title: 'Fairness-Aware',
            description: 'Demographic comparison and fairness monitoring across groups.',
            icon: '⚖️',
        },
        {
            title: 'Personalized Recommendations',
            description: 'Action-oriented suggestions tailored to the patient profile.',
            icon: '💡',
        },
        {
            title: 'Risk Stratification',
            description: 'Low, moderate, and high-risk segmentation for decision support.',
            icon: '📊',
        },
        {
            title: 'Clinical Support',
            description: 'A decision-ready interface designed for healthcare insight.',
            icon: '🏥',
        },
    ]

    const stats = [
        { value: '253K+', label: 'Health Records' },
        { value: '11', label: 'ML Models' },
        { value: '4', label: 'Fairness Metrics' },
        { value: '24/7', label: 'Explainable Insights' },
    ]

    return (
        <div className="bg-slate-50 dark:bg-slate-950">
            <Hero />

            <section className="relative py-20 px-4">
                <div className="absolute inset-0 animated-grid opacity-60" />
                <div className="relative max-w-6xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, y: 25 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="text-center mb-12"
                    >
                        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.32em] text-blue-600">Why it stands out</p>
                        <h2 className="text-4xl font-black text-slate-900 dark:text-white md:text-5xl">A complete explainable care workflow</h2>
                    </motion.div>

                    <div className="grid gap-6 md:grid-cols-3">
                        {features.map((feature, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 28 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                viewport={{ once: true }}
                                whileHover={{ y: -8, scale: 1.01 }}
                                className="glass-card rounded-3xl p-7"
                            >
                                <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-violet-600 text-2xl shadow-lg shadow-blue-500/20">{feature.icon}</div>
                                <h3 className="mb-2 text-xl font-bold text-slate-900 dark:text-white">{feature.title}</h3>
                                <p className="text-sm leading-6 text-slate-600 dark:text-slate-300">{feature.description}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            <section className="py-20 px-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600">
                <div className="max-w-4xl mx-auto text-center text-white">
                    <h2 className="text-4xl font-black mb-12">Research Impact</h2>

                    <div className="grid md:grid-cols-4 gap-8">
                        {stats.map((stat, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: index * 0.08 }}
                                className="rounded-[28px] border border-white/15 bg-white/10 p-6 backdrop-blur-sm"
                            >
                                <div className="text-4xl font-black mb-2">{stat.value}</div>
                                <div className="text-sm text-blue-100">{stat.label}</div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            <section className="py-20 px-4 bg-white dark:bg-slate-950">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-14">
                        <p className="text-blue-600 font-semibold uppercase tracking-[0.3em] text-sm mb-3">Simple workflow</p>
                        <h2 className="text-4xl font-black text-slate-900 dark:text-white">How It Works</h2>
                    </div>

                    <div className="grid md:grid-cols-4 gap-8">
                        {[
                            { step: '1', title: 'Input Data', desc: 'Enter your health metrics' },
                            { step: '2', title: 'Prediction', desc: 'ML model predicts risk level' },
                            { step: '3', title: 'Explanation', desc: 'SHAP explains the prediction' },
                            { step: '4', title: 'Recommendations', desc: 'Get personalized advice' },
                        ].map((item, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, x: 10 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.08 }}
                                className="relative rounded-[30px] border border-slate-200 bg-slate-50 p-6 shadow-lg shadow-slate-200/60 dark:border-slate-800 dark:bg-slate-900 dark:shadow-none"
                            >
                                <div className="absolute -left-4 -top-4 w-10 h-10 bg-gradient-to-br from-blue-600 to-violet-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
                                    {item.step}
                                </div>
                                <div className="pl-8 pt-4">
                                    <h3 className="text-lg font-bold mb-2 text-slate-900 dark:text-white">{item.title}</h3>
                                    <p className="text-gray-600 dark:text-slate-300">{item.desc}</p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    )
}

export default HomePage
