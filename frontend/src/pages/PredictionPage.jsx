/**
 * Prediction Page
 * Main prediction form
 */

import React, { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { predictionService, analyticsService } from '../services/api'
import { motion } from 'framer-motion'

const PredictionPage = () => {
    const [prediction, setPrediction] = useState(null)
    const [history, setHistory] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const defaultValues = {
        HighBP: 1,
        HighChol: 1,
        CholCheck: 1,
        BMI: 32.5,
        Smoker: 1,
        Stroke: 0,
        HeartDiseaseorAttack: 0,
        PhysActivity: 0,
        Fruits: 0,
        Veggies: 0,
        HvyAlcoholConsump: 0,
        AnyHealthcare: 1,
        NoDocbcCost: 0,
        GenHlth: 4,
        MentHlth: 10,
        PhysHlth: 15,
        DiffWalk: 1,
        Sex: 0,
        Age: 6,
        Education: 4,
        Income: 7,
    }
    const { register, handleSubmit, reset, formState: { errors } } = useForm({ defaultValues })

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await analyticsService.getPredictionHistory()
                setHistory(response.data.history || [])
            } catch (err) {
                console.error('History unavailable', err)
            }
        }

        fetchHistory()
    }, [])

    const fieldLabels = {
        HighBP: 'High blood pressure (0/1)',
        HighChol: 'High cholesterol (0/1)',
        CholCheck: 'Cholesterol check (0/1)',
        BMI: 'BMI',
        Smoker: 'Current smoker (0/1)',
        Stroke: 'History of stroke (0/1)',
        HeartDiseaseorAttack: 'Heart disease / attack (0/1)',
        PhysActivity: 'Physical activity (0/1)',
        Fruits: 'Fruit intake (0/1)',
        Veggies: 'Vegetable intake (0/1)',
        HvyAlcoholConsump: 'Heavy alcohol use (0/1)',
        AnyHealthcare: 'Any healthcare coverage (0/1)',
        NoDocbcCost: 'No doctor because of cost (0/1)',
        GenHlth: 'General health (1-5)',
        MentHlth: 'Mental health days (0-30)',
        PhysHlth: 'Poor physical health days (0-30)',
        DiffWalk: 'Difficulty walking (0/1)',
        Sex: 'Sex (0=Female, 1=Male)',
        Age: 'Age category (1-13)',
        Education: 'Education level (1-6)',
        Income: 'Income category (1-8)',
    }

    const categoryOptions = {
        HighBP: [0, 1],
        HighChol: [0, 1],
        CholCheck: [0, 1],
        Smoker: [0, 1],
        Stroke: [0, 1],
        HeartDiseaseorAttack: [0, 1],
        PhysActivity: [0, 1],
        Fruits: [0, 1],
        Veggies: [0, 1],
        HvyAlcoholConsump: [0, 1],
        AnyHealthcare: [0, 1],
        NoDocbcCost: [0, 1],
        GenHlth: [1, 2, 3, 4, 5],
        MentHlth: Array.from({ length: 31 }, (_, index) => index),
        PhysHlth: Array.from({ length: 31 }, (_, index) => index),
        DiffWalk: [0, 1],
        Sex: [0, 1],
        Age: Array.from({ length: 13 }, (_, index) => index + 1),
        Education: [1, 2, 3, 4, 5, 6],
        Income: [1, 2, 3, 4, 5, 6, 7, 8],
    }

    const features = Object.keys(fieldLabels)

    const riskLevels = {
        0: { label: 'Low Risk', color: 'bg-emerald-100 text-emerald-800 border-emerald-200', icon: '✓', accent: 'from-emerald-500 to-green-500' },
        1: { label: 'Moderate Risk', color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: '⚠️', accent: 'from-yellow-500 to-amber-500' },
        2: { label: 'High Risk', color: 'bg-rose-100 text-rose-800 border-rose-200', icon: '⛔', accent: 'from-red-500 to-pink-500' },
    }

    const riskMeta = {
        0: { percent: '14%', label: 'Healthy range' },
        1: { percent: '48%', label: 'Watch closely' },
        2: { percent: '82%', label: 'High priority' },
    }

    const onSubmit = async (data) => {
        try {
            setError(null)
            setLoading(true)

            const features = {}
            Object.keys(data).forEach((key) => {
                features[key] = parseFloat(data[key])
            })

            const response = await predictionService.predict(features)
            setPrediction(response.data)
            const historyResponse = await analyticsService.getPredictionHistory()
            setHistory(historyResponse.data.history || [])
        } catch (err) {
            setError(err.response?.data?.message || 'Prediction failed')
        } finally {
            setLoading(false)
        }
    }

    const downloadReport = () => {
        if (!prediction) return

        const blob = new Blob([
            `Diabetes Risk Report\n\n` +
            `Risk Level: ${prediction.risk_level}\n` +
            `Confidence: ${(prediction.confidence * 100).toFixed(1)}%\n` +
            `Prediction: ${prediction.prediction}\n\n` +
            `Top features:\n` +
            prediction.explanation.top_features.map((item) => `- ${item.feature}: ${item.value} (${item.direction})`).join('\n') + `\n\n` +
            `Recommendations:\n` +
            [...prediction.recommendations.diet, ...prediction.recommendations.exercise].map((item) => `- ${item}`).join('\n')
        ], { type: 'text/plain;charset=utf-8' })

        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = 'diabetes-risk-report.txt'
        link.click()
        URL.revokeObjectURL(link.href)
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-violet-50 py-12 px-4 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
            <div className="max-w-7xl mx-auto">
                <div className="mb-10 text-center">
                    <p className="mb-3 text-sm font-semibold uppercase tracking-[0.32em] text-blue-600">Live demo prediction</p>
                    <h1 className="mb-4 text-4xl font-black text-slate-900 dark:text-white md:text-5xl">Understand Your Diabetes Risk with Explainable AI</h1>
                    <p className="mx-auto max-w-2xl text-lg text-slate-600 dark:text-slate-300">
                        Enter your health metrics for a personalized risk assessment paired with transparent factor-level insight.
                    </p>
                </div>

                <div className="grid gap-8 lg:grid-cols-[1.55fr_0.95fr]">
                    <div className="glass-card rounded-[30px] p-8 dark:bg-slate-900/80">
                        {error && (
                            <div className="mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700">
                                {error}
                            </div>
                        )}

                        <div className="mb-6 flex items-center justify-between gap-3">
                            <div>
                                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Assessment progress</p>
                                <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Health profile</h2>
                            </div>
                            <div className="rounded-full bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700 dark:bg-blue-950/50 dark:text-blue-300">
                                20 health indicators
                            </div>
                        </div>

                        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                            <div className="flex justify-end">
                                <button
                                    type="button"
                                    onClick={() => reset(defaultValues)}
                                    className="rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                                >
                                    Load sample values
                                </button>
                            </div>

                            <div className="grid gap-4 md:grid-cols-2">
                                {features.map((feature) => (
                                    <div key={feature} className="rounded-2xl border border-slate-200 bg-slate-50/80 p-3 shadow-sm dark:border-slate-700 dark:bg-slate-800/80">
                                        <label className="mb-2 block text-xs font-bold uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">
                                            {fieldLabels[feature]}
                                            <span className="ml-1 text-blue-500">*</span>
                                        </label>
                                        {categoryOptions[feature] ? (
                                            <select
                                                {...register(feature, {
                                                    required: `${fieldLabels[feature]} is required`,
                                                    valueAsNumber: true,
                                                })}
                                                className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-inner outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
                                            >
                                                {categoryOptions[feature].map((option) => (
                                                    <option key={option} value={option}>{option}</option>
                                                ))}
                                            </select>
                                        ) : (
                                            <input
                                                type="number"
                                                placeholder={feature === 'BMI' ? 'e.g. 25.0' : 'Enter value'}
                                                {...register(feature, {
                                                    required: `${fieldLabels[feature]} is required`,
                                                    valueAsNumber: true,
                                                })}
                                                className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-inner outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
                                            />
                                        )}
                                        {errors[feature] && (
                                            <p className="mt-1 text-xs text-red-500">{errors[feature].message}</p>
                                        )}
                                    </div>
                                ))}
                            </div>

                            <button
                                type="submit"
                                disabled={loading}
                                className="mt-3 w-full rounded-full bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 py-3.5 text-base font-bold text-white shadow-lg shadow-blue-500/30 transition hover:shadow-xl disabled:opacity-50"
                            >
                                {loading ? 'Predicting...' : 'Get Prediction'}
                            </button>
                        </form>
                    </div>

                    {prediction && (
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="glass-card rounded-[30px] p-7 dark:bg-slate-900/80"
                        >
                            <div className="mb-6 flex items-center justify-between gap-3">
                                <div>
                                    <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Risk status</p>
                                    <h2 className="text-2xl font-black text-slate-900 dark:text-white">Prediction Result</h2>
                                </div>
                                <button
                                    onClick={downloadReport}
                                    className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-700 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200"
                                >
                                    Export report
                                </button>
                            </div>

                            <div className={`mb-6 rounded-[24px] border p-4 ${riskLevels[prediction.prediction].color}`}>
                                <div className="flex items-center justify-between gap-3">
                                    <div className="text-3xl font-black">{riskLevels[prediction.prediction].icon}</div>
                                    <div className="text-right">
                                        <div className="text-xs uppercase tracking-[0.2em] opacity-75">Current risk</div>
                                        <div className="text-2xl font-black">{riskLevels[prediction.prediction].label}</div>
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-6">
                                <div className="rounded-[24px] bg-slate-50 p-5 dark:bg-slate-800/70">
                                    <div className="mb-4 flex items-center justify-between">
                                        <div>
                                            <div className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">Confidence</div>
                                            <div className="text-3xl font-black text-slate-900 dark:text-white">{(prediction.confidence * 100).toFixed(1)}%</div>
                                        </div>
                                        <div className="risk-ring h-20 w-20 rounded-full bg-gradient-to-br from-blue-500 to-violet-600 text-xl font-black text-slate-900">
                                            <span className="text-lg text-slate-900">{riskMeta[prediction.prediction]?.percent}</span>
                                        </div>
                                    </div>

                                    <div className="text-sm text-slate-500 dark:text-slate-400">{riskMeta[prediction.prediction]?.label}</div>
                                </div>

                                <div className="rounded-[24px] bg-slate-50 p-5 dark:bg-slate-800/70">
                                    <div className="mb-3 text-sm font-bold uppercase tracking-[0.18em] text-slate-500 dark:text-slate-400">Class probability</div>
                                    <div className="space-y-3">
                                        {prediction.probability && (
                                            <>
                                                <div>
                                                    <div className="mb-1 flex items-center justify-between text-sm">
                                                        <span className="font-medium text-slate-700 dark:text-slate-200">Low Risk</span>
                                                        <span className="text-slate-500 dark:text-slate-400">{(prediction.probability.low_risk * 100).toFixed(1)}%</span>
                                                    </div>
                                                    <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                                                        <div className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-green-500" style={{ width: `${prediction.probability.low_risk * 100}%` }}></div>
                                                    </div>
                                                </div>

                                                <div>
                                                    <div className="mb-1 flex items-center justify-between text-sm">
                                                        <span className="font-medium text-slate-700 dark:text-slate-200">Moderate Risk</span>
                                                        <span className="text-slate-500 dark:text-slate-400">{(prediction.probability.moderate_risk * 100).toFixed(1)}%</span>
                                                    </div>
                                                    <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                                                        <div className="h-full rounded-full bg-gradient-to-r from-yellow-500 to-amber-500" style={{ width: `${prediction.probability.moderate_risk * 100}%` }}></div>
                                                    </div>
                                                </div>

                                                <div>
                                                    <div className="mb-1 flex items-center justify-between text-sm">
                                                        <span className="font-medium text-slate-700 dark:text-slate-200">High Risk</span>
                                                        <span className="text-slate-500 dark:text-slate-400">{(prediction.probability.high_risk * 100).toFixed(1)}%</span>
                                                    </div>
                                                    <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                                                        <div className="h-full rounded-full bg-gradient-to-r from-rose-500 to-red-500" style={{ width: `${prediction.probability.high_risk * 100}%` }}></div>
                                                    </div>
                                                </div>
                                            </>
                                        )}
                                    </div>
                                </div>

                                <div className="rounded-[24px] bg-slate-50 p-5 dark:bg-slate-800/70">
                                    <h3 className="mb-4 text-lg font-black text-slate-900 dark:text-white">Why this prediction?</h3>
                                    <div className="space-y-3">
                                        {prediction.explanation?.top_features?.map((feature, idx) => (
                                            <div key={idx} className="rounded-2xl border border-slate-200 bg-white p-3 dark:border-slate-700 dark:bg-slate-900/80">
                                                <div className="mb-2 flex items-center justify-between text-sm">
                                                    <span className="font-semibold text-slate-700 dark:text-slate-200">{feature.feature}</span>
                                                    <span className="font-bold text-slate-900 dark:text-white">+{feature.importance.toFixed(2)}</span>
                                                </div>
                                                <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                                                    <div
                                                        className="h-full rounded-full bg-gradient-to-r from-blue-500 via-cyan-500 to-violet-500"
                                                        style={{ width: `${Math.min(Math.abs(feature.importance) * 700, 100)}%` }}
                                                    ></div>
                                                </div>
                                                <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">Value: {feature.value} • {feature.direction}</div>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="rounded-[24px] bg-slate-50 p-5 dark:bg-slate-800/70">
                                    <h3 className="mb-4 text-lg font-black text-slate-900 dark:text-white">Personalized recommendations</h3>
                                    <ul className="space-y-3 text-sm">
                                        {[...(prediction.recommendations?.diet || []), ...(prediction.recommendations?.exercise || [])].slice(0, 5).map((item, idx) => (
                                            <li key={idx} className="rounded-2xl border border-emerald-200 bg-emerald-50 p-3 text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950/60 dark:text-emerald-200">{item}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </div>

                <div className="max-w-6xl mx-auto mt-8">
                    <div className="glass-card rounded-[30px] border border-slate-200 p-6 dark:border-slate-700 dark:bg-slate-900/80">
                        <h2 className="mb-4 text-2xl font-black text-slate-900 dark:text-white">Recent prediction history</h2>
                        {history.length === 0 ? (
                            <p className="text-slate-500 dark:text-slate-400">No prior predictions yet.</p>
                        ) : (
                            <div className="space-y-3">
                                {history.map((entry, idx) => {
                                    const riskColor =
                                        entry.risk_level === 'Low Risk'
                                            ? 'border-emerald-200 bg-emerald-50 text-emerald-900 dark:border-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-200'
                                            : entry.risk_level === 'Moderate Risk'
                                                ? 'border-yellow-200 bg-yellow-50 text-yellow-900 dark:border-yellow-800 dark:bg-yellow-950/60 dark:text-yellow-200'
                                                : 'border-rose-200 bg-rose-50 text-rose-900 dark:border-rose-800 dark:bg-rose-950/60 dark:text-rose-200'

                                    return (
                                        <div key={idx} className={`flex items-center justify-between rounded-2xl border p-3 ${riskColor}`}>
                                            <div>
                                                <div className="font-semibold">{entry.risk_level}</div>
                                                <div className="text-sm opacity-80">{new Date(entry.timestamp).toLocaleString()}</div>
                                            </div>
                                            <div className="text-sm font-semibold">Confidence {(entry.confidence * 100).toFixed(1)}%</div>
                                        </div>
                                    )
                                })}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PredictionPage
