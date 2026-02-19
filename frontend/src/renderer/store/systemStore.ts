import { create } from 'zustand'
import { SystemStats } from '../types'

interface SystemState {
    stats: SystemStats | null
    isConnected: boolean
    updateStats: (stats: SystemStats) => void
    setConnection: (status: boolean) => void
}

export const useSystemStore = create<SystemState>((set) => ({
    stats: null,
    isConnected: false,
    updateStats: (stats) => set({ stats }),
    setConnection: (status) => set({ isConnected: status }),
}))
