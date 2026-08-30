/**
 * Dashboard Page
 * User dashboard with analytics
 */

import React, { useState, useEffect } from 'react'
import { analyticsService, modelService } from '../services/api'
import { motion } from 'framer-motion'
import { FiActivity, FiBarChart2, FiCpu, FiShield } from 'react-icons/fi'

const DashboardPage = () => {
    const [dashboardData, setDashboardData] = useState(null)
    const [modelInfo, setModelInfo] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [dashboard, model] = await Promise.all([
                    analyticsService.getDashboardData(),
                    modelService.getModelInfo(),
                ])
                setDashboardData(dashboard.data)
                setModelInfo(model.data)
            } catch (err) {
                setError(err.response?.data?.message || 'Failed to load dashboard')
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])

    if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-700 dark:bg-slate-950 dark:text-slate-200">Loading dashboard...</div>
    if (error) return <div className="min-h-screen flex items-center justify-center bg-slate-50 text-red-600 dark:bg-slate-950">{error}</div>

    const perf = dashboardData?.model_performance || {}

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-violet-50 py-12 px-4 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
                    <div>
                        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-600">Operations center</p>
                        <h1 className="text-4xl font-bold text-slate-900 dark:text-slate-100">Live Model Dashboard</h1>
                    </div>
                    <div className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/70 dark:text-emerald-300">
                        <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
                        System online
                    </div>
                </div>

                {/* Model Info */}
                {modelInfo && (
                    <div className="grid md:grid-cols-4 gap-6 mb-10">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-white rounded-lg shadow p-6"
                        >
                            <div className="text-sm text-slate-500 dark:text-slate-400">Best Model</div>
                            <div className="text-2xl font-bold mt-2 text-slate-900 dark:text-slate-100">{modelInfo.best_model}</div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 }}
                            className="bg-white rounded-lg shadow p-6"
                        >
                            <div className="text-sm text-slate-500 dark:text-slate-400">Accuracy</div>
                            <div className="text-2xl font-bold mt-2 text-slate-900 dark:text-slate-100">{(perf.accuracy * 100).toFixed(1)}%</div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                            className="bg-white rounded-lg shadow p-6"
                        >
                            <div className="text-sm text-slate-500 dark:text-slate-400">Precision</div>
                            <div className="text-2xl font-bold mt-2 text-slate-900 dark:text-slate-100">{(perf.precision * 100).toFixed(1)}%</div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                            className="bg-white rounded-lg shadow p-6"
                        >
                            <div className="text-sm text-slate-500 dark:text-slate-400">F1-Score</div>
                            <div className="text-2xl font-bold mt-2 text-slate-900 dark:text-slate-100">{(perf.f1_score * 100).toFixed(1)}%</div>
                        </motion.div>
                    </div>
                )}

                {/* Model Performance Details */}
                <div className="rounded-[32px] border border-slate-200 bg-white/80 p-8 shadow-[0_20px_70px_rgba(15,23,42,0.08)] backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="rounded-2xl bg-gradient-to-br from-blue-600 to-violet-600 p-3 text-white">
                            <FiBarChart2 className="h-5 w-5" />
                        </div>
                        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Model Performance</h2>
                    </div>

                    <div className="grid md:grid-cols-2 gap-8">
                        <div className="rounded-3xl bg-slate-50 p-6 dark:bg-slate-800/70">
                            <h3 className="text-lg font-semibold mb-4 text-slate-900 dark:text-slate-100">Key Metrics</h3>
                            <dl className="space-y-4">
                                <div>
                                    <dt className="text-sm text-slate-500 dark:text-slate-400">Accuracy</dt>
                                    <dd className="text-2xl font-bold text-slate-900 dark:text-slate-100">{(perf.accuracy * 100).toFixed(2)}%</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-slate-500 dark:text-slate-400">Precision</dt>
                                    <dd className="text-2xl font-bold text-slate-900 dark:text-slate-100">{(perf.precision * 100).toFixed(2)}%</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-slate-500 dark:text-slate-400">Recall</dt>
                                    <dd className="text-2xl font-bold text-slate-900 dark:text-slate-100">{(perf.recall * 100).toFixed(2)}%</dd>
                                </div>
                            </dl>
                        </div>

                        <div className="rounded-3xl bg-slate-50 p-6 dark:bg-slate-800/70">
                            <h3 className="text-lg font-semibold mb-4 text-slate-900 dark:text-slate-100">Dataset Snapshot</h3>
                            <dl className="space-y-4">
                                <div>
                                    <dt className="text-sm text-slate-500 dark:text-slate-400">Test Set Size</dt>
                                    <dd className="text-2xl font-bold text-slate-900 dark:text-slate-100">{dashboardData?.test_set_size?.toLocaleString()}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm text-slate-500 dark:text-slate-400">Features</dt>
                                    <dd className="text-2xl font-bold text-slate-900 dark:text-slate-100">{dashboardData?.feature_count}</dd>
                                </div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default DashboardPage
