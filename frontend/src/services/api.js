/**
 * API Service
 * Handles all HTTP requests to the backend
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Add token to requests
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => Promise.reject(error)
)

export const authService = {
    login: (username, password) =>
        apiClient.post('/auth/login', { username, password }),
    logout: () => apiClient.post('/auth/logout'),
}

export const modelService = {
    getModelInfo: () => apiClient.get('/models/info'),
    getModelComparison: () => apiClient.get('/models/comparison'),
}

export const predictionService = {
    predict: (features) => apiClient.post('/predict', features),
    predictBatch: (patients) => apiClient.post('/predict/batch', { patients }),
}

export const explainabilityService = {
    getFeatureImportance: () => apiClient.get('/explainability/feature-importance'),
}

export const fairnessService = {
    getFairnessReport: () => apiClient.get('/fairness/report'),
}

export const analyticsService = {
    getPredictions: () => apiClient.get('/analytics/predictions'),
    getDashboardData: () => apiClient.get('/analytics/dashboard'),
}

export default apiClient
