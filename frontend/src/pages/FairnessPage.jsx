/**
 * Fairness Page
 * Fairness evaluation and bias detection
 */

import React, { useState, useEffect } from 'react'
import { fairnessService } from '../services/api'

const FairnessPage = () => {
    const [report, setReport] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchReport = async () => {
            try {
                const response = await fairnessService.getFairnessReport()
                setReport(response.data.report)
            } catch (err) {
                setError(err.response?.data?.message || 'Failed to load fairness report')
            } finally {
                setLoading(false)
            }
        }

        fetchReport()
    }, [])

    if (loading) return <div className="text-center py-12">Loading...</div>
    if (error) return <div className="text-center py-12 text-red-600">{error}</div>

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold mb-8">Fairness Evaluation</h1>

                <div className="bg-white rounded-lg shadow p-8">
                    <pre className="whitespace-pre-wrap font-mono text-sm overflow-auto">
                        {report}
                    </pre>
                </div>

                <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h2 className="text-lg font-bold text-blue-900 mb-2">What is Fairness?</h2>
                    <p className="text-blue-800">
                        Fairness evaluation ensures that our model's predictions don't discriminate
                        against any demographic group. We measure fairness across gender, age,
                        education, and income levels using multiple fairness metrics.
                    </p>
                </div>
            </div>
        </div>
    )
}

export default FairnessPage
