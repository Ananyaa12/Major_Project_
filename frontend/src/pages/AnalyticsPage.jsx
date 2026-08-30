/**
 * Analytics Page
 * Model comparison and feature importance
 */

import React, { useState, useEffect } from 'react'
import { modelService, explainabilityService } from '../services/api'
import { motion } from 'framer-motion'
import { FiBarChart2, FiCpu } from 'react-icons/fi'

const AnalyticsPage = () => {
    const [comparison, setComparison] = useState(null)
    const [importance, setImportance] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [comp, imp] = await Promise.all([
                    modelService.getModelComparison(),
                    explainabilityService.getFeatureImportance(),
                ])
                setComparison(comp.data)
                setImportance(imp.data.features)
            } catch (err) {
                setError(err.response?.data?.message || 'Failed to load analytics')
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])

    if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-700 dark:bg-slate-950 dark:text-slate-200">Loading analytics...</div>
    if (error) return <div className="min-h-screen flex items-center justify-center bg-slate-50 text-red-600 dark:bg-slate-950">{error}</div>

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-violet-50 py-12 px-4 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-600">Insight layer</p>
                    <h1 className="text-4xl font-bold text-slate-900 dark:text-slate-100">Analytics & Explainability</h1>
                </div>

                {/* Model Comparison */}
                {comparison && (
                    <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} className="mb-12 overflow-hidden rounded-[32px] border border-slate-200 bg-white/80 shadow-[0_20px_70px_rgba(15,23,42,0.08)] backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
                        <div className="flex items-center gap-3 border-b border-slate-200 p-8 dark:border-slate-800">
                            <div className="rounded-2xl bg-gradient-to-br from-blue-600 to-violet-600 p-3 text-white">
                                <FiBarChart2 className="h-5 w-5" />
                            </div>
                            <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Model Comparison</h2>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-slate-50 dark:bg-slate-800/70">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-sm font-semibold">Model</th>
                                        <th className="px-6 py-3 text-left text-sm font-semibold">Accuracy</th>
                                        <th className="px-6 py-3 text-left text-sm font-semibold">Precision</th>
                                        <th className="px-6 py-3 text-left text-sm font-semibold">Recall</th>
                                        <th className="px-6 py-3 text-left text-sm font-semibold">F1-Score</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {comparison.map((model, i) => (
                                        <tr key={i} className="border-b border-slate-200 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/70">
                                            <td className="px-6 py-3 font-semibold">{model.Model}</td>
                                            <td className="px-6 py-3">{(model.Accuracy * 100).toFixed(2)}%</td>
                                            <td className="px-6 py-3">{(model.Precision * 100).toFixed(2)}%</td>
                                            <td className="px-6 py-3">{(model.Recall * 100).toFixed(2)}%</td>
                                            <td className="px-6 py-3 font-bold">{(model['F1-Score'] * 100).toFixed(2)}%</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </motion.div>
                )}

                {/* Feature Importance */}
                {importance && (
                    <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} className="rounded-[32px] border border-slate-200 bg-white/80 p-8 shadow-[0_20px_70px_rgba(15,23,42,0.08)] backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="rounded-2xl bg-gradient-to-br from-blue-600 to-violet-600 p-3 text-white">
                                <FiCpu className="h-5 w-5" />
                            </div>
                            <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Top Feature Importance (SHAP)</h2>
                        </div>

                        <div className="space-y-4">
                            {importance.slice(0, 10).map((feature, i) => (
                                <div key={i}>
                                    <div className="flex justify-between mb-1">
                                        <span className="font-semibold">{feature.Feature}</span>
                                        <span className="text-gray-600">{feature.Importance.toFixed(4)}</span>
                                    </div>
                                    <div className="w-full bg-slate-200 rounded-full h-2 dark:bg-slate-700">
                                        <div
                                            className="bg-gradient-to-r from-blue-600 to-violet-600 h-2 rounded-full"
                                            style={{
                                                width: `${(feature.Importance / Math.max(...importance.map(f => f.Importance))) * 100}%`,
                                            }}
                                        ></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                )}
            </div>
        </div>
    )
}

export default AnalyticsPage
