import { io, Socket } from 'socket.io-client'
import { useEffect, useRef } from 'react'
import { useSystemStore } from '../store/systemStore'
import { useChatStore } from '../store/chatStore'
import { nanoid } from 'nanoid'

const SOCKET_URL = 'http://localhost:8000'

export function useWebSocket() {
    const socketRef = useRef<Socket | null>(null)
    const { updateStats, setConnection } = useSystemStore()
    const { addMessage, setTyping } = useChatStore()

    useEffect(() => {
        socketRef.current = io(SOCKET_URL, {
            transports: ['websocket'],
            reconnectionAttempts: 5,
        })

        const socket = socketRef.current

        socket.on('connect', () => {
            console.log('Connected to backend')
            setConnection(true)
        })

        socket.on('disconnect', () => {
            console.log('Disconnected from backend')
            setConnection(false)
            setTyping(false)
        })

        socket.on('connect_error', (err) => {
            console.log('Connection error:', err)
            setConnection(false)
            setTyping(false)
        })

        socket.on('system_stats', (stats) => {
            updateStats(stats)
        })

        socket.on('response', (data) => {
            setTyping(false)
            if (data.response || data.message) {
                addMessage({
                    id: nanoid(),
                    role: 'assistant',
                    content: data.response || data.message,
                    timestamp: Date.now(),
                    intent: data.intent,
                })
            }
        })

        socket.on('status', (data) => {
            if (data.state === 'processing') {
                setTyping(true)
            }
        })

        return () => {
            socket.disconnect()
        }
    }, [])

    const sendCommand = (text: string) => {
        if (!socketRef.current) return

        // Add user message immediately
        addMessage({
            id: nanoid(),
            role: 'user',
            content: text,
            timestamp: Date.now(),
        })

        setTyping(true)
        socketRef.current.emit('command', { content: text })
    }

    return { sendCommand }
}
