/**
 * Auth Context
 * Manages authentication state globally
 */

import React, { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '../services/api'

const AuthContext = createContext()

export const useAuth = () => {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context
}

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        // Check if user is already logged in
        const token = localStorage.getItem('authToken')
        const userData = localStorage.getItem('user')
        if (token && userData) {
            setUser(JSON.parse(userData))
        }
        setLoading(false)
    }, [])

    const login = async (username, password) => {
        try {
            setError(null)
            const response = await authService.login(username, password)
            const { token, user: userData } = response.data

            localStorage.setItem('authToken', token)
            localStorage.setItem('user', JSON.stringify(userData))
            setUser(userData)

            return userData
        } catch (err) {
            const errorMsg = err.response?.data?.message || 'Login failed'
            setError(errorMsg)
            throw err
        }
    }

    const logout = async () => {
        try {
            await authService.logout()
        } catch (err) {
            console.error('Logout error:', err)
        } finally {
            localStorage.removeItem('authToken')
            localStorage.removeItem('user')
            setUser(null)
        }
    }

    const value = {
        user,
        loading,
        error,
        login,
        logout,
        isAuthenticated: !!user,
    }

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
