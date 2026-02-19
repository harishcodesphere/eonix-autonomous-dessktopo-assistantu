import { io, Socket } from 'socket.io-client'
import { useEffect, useRef, useCallback } from 'react'
import { useSystemStore } from '../store/systemStore'
import { useChatStore } from '../store/chatStore'
import { nanoid } from 'nanoid'

const SOCKET_URL = 'http://localhost:8000'
const API_URL = 'http://localhost:8000'

export function useWebSocket() {
    const socketRef = useRef<Socket | null>(null)
    const { updateStats, setConnection } = useSystemStore()
    const { addMessage, setTyping, getHistory } = useChatStore()

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
                    brain: data.brain,
                    actions: data.actions,
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

    const sendCommand = useCallback((text: string) => {
        // Add user message immediately
        addMessage({
            id: nanoid(),
            role: 'user',
            content: text,
            timestamp: Date.now(),
        })

        setTyping(true)

        // Use SSE streaming via the /api/chat endpoint for richer responses
        const history = getHistory()

        fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                stream: true,
                history: history,
            }),
        }).then(async (response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const reader = response.body?.getReader()
            if (!reader) {
                throw new Error('No response body')
            }

            const decoder = new TextDecoder()
            let buffer = ''
            let finalReply = ''
            let finalBrain = ''
            let finalActions: any[] = []

            while (true) {
                const { done, value } = await reader.read()
                if (done) break

                buffer += decoder.decode(value, { stream: true })
                const lines = buffer.split('\n')
                buffer = lines.pop() || ''

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6))

                            if (data.type === 'complete') {
                                finalReply = data.reply || finalReply
                                finalBrain = data.brain || finalBrain
                                finalActions = data.actions || finalActions
                            } else if (data.type === 'action') {
                                finalActions.push({
                                    tool: data.tool,
                                    description: data.description || data.tool,
                                    success: data.success,
                                })
                            }
                        } catch {
                            // Skip non-JSON lines
                        }
                    }
                }
            }

            setTyping(false)

            if (finalReply) {
                addMessage({
                    id: nanoid(),
                    role: 'assistant',
                    content: finalReply,
                    timestamp: Date.now(),
                    brain: finalBrain,
                    actions: finalActions.length > 0 ? finalActions : undefined,
                })
            }
        }).catch((err) => {
            console.error('Chat API error:', err)
            setTyping(false)

            // Fallback to WebSocket if SSE fails
            if (socketRef.current) {
                socketRef.current.emit('command', { content: text })
                setTyping(true)
            } else {
                addMessage({
                    id: nanoid(),
                    role: 'assistant',
                    content: 'Connection error. Please check that the backend is running.',
                    timestamp: Date.now(),
                    brain: 'system',
                })
            }
        })
    }, [addMessage, setTyping, getHistory])

    return { sendCommand }
}
