import { useState, useEffect } from 'react'

interface Process {
    pid: number
    name: string
    cpu_percent: number
    memory_percent: number
}

// Mock data until API is ready
const MOCK_PROCESSES: Process[] = [
    { pid: 1234, name: 'chrome.exe', cpu_percent: 12.5, memory_percent: 4.2 },
    { pid: 5678, name: 'code.exe', cpu_percent: 5.1, memory_percent: 8.5 },
    { pid: 9101, name: 'spotify.exe', cpu_percent: 1.2, memory_percent: 2.1 },
    { pid: 1121, name: 'python.exe', cpu_percent: 0.5, memory_percent: 1.1 },
]

export function ProcessList() {
    const [processes, setProcesses] = useState<Process[]>(MOCK_PROCESSES)

    // In real app, fetch from /api/system/processes

    return (
        <div className="bg-gray-800/40 backdrop-blur-md border border-gray-700/50 rounded-xl overflow-hidden text-sm">
            <div className="grid grid-cols-4 bg-gray-800/60 p-3 font-semibold text-gray-400">
                <div>Name</div>
                <div className="text-right">PID</div>
                <div className="text-right">CPU</div>
                <div className="text-right">Memory</div>
            </div>
            <div className="divide-y divide-gray-700/50 max-h-64 overflow-y-auto">
                {processes.map((proc) => (
                    <div key={proc.pid} className="grid grid-cols-4 p-3 hover:bg-white/5 transition-colors">
                        <div className="text-white font-medium">{proc.name}</div>
                        <div className="text-right text-gray-500 font-mono">{proc.pid}</div>
                        <div className="text-right text-cyan-400 font-mono">{proc.cpu_percent}%</div>
                        <div className="text-right text-purple-400 font-mono">{proc.memory_percent}%</div>
                    </div>
                ))}
            </div>
        </div>
    )
}
