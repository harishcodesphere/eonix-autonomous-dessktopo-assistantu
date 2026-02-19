import { motion } from 'framer-motion';
import { Power, Cpu, Shield, Globe } from 'lucide-react';

interface LandingPageProps {
    onEnter: () => void;
}

export function LandingPage({ onEnter }: LandingPageProps) {
    return (
        <div className="relative h-screen w-full bg-black overflow-hidden flex flex-col items-center justify-center text-white selection:bg-cyan-500/30">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-gray-900 via-black to-black opacity-80 z-0"></div>
            <div className="absolute inset-0 bg-grid-pattern opacity-10 z-0"></div>

            {/* Animated Glows */}
            <motion.div
                animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.5, 0.3] }}
                transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
                className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/20 rounded-full blur-[128px] z-0"
            />
            <motion.div
                animate={{ scale: [1, 1.3, 1], opacity: [0.2, 0.4, 0.2] }}
                transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 1 }}
                className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[128px] z-0"
            />

            {/* Content Container */}
            <div className="relative z-10 flex flex-col items-center max-w-4xl px-6 text-center">

                {/* Logo / Title Area */}
                <motion.div
                    initial={{ y: -50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="mb-8"
                >
                    <div className="inline-flex items-center justify-center p-3 mb-6 rounded-2xl bg-gray-900/50 border border-gray-800 backdrop-blur-md shadow-2xl shadow-cyan-900/20">
                        <Cpu className="w-8 h-8 text-cyan-400 mr-2" />
                        <span className="text-sm font-mono tracking-widest text-cyan-400">SYSTEM READY</span>
                    </div>
                </motion.div>

                <motion.h1
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="text-7xl md:text-8xl font-black tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white via-gray-200 to-gray-500 drop-shadow-2xl"
                >
                    EONIX <span className="text-cyan-500">OS</span>
                </motion.h1>

                <motion.p
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    className="text-xl md:text-2xl text-gray-400 max-w-2xl mb-12 font-light leading-relaxed"
                >
                    Next-generation AI orchestration platform.
                    Manage tasks, execute commands, and control your digital environment with
                    <span className="text-white font-medium"> absolute precision</span>.
                </motion.p>

                {/* Feature Grid (Small) */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8, duration: 1 }}
                    className="grid grid-cols-3 gap-8 mb-16 w-full max-w-lg"
                >
                    <div className="flex flex-col items-center">
                        <div className="p-3 rounded-xl bg-gray-900/50 border border-gray-800 mb-3 text-cyan-400">
                            <Cpu size={24} />
                        </div>
                        <span className="text-xs uppercase tracking-widest text-gray-500">AI Core</span>
                    </div>
                    <div className="flex flex-col items-center">
                        <div className="p-3 rounded-xl bg-gray-900/50 border border-gray-800 mb-3 text-purple-400">
                            <Shield size={24} />
                        </div>
                        <span className="text-xs uppercase tracking-widest text-gray-500">Secure</span>
                    </div>
                    <div className="flex flex-col items-center">
                        <div className="p-3 rounded-xl bg-gray-900/50 border border-gray-800 mb-3 text-emerald-400">
                            <Globe size={24} />
                        </div>
                        <span className="text-xs uppercase tracking-widest text-gray-500">Connected</span>
                    </div>
                </motion.div>

                {/* Call to Action */}
                <motion.div
                    initial={{ y: 50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0.6 }}
                >
                    <button
                        onClick={onEnter}
                        className="group relative px-8 py-4 bg-cyan-600 hover:bg-cyan-500 text-black font-bold text-lg rounded-full transition-all duration-300 shadow-[0_0_40px_-10px_rgba(6,182,212,0.5)] hover:shadow-[0_0_60px_-15px_rgba(6,182,212,0.7)] flex items-center overflow-hidden"
                    >
                        <span className="relative z-10 flex items-center">
                            INITIALIZE SYSTEM
                            <Power className="ml-2 w-5 h-5 group-hover:rotate-90 transition-transform duration-300" />
                        </span>

                        {/* Button Glow Effect */}
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 backdrop-blur-sm"></div>
                    </button>

                    <div className="mt-4 text-xs font-mono text-gray-600">
                        v1.0.0 // READY TO ENGAGE
                    </div>
                </motion.div>
            </div>

            {/* Footer / Decorative Elements */}
            <div className="absolute bottom-0 w-full h-px bg-gradient-to-r from-transparent via-gray-800 to-transparent"></div>
            <div className="absolute bottom-0 left-0 p-6 font-mono text-xs text-gray-700">
                SECURE CONNECTION ESTABLISHED
            </div>
            <div className="absolute bottom-0 right-0 p-6 font-mono text-xs text-gray-700">
                LATENCY: 12ms
            </div>
        </div>
    );
}

// Add this to your tailwind config or global css for the grid pattern if not exists,
// or I will add a utility class in globals.css
