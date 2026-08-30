/**
 * App Component
 * Main application router and layout
 */

import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Navigation from './components/Navigation'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import PredictionPage from './pages/PredictionPage'
import FairnessPage from './pages/FairnessPage'
import AnalyticsPage from './pages/AnalyticsPage'
import AboutPage from './pages/AboutPage'
import './index.css'

function App() {
    return (
        <Router>
            <AuthProvider>
                <div className="min-h-screen bg-gray-50">
                    <Navigation />
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/about" element={<AboutPage />} />
                        <Route path="/dashboard" element={<DashboardPage />} />
                        <Route path="/predict" element={<PredictionPage />} />
                        <Route path="/fairness" element={<FairnessPage />} />
                        <Route path="/analytics" element={<AnalyticsPage />} />
                    </Routes>
                </div>
            </AuthProvider>
        </Router>
    )
}

export default App
