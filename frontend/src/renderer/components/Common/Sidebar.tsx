import { useState } from 'react'


interface SidebarProps {
    activeView: string
    onViewChange: (view: string) => void
}

export function Sidebar({ activeView, onViewChange }: SidebarProps) {
    const menuItems = [
        { id: 'chat', label: 'Chat', icon: '💬' },
        { id: 'dashboard', label: 'Dashboard', icon: '📊' },
        { id: 'plugins', label: 'Plugins', icon: '🧩' },
        { id: 'settings', label: 'Settings', icon: '⚙️' },
    ]

    return (
        <div className="w-16 h-full flex flex-col items-center py-4 bg-gray-900 border-r border-gray-800 backdrop-blur-md bg-opacity-80">
            <div className="mb-8 text-cyan-400 font-bold text-xl">E</div>

            <div className="flex-1 w-full space-y-4">
                {menuItems.map((item) => (
                    <button
                        key={item.id}
                        onClick={() => onViewChange(item.id)}
                        className={`w-10 h-10 mx-auto flex items-center justify-center rounded-xl transition-all duration-200 ${activeView === item.id
                            ? 'bg-cyan-500/20 text-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.3)]'
                            : 'text-gray-400 hover:text-white hover:bg-gray-800'
                            }`}
                        title={item.label}
                    >
                        <span className="text-lg">{item.icon}</span>
                    </button>
                ))}
            </div>
        </div>
    )
}
