import { useEffect, useRef } from 'react'
import { useChatStore } from '../../store/chatStore'
import { MessageBubble } from './MessageBubble'
import { useWebSocket } from '../../hooks/useWebSocket'

export function ChatInterface() {
    const { messages, isTyping } = useChatStore()
    const { sendCommand } = useWebSocket()
    const scrollRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight
        }
    }, [messages, isTyping])

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            const target = e.target as HTMLInputElement
            if (target.value.trim()) {
                sendCommand(target.value)
                target.value = ''
            }
        }
    }

    return (
        <div className="flex flex-col h-full w-full max-w-3xl mx-auto">
            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto px-4 py-6 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent"
            >
                <div className="flex flex-col justify-end min-h-full">
                    {messages.length === 0 && (
                        <div className="text-center text-gray-500 text-sm my-auto">
                            Listening for commands...
                        </div>
                    )}

                    {messages.map((msg) => (
                        <MessageBubble key={msg.id} message={msg} />
                    ))}

                    {isTyping && (
                        <div className="flex items-center space-x-2 p-4 text-cyan-400 animate-pulse text-xs uppercase tracking-widest font-mono">
                            <span>Thinking</span>
                            <span className="animate-bounce">.</span>
                            <span className="animate-bounce delay-100">.</span>
                            <span className="animate-bounce delay-200">.</span>
                        </div>
                    )}
                </div>
            </div>

            <div className="p-4 border-t border-gray-800 bg-gray-900/50 backdrop-blur-md">
                <input
                    type="text"
                    placeholder="Command..."
                    className="w-full bg-gray-800/80 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all font-mono text-sm"
                    onKeyDown={handleKeyDown}
                    autoFocus
                />
            </div>
        </div>
    )
}
