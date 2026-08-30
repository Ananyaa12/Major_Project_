/**
 * Navigation Component
 * Main navigation bar for the application
 */

import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { FiMenu, FiX, FiLogOut, FiMoon, FiSun, FiChevronDown, FiCheck } from 'react-icons/fi'
import { useAuth } from '../context/AuthContext'

const Navigation = () => {
    const [isOpen, setIsOpen] = useState(false)
    const [themeMenuOpen, setThemeMenuOpen] = useState(false)
    const [theme, setTheme] = useState('light-ocean')
    const location = useLocation()
    const { isAuthenticated, logout } = useAuth()

    useEffect(() => {
        const stored = localStorage.getItem('theme')
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        const initialTheme = stored === 'dark'
            ? 'dark-ocean'
            : stored === 'light'
                ? 'light-ocean'
                : stored || (systemPrefersDark ? 'dark-ocean' : 'light-ocean')
        setTheme(initialTheme)
    }, [])

    useEffect(() => {
        const isDark = theme.startsWith('dark-')
        document.documentElement.classList.toggle('dark', isDark)
        document.documentElement.dataset.theme = theme
        localStorage.setItem('theme', theme)
    }, [theme])

    const themeOptions = [
        { id: 'light-ocean', label: 'Ocean', mode: 'Light', swatch: '#2563eb' },
        { id: 'light-emerald', label: 'Emerald', mode: 'Light', swatch: '#059669' },
        { id: 'light-rose', label: 'Rose', mode: 'Light', swatch: '#e11d48' },
        { id: 'dark-ocean', label: 'Midnight', mode: 'Dark', swatch: '#38bdf8' },
        { id: 'dark-emerald', label: 'Forest', mode: 'Dark', swatch: '#34d399' },
        { id: 'dark-rose', label: 'Berry', mode: 'Dark', swatch: '#fb7185' },
    ]

    const selectedTheme = themeOptions.find((option) => option.id === theme) || themeOptions[0]

    const navLinks = [
        { label: 'Home', path: '/' },
        { label: 'About', path: '/about' },
        { label: 'Research', path: '/research' },
        { label: 'Features', path: '/features' },
        { label: 'Dataset', path: '/dataset' },
        { label: 'Dashboard', path: '/dashboard', auth: true },
        { label: 'Predict', path: '/predict', auth: true },
        { label: 'Fairness', path: '/fairness', auth: true },
        { label: 'Analytics', path: '/analytics', auth: true },
    ]

    const filteredLinks = navLinks.filter(
        (link) => !link.auth || isAuthenticated
    )

    const handleLogout = async () => {
        await logout()
        window.location.href = '/'
    }

    return (
        <nav className="sticky top-0 z-50 border-b border-slate-200/70 bg-white/80 backdrop-blur-xl shadow-sm dark:border-slate-700 dark:bg-slate-900/80">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-violet-600 flex items-center justify-center shadow-lg">
                            <span className="text-white font-bold text-lg">🩺</span>
                        </div>
                        <span className="text-slate-800 font-bold hidden md:inline text-lg dark:text-slate-100">DiabetesAI</span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex space-x-1">
                        {filteredLinks.map((link) => (
                            <Link
                                key={link.path}
                                to={link.path}
                                className={`px-3 py-2 rounded-full text-sm font-medium transition-all ${location.pathname === link.path
                                    ? 'bg-blue-600 text-white shadow-sm'
                                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white'
                                    }`}
                            >
                                {link.label}
                            </Link>
                        ))}
                    </div>

                    {/* Auth Buttons */}
                    <div className="flex items-center space-x-4">
                        {!isAuthenticated ? (
                            <Link
                                to="/login"
                                className="px-4 py-2 bg-gradient-to-r from-blue-600 to-violet-600 text-white rounded-full font-semibold shadow-sm hover:shadow-md transition"
                            >
                                Login
                            </Link>
                        ) : (
                            <button
                                onClick={handleLogout}
                                className="flex items-center space-x-2 px-4 py-2 bg-rose-500 text-white rounded-full hover:bg-rose-600 transition"
                            >
                                <FiLogOut className="w-4 h-4" />
                                <span>Logout</span>
                            </button>
                        )}

                        <div className="relative">
                            <button
                                onClick={() => setThemeMenuOpen(!themeMenuOpen)}
                                className="flex items-center gap-2 rounded-full border border-slate-200 px-3 py-2 text-sm text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
                                aria-label="Choose color theme"
                                aria-expanded={themeMenuOpen}
                            >
                                {theme.startsWith('dark-') ? <FiMoon className="h-4 w-4" /> : <FiSun className="h-4 w-4" />}
                                <span className="hidden lg:inline">{selectedTheme.label}</span>
                                <FiChevronDown className="h-4 w-4" />
                            </button>
                            {themeMenuOpen && (
                                <div className="absolute right-0 mt-2 w-52 rounded-2xl border border-slate-200 bg-white p-2 shadow-xl dark:border-slate-700 dark:bg-slate-900">
                                    <p className="px-3 pb-2 pt-1 text-xs font-semibold uppercase tracking-wide text-slate-400">Color theme</p>
                                    {themeOptions.map((option) => (
                                        <button
                                            key={option.id}
                                            onClick={() => { setTheme(option.id); setThemeMenuOpen(false) }}
                                            className="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800"
                                        >
                                            <span className="h-3 w-3 rounded-full" style={{ backgroundColor: option.swatch }} />
                                            <span className="flex-1">{option.label}<span className="ml-1 text-xs text-slate-400">{option.mode}</span></span>
                                            {theme === option.id && <FiCheck className="h-4 w-4 text-blue-600" />}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Mobile Menu Button */}
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="md:hidden text-slate-700 dark:text-slate-200"
                        >
                            {isOpen ? (
                                <FiX className="w-6 h-6" />
                            ) : (
                                <FiMenu className="w-6 h-6" />
                            )}
                        </button>
                    </div>
                </div>

                {/* Mobile Navigation */}
                {isOpen && (
                    <div className="md:hidden pb-4">
                        {filteredLinks.map((link) => (
                            <Link
                                key={link.path}
                                to={link.path}
                                className="block px-3 py-2 text-slate-700 hover:bg-slate-100 rounded-xl dark:text-slate-200 dark:hover:bg-slate-800"
                                onClick={() => setIsOpen(false)}
                            >
                                {link.label}
                            </Link>
                        ))}
                    </div>
                )}
            </div>
        </nav>
    )
}

export default Navigation
