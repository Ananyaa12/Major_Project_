/**
 * Prediction Page
 * Main prediction form
 */

import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { predictionService } from '../services/api'
import { motion } from 'framer-motion'

const PredictionPage = () => {
    const [prediction, setPrediction] = useState(null)
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

    // BRFSS 2015 features
    const features = [
        'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
        'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
        'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth',
        'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income'
    ]

    const riskLevels = {
        0: { label: 'Low Risk', color: 'bg-green-100 text-green-800', icon: '✓' },
        1: { label: 'Moderate Risk', color: 'bg-yellow-100 text-yellow-800', icon: '⚠️' },
        2: { label: 'High Risk', color: 'bg-red-100 text-red-800', icon: '⛔' },
    }

    const onSubmit = async (data) => {
        try {
            setError(null)
            setLoading(true)

            // Convert string values to numbers
            const features = {}
            Object.keys(data).forEach((key) => {
                features[key] = parseFloat(data[key])
            })

            const response = await predictionService.predict(features)
            setPrediction(response.data)
        } catch (err) {
            setError(err.response?.data?.message || 'Prediction failed')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-violet-50 py-12 px-4">
            <div className="max-w-6xl mx-auto">
                <div className="text-center mb-10">
                    <p className="text-blue-600 font-semibold uppercase tracking-[0.3em] text-sm mb-3">Live demo prediction</p>
                    <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">Diabetes Risk Prediction</h1>
                    <p className="text-lg text-slate-600 max-w-2xl mx-auto">
                        Enter your health metrics for a personalized risk assessment powered by the trained model.
                    </p>
                </div>

                <div className="grid lg:grid-cols-[1.6fr_0.9fr] gap-8">
                    {/* Form */}
                    <div className="bg-white/90 rounded-[28px] shadow-[0_20px_70px_rgba(15,23,42,0.08)] border border-slate-200 p-8 backdrop-blur">
                        {error && (
                            <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                                {error}
                            </div>
                        )}

                        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                            <div className="flex justify-end">
                                <button
                                    type="button"
                                    onClick={() => reset(defaultValues)}
                                    className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                                >
                                    Load sample values
                                </button>
                            </div>

                            <div className="grid md:grid-cols-2 gap-4">
                                {features.map((feature) => (
                                    <div key={feature}>
                                        <label className="block text-sm font-semibold mb-1">{feature}</label>
                                        <input
                                            type="number"
                                            placeholder="0"
                                            {...register(feature, {
                                                required: `${feature} is required`,
                                                valueAsNumber: true,
                                            })}
                                            className="w-full px-3 py-2 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-50"
                                        />
                                        {errors[feature] && (
                                            <p className="text-red-500 text-xs mt-1">{errors[feature].message}</p>
                                        )}
                                    </div>
                                ))}
                            </div>

                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full bg-gradient-to-r from-blue-600 to-violet-600 text-white font-semibold py-3 rounded-full hover:shadow-lg transition disabled:opacity-50 mt-6"
                            >
                                {loading ? 'Predicting...' : 'Get Prediction'}
                            </button>
                        </form>
                    </div>

                    {/* Results */}
                    {prediction && (
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="bg-white/90 rounded-[28px] shadow-[0_20px_70px_rgba(15,23,42,0.08)] border border-slate-200 p-8 backdrop-blur"
                        >
                            <h2 className="text-2xl font-bold mb-6">Prediction Result</h2>

                            <div className={`p-4 rounded-2xl mb-6 ${riskLevels[prediction.prediction].color}`}>
                                <div className="text-3xl font-bold">
                                    {riskLevels[prediction.prediction].icon} {riskLevels[prediction.prediction].label}
                                </div>
                            </div>

                            <div className="space-y-4">
                                <div>
                                    <div className="text-sm text-gray-600">Confidence</div>
                                    <div className="text-2xl font-bold">{(prediction.confidence * 100).toFixed(1)}%</div>
                                </div>

                                <div>
                                    <div className="text-sm text-gray-600">Probabilities</div>
                                    <div className="space-y-2 mt-2">
                                        {prediction.probability && (
                                            <>
                                                <div className="flex justify-between text-sm">
                                                    <span>Low Risk</span>
                                                    <span>{(prediction.probability.low_risk * 100).toFixed(1)}%</span>
                                                </div>
                                                <div className="w-full bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className="bg-green-500 h-2 rounded-full"
                                                        style={{ width: `${prediction.probability.low_risk * 100}%` }}
                                                    ></div>
                                                </div>

                                                <div className="flex justify-between text-sm mt-2">
                                                    <span>Moderate Risk</span>
                                                    <span>{(prediction.probability.moderate_risk * 100).toFixed(1)}%</span>
                                                </div>
                                                <div className="w-full bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className="bg-yellow-500 h-2 rounded-full"
                                                        style={{ width: `${prediction.probability.moderate_risk * 100}%` }}
                                                    ></div>
                                                </div>

                                                <div className="flex justify-between text-sm mt-2">
                                                    <span>High Risk</span>
                                                    <span>{(prediction.probability.high_risk * 100).toFixed(1)}%</span>
                                                </div>
                                                <div className="w-full bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className="bg-red-500 h-2 rounded-full"
                                                        style={{ width: `${prediction.probability.high_risk * 100}%` }}
                                                    ></div>
                                                </div>
                                            </>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default PredictionPage
