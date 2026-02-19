import { create } from 'zustand'
import { Message } from '../types'

interface ChatState {
    messages: Message[]
    isTyping: boolean
    addMessage: (msg: Message) => void
    setTyping: (status: boolean) => void
    clearChat: () => void
}

export const useChatStore = create<ChatState>((set) => ({
    messages: [],
    isTyping: false,
    addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
    setTyping: (status) => set({ isTyping: status }),
    clearChat: () => set({ messages: [] }),
}))
