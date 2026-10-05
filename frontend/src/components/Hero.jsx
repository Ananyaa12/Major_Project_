/**
 * Hero Component
 * Landing page hero section
 */

import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FiArrowRight } from 'react-icons/fi'

const Hero = () => {
    return (
        <section className="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-blue-900 to-violet-900 flex items-center justify-center px-4 py-20">
            <div className="absolute inset-0 animated-grid opacity-30" />
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.18),_transparent_35%)]" />
            <div className="absolute -left-10 top-20 h-52 w-52 rounded-full bg-cyan-400/20 blur-3xl float-slow" />
            <div className="absolute right-8 bottom-10 h-60 w-60 rounded-full bg-violet-400/20 blur-3xl float-slower" />
            <div className="max-w-6xl mx-auto relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center text-white"
                >
                    <div className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-4 py-2 mb-6 text-sm font-medium backdrop-blur">
                        <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
                        AI-powered health risk assessment
                    </div>
                    <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight">
                        Understand Your Diabetes Risk
                        <span className="block text-transparent bg-clip-text bg-gradient-to-r from-sky-300 via-cyan-200 to-violet-200">
                            with Explainable AI
                        </span>
                    </h1>

                    <p className="text-xl md:text-2xl mb-8 text-white/90 max-w-3xl mx-auto leading-relaxed">
                        Personalized diabetes risk assessment powered by machine learning, fairness-aware analytics, and transparent clinical insight.
                    </p>

                    <div className="flex flex-col md:flex-row gap-4 justify-center mb-12">
                        <Link
                            to="/predict"
                            className="inline-flex items-center justify-center space-x-2 bg-white text-violet-700 px-8 py-4 rounded-full font-bold hover:scale-[1.02] transition-transform shadow-lg"
                        >
                            <span>Get Started</span>
                            <FiArrowRight className="w-5 h-5" />
                        </Link>

                        <Link
                            to="/about"
                            className="inline-flex items-center justify-center space-x-2 border border-white/30 bg-white/10 text-white px-8 py-4 rounded-full font-bold hover:bg-white/20 transition"
                        >
                            <span>Learn More</span>
                        </Link>
                    </div>

                    {/* Stats */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="grid gap-6 mt-16 md:grid-cols-4"
                    >
                        <div className="glass-card rounded-[26px] p-6 text-left">
                            <div className="text-3xl font-black">253K+</div>
                            <div className="text-sm opacity-90">Health Records</div>
                        </div>
                        <div className="glass-card rounded-[26px] p-6 text-left">
                            <div className="text-3xl font-black">11</div>
                            <div className="text-sm opacity-90">ML Models</div>
                        </div>
                        <div className="glass-card rounded-[26px] p-6 text-left">
                            <div className="text-3xl font-black">4</div>
                            <div className="text-sm opacity-90">Fairness Metrics</div>
                        </div>
                        <div className="glass-card rounded-[26px] p-6 text-left">
                            <div className="text-3xl font-black">24/7</div>
                            <div className="text-sm opacity-90">Explainable Insights</div>
                        </div>
                    </motion.div>
                </motion.div>
            </div>
        </section>
    )
}

export default Hero
