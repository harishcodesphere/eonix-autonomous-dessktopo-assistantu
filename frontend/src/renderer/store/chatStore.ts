import { create } from 'zustand'
import { Message } from '../types'

interface ChatState {
    messages: Message[]
    isTyping: boolean
    addMessage: (msg: Message) => void
    setTyping: (status: boolean) => void
    clearChat: () => void
    getHistory: () => { role: string; content: string }[]
}

export const useChatStore = create<ChatState>((set, get) => ({
    messages: [],
    isTyping: false,
    addMessage: (msg) => set((state) => ({
        messages: [...state.messages, msg]
    })),
    setTyping: (status) => set({ isTyping: status }),
    clearChat: () => set({ messages: [] }),
    getHistory: () => {
        const msgs = get().messages
        // Return last 20 messages in the format the backend expects
        return msgs.slice(-20).map((m) => ({
            role: m.role,
            content: m.content
        }))
    },
}))
