export interface Message {
    id: string
    role: 'user' | 'assistant' | 'system'
    content: string
    timestamp: number
    intent?: string
}

export interface SystemStats {
    cpu: { percent: number; cores: number }
    memory: { used_gb: number; total_gb: number; percent: number }
    disk: { used_gb: number; total_gb: number; percent: number }
    battery?: { percent: number; plugged: boolean }
}

export interface Plugin {
    name: string
    description: string
    version: string
    enabled: boolean
    key: string
}

export interface CommandResult {
    status: 'success' | 'error' | 'pending'
    data?: any
    message?: string
}
