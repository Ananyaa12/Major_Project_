/**
 * Fairness Page
 * Fairness evaluation and bias detection
 */

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { fairnessService } from '../services/api'

const FairnessPage = () => {
    const [summary, setSummary] = useState(null)
    const [report, setReport] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const fairnessHighlights = summary
        ? (() => {
            const allGroups = Object.values(summary.groups || {})
            const allValues = allGroups.flatMap((group) => Object.values(group || {}))
            const selectionRates = allValues.map((entry) => Number(entry?.selection_rate ?? 0))
            const truePositiveRates = allValues.map((entry) => Number(entry?.true_positive_rate ?? 0))
            const falsePositiveRates = allValues.map((entry) => Number(entry?.false_positive_rate ?? 0))

            const avgSelectionRate = selectionRates.length ? (selectionRates.reduce((sum, value) => sum + value, 0) / selectionRates.length) : 0
            const avgTPR = truePositiveRates.length ? (truePositiveRates.reduce((sum, value) => sum + value, 0) / truePositiveRates.length) : 0
            const avgFPR = falsePositiveRates.length ? (falsePositiveRates.reduce((sum, value) => sum + value, 0) / falsePositiveRates.length) : 0

            return [
                { label: 'Selection spread', value: `${avgSelectionRate.toFixed(2)}`, accent: 'from-blue-500 to-indigo-500' },
                { label: 'TPR balance', value: `${avgTPR.toFixed(2)}`, accent: 'from-emerald-500 to-green-500' },
                { label: 'FPR balance', value: `${avgFPR.toFixed(2)}`, accent: 'from-amber-500 to-orange-500' },
            ]
        })()
        : []

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [summaryResponse, reportResponse] = await Promise.all([
                    fairnessService.getFairnessSummary(),
                    fairnessService.getFairnessReport(),
                ])
                setSummary(summaryResponse.data)
                setReport(reportResponse.data.report)
            } catch (err) {
                setError(err.response?.data?.message || 'Failed to load fairness data')
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])

    if (loading) return <div className="py-12 text-center text-slate-600 dark:text-slate-300">Loading fairness dashboard...</div>
    if (error) return <div className="py-12 text-center text-red-600">{error}</div>

    const renderMetricBars = (groupName, metrics) => (
        <div className="space-y-4">
            {Object.entries(metrics).map(([label, values]) => (
                <div key={label} className="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800/80">
                    <div className="mb-2 flex items-center justify-between gap-3">
                        <span className="font-semibold text-slate-800 dark:text-slate-100">{label}</span>
                        <span className="text-sm text-slate-500 dark:text-slate-400">Selection {Number(values.selection_rate ?? 0).toFixed(2)}</span>
                    </div>
                    <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                        <div
                            className="h-full rounded-full bg-gradient-to-r from-blue-500 to-violet-500"
                            style={{ width: `${Math.min((Number(values.selection_rate ?? 0) * 100), 100)}%` }}
                        ></div>
                    </div>
                    <div className="mt-2 flex justify-between text-xs text-slate-500 dark:text-slate-400">
                        <span>TPR {Number(values.true_positive_rate ?? 0).toFixed(2)}</span>
                        <span>FPR {Number(values.false_positive_rate ?? 0).toFixed(2)}</span>
                    </div>
                </div>
            ))}
        </div>
    )

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-violet-50 px-4 py-12 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
            <div className="mx-auto max-w-7xl">
                <div className="mb-8">
                    <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-600">Ethics & inclusion</p>
                    <h1 className="text-4xl font-black text-slate-900 dark:text-slate-100">Fairness Dashboard</h1>
                </div>

                {fairnessHighlights.length > 0 && (
                    <div className="mb-10 grid gap-6 md:grid-cols-3">
                        {fairnessHighlights.map((item) => (
                            <motion.div
                                key={item.label}
                                initial={{ opacity: 0, y: 16 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="glass-card rounded-[28px] p-6"
                            >
                                <div className={`mb-4 h-2.5 w-20 rounded-full bg-gradient-to-r ${item.accent}`} />
                                <div className="text-sm text-slate-500 dark:text-slate-400">{item.label}</div>
                                <div className="mt-2 text-3xl font-black text-slate-900 dark:text-slate-100">{item.value}</div>
                            </motion.div>
                        ))}
                    </div>
                )}

                <div className="mb-8 grid gap-8 lg:grid-cols-2">
                    <div className="rounded-[32px] border border-slate-200 bg-white/80 p-6 shadow-[0_20px_70px_rgba(15,23,42,0.08)] backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
                        <h2 className="mb-5 text-2xl font-black text-slate-900 dark:text-slate-100">Group comparison</h2>
                        <div className="space-y-6">
                            {summary && Object.entries(summary.groups || {}).map(([group, values]) => (
                                <div key={group} className="rounded-[26px] border border-slate-200 bg-slate-50 p-5 dark:border-slate-700 dark:bg-slate-800/80">
                                    <h3 className="mb-4 text-lg font-bold text-slate-900 dark:text-slate-100">{group}</h3>
                                    {renderMetricBars(group, values)}
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="rounded-[32px] border border-slate-200 bg-white/80 p-6 shadow-[0_20px_70px_rgba(15,23,42,0.08)] backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
                        <h2 className="mb-5 text-2xl font-black text-slate-900 dark:text-slate-100">Model fairness note</h2>
                        <div className="rounded-[24px] border border-blue-200 bg-blue-50 p-5 text-sm leading-6 text-blue-900 dark:border-blue-900 dark:bg-blue-950/50 dark:text-blue-100">
                            {summary?.status || 'Fairness metrics reviewed and tracked for ongoing monitoring.'}
                        </div>
                        <div className="mt-6 overflow-hidden rounded-[24px] border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800/80">
                            <pre className="max-h-[420px] overflow-auto whitespace-pre-wrap font-mono text-xs leading-6 text-slate-700 dark:text-slate-200">
                                {report || 'No detailed fairness report available yet.'}
                            </pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default FairnessPage
