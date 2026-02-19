import { useState } from 'react'
import { PluginManager } from './components/Plugins/PluginManager'
import { Sidebar } from './components/Common/Sidebar'
import { ChatInterface } from './components/Chat/ChatInterface'
import { SystemMetrics } from './components/Dashboard/SystemMetrics'
import { ProcessList } from './components/Dashboard/ProcessList'
import { SettingsPanel } from './components/Settings/SettingsPanel'
import { LandingPage } from './components/Landing/LandingPage'
import { AnimatePresence, motion } from 'framer-motion'

export default function App() {
    const [hasEntered, setHasEntered] = useState(false)
    const [activeView, setActiveView] = useState('chat')

    if (!hasEntered) {
        return <LandingPage onEnter={() => setHasEntered(true)} />
    }

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
            className="flex h-screen bg-gradient-to-br from-gray-900 via-gray-900 to-black text-white font-sans overflow-hidden"
        >
            <Sidebar activeView={activeView} onViewChange={setActiveView} />

            <main className="flex-1 relative flex flex-col">
                {/* Header / Title Bar */}
                <div className="h-12 flex items-center px-6 border-b border-gray-800/50 select-none drag-region">
                    <span className="font-bold text-sm tracking-widest text-cyan-400 font-mono">EONIX SYSTEM</span>
                    <div className="ml-auto text-xs text-gray-600 font-mono">{activeView.toUpperCase()} MODE</div>
                </div>

                {/* Content Area */}
                <div className="flex-1 relative overflow-hidden">
                    <AnimatePresence mode="wait">
                        {activeView === 'chat' && (
                            <motion.div
                                key="chat"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.3 }}
                                className="h-full w-full"
                            >
                                <ChatInterface />
                            </motion.div>
                        )}

                        {activeView === 'dashboard' && (
                            <motion.div
                                key="dashboard"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                transition={{ duration: 0.3 }}
                                className="h-full overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-gray-700"
                            >
                                <h2 className="text-2xl font-light mb-6">System Overview</h2>
                                <SystemMetrics />

                                <div className="mt-8">
                                    <h3 className="text-lg text-gray-400 mb-4">Active Processes</h3>
                                    <ProcessList />
                                </div>
                            </motion.div>
                        )}

                        {activeView === 'plugins' && (
                            <motion.div
                                key="plugins"
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                transition={{ duration: 0.3 }}
                                className="h-full w-full overflow-hidden"
                            >
                                <PluginManager />
                            </motion.div>
                        )}

                        {activeView === 'settings' && (
                            <motion.div
                                key="settings"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                transition={{ duration: 0.3 }}
                                className="h-full overflow-y-auto scrollbar-thin scrollbar-thumb-gray-700"
                            >
                                <SettingsPanel />
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </main>
        </motion.div>
    )
}

function PluginManagerPlaceholder() {
    return (
        <div className="p-12 border border-dashed border-gray-800 rounded-xl">
            <div className="text-4xl mb-4">🧩</div>
            <h3 className="text-xl font-medium mb-2">Plugin Manager</h3>
            <p className="text-gray-500">Discover and manage Eonix capabilities.</p>
        </div>
    )
}
