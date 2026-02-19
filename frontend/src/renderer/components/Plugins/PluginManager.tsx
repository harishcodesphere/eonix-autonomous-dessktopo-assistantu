import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Plugin } from '../../types'

const API_URL = 'http://localhost:8000'

export function PluginManager() {
    const [plugins, setPlugins] = useState<Plugin[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        fetchPlugins()
    }, [])

    const fetchPlugins = async () => {
        try {
            const res = await fetch(`${API_URL}/api/plugins`)
            if (!res.ok) throw new Error('Failed to fetch plugins')
            const data = await res.json()
            setPlugins(data)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Unknown error')
        } finally {
            setLoading(false)
        }
    }

    const togglePlugin = async (pluginName: string, currentState: boolean) => {
        // Optimistic update
        setPlugins(prev => prev.map(p =>
            p.name === pluginName ? { ...p, enabled: !currentState } : p
        ))

        try {
            // In a real app, we'd call an API backend to persist this
            // await fetch(`${API_URL}/api/plugins/${pluginName}/toggle`, { method: 'POST' })

            // For now, since the backend doesn't have a toggle endpoint yet, 
            // we just simulate it or would add that endpoint in Phase 6+
            console.log(`Toggled ${pluginName} to ${!currentState}`)
        } catch (err) {
            // Revert on error
            setPlugins(prev => prev.map(p =>
                p.name === pluginName ? { ...p, enabled: currentState } : p
            ))
            console.error('Failed to toggle plugin:', err)
        }
    }

    if (loading) {
        return (
            <div className="flex h-full items-center justify-center text-gray-500">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500" />
            </div>
        )
    }

    if (error) {
        return (
            <div className="flex h-full items-center justify-center text-red-500">
                Error: {error}
            </div>
        )
    }

    if (plugins.length === 0) {
        return (
            <div className="flex h-full flex-col items-center justify-center text-gray-500 space-y-4">
                <div className="text-4xl">🔌</div>
                <p>No plugins installed.</p>
            </div>
        )
    }

    return (
        <div className="h-full overflow-y-auto px-6 py-6 scrollbar-thin scrollbar-thumb-gray-700">
            <h2 className="text-2xl font-semibold mb-6 text-gray-100 flex items-center gap-3">
                <span className="text-cyan-400">⚡</span> Plugins & Extensions
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {plugins.map((plugin) => (
                    <motion.div
                        key={plugin.name}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`relative group bg-gray-800/40 border backdrop-blur-sm rounded-xl p-5 transition-all duration-300
                            ${plugin.enabled
                                ? 'border-cyan-500/30 shadow-[0_0_15px_-5px_rgba(6,182,212,0.15)]'
                                : 'border-gray-700/50 opacity-60 hover:opacity-100'
                            }`}
                    >
                        {/* Header */}
                        <div className="flex justify-between items-start mb-3">
                            <div className="p-2 rounded-lg bg-gray-800 border border-gray-700">
                                <span className="text-xl">
                                    {getPluginIcon(plugin.name)}
                                </span>
                            </div>

                            <button
                                onClick={() => togglePlugin(plugin.name, plugin.enabled)}
                                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none
                                    ${plugin.enabled ? 'bg-cyan-600' : 'bg-gray-700'}`}
                            >
                                <span
                                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform
                                        ${plugin.enabled ? 'translate-x-6' : 'translate-x-1'}`}
                                />
                            </button>
                        </div>

                        {/* Content */}
                        <div>
                            <h3 className="text-lg font-medium text-gray-200 mb-1">
                                {formatName(plugin.name)}
                            </h3>
                            <p className="text-sm text-gray-400 leading-relaxed mb-4 min-h-[40px]">
                                {plugin.description || "No description provided."}
                            </p>

                            <div className="flex items-center justify-between text-xs text-gray-500 font-mono border-t border-gray-700/50 pt-3">
                                <span>v{plugin.version}</span>
                                <span className={plugin.enabled ? 'text-green-400' : 'text-gray-500'}>
                                    {plugin.enabled ? '● Active' : '○ Disabled'}
                                </span>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    )
}

// Helpers
function formatName(name: string) {
    return name
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase())
        .replace('Plugin', '')
}

function getPluginIcon(name: string) {
    if (name.includes('email')) return '📧'
    if (name.includes('spotify')) return '🎵'
    if (name.includes('calendar')) return '📅'
    if (name.includes('weather')) return '☀️'
    if (name.includes('discord')) return '💬'
    if (name.includes('github')) return '🐙'
    if (name.includes('notion')) return '📝'
    if (name.includes('cloud')) return '☁️'
    return '🔌'
}
