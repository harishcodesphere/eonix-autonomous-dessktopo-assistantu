import { useState, useEffect, useRef } from 'react'
import { useChatStore } from '../../store/chatStore'
import { MessageBubble } from './MessageBubble'
import { useWebSocket } from '../../hooks/useWebSocket'
import { motion, AnimatePresence } from 'framer-motion'

const SUGGESTED_PROMPTS = [
    "What is machine learning?",
    "Write a Python function to sort a list",
    "Explain quantum computing simply",
    "What's the weather command?",
    "Tell me a programming joke",
    "How does the internet work?",
]

export function ChatInterface() {
    const { messages, isTyping, clearChat } = useChatStore()
    const { sendCommand } = useWebSocket()
    const scrollRef = useRef<HTMLDivElement>(null)
    const inputRef = useRef<HTMLTextAreaElement>(null)
    const [inputValue, setInputValue] = useState('')

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight
        }
    }, [messages, isTyping])

    const handleSend = () => {
        const text = inputValue.trim()
        if (text) {
            sendCommand(text)
            setInputValue('')
            // Reset textarea height
            if (inputRef.current) {
                inputRef.current.style.height = 'auto'
            }
        }
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputValue(e.target.value)
        // Auto-resize textarea
        const target = e.target
        target.style.height = 'auto'
        target.style.height = Math.min(target.scrollHeight, 120) + 'px'
    }

    return (
        <div className="flex flex-col h-full w-full max-w-3xl mx-auto">
            {/* Chat header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800/50">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                    <span className="text-xs font-mono text-gray-400 uppercase tracking-widest">
                        Eonix Chat
                    </span>
                </div>
                {messages.length > 0 && (
                    <button
                        onClick={clearChat}
                        className="text-xs text-gray-500 hover:text-gray-300 transition-colors font-mono"
                    >
                        Clear
                    </button>
                )}
            </div>

            {/* Messages area */}
            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto px-4 py-6 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent"
            >
                <div className="flex flex-col justify-end min-h-full">
                    <AnimatePresence>
                        {messages.length === 0 && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="my-auto text-center py-12"
                            >
                                <div className="text-4xl mb-4">🤖</div>
                                <h2 className="text-xl font-semibold text-gray-200 mb-2">
                                    Hey there! I'm Eonix.
                                </h2>
                                <p className="text-sm text-gray-500 mb-8 max-w-md mx-auto">
                                    Your AI desktop assistant. Ask me anything — science,
                                    code, math, or give me commands to control your PC.
                                </p>

                                {/* Suggested prompts */}
                                <div className="grid grid-cols-2 gap-2 max-w-lg mx-auto">
                                    {SUGGESTED_PROMPTS.map((prompt, i) => (
                                        <button
                                            key={i}
                                            onClick={() => {
                                                setInputValue(prompt)
                                                inputRef.current?.focus()
                                            }}
                                            className="text-left text-xs px-3 py-2.5 rounded-lg 
                                                border border-gray-700/50 bg-gray-800/30
                                                text-gray-400 hover:text-cyan-300 hover:border-cyan-500/30
                                                hover:bg-gray-800/60 transition-all duration-200"
                                        >
                                            {prompt}
                                        </button>
                                    ))}
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {messages.map((msg) => (
                        <MessageBubble key={msg.id} message={msg} />
                    ))}

                    {isTyping && (
                        <motion.div
                            initial={{ opacity: 0, y: 5 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex items-center space-x-2 p-4 text-cyan-400"
                        >
                            <div className="flex space-x-1">
                                <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                            <span className="text-xs uppercase tracking-widest font-mono">
                                Thinking
                            </span>
                        </motion.div>
                    )}
                </div>
            </div>

            {/* Input area */}
            <div className="p-4 border-t border-gray-800 bg-gray-900/50 backdrop-blur-md">
                <div className="flex items-end gap-2">
                    <textarea
                        ref={inputRef}
                        value={inputValue}
                        onChange={handleInput}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask me anything or give a command..."
                        rows={1}
                        className="flex-1 bg-gray-800/80 border border-gray-700 rounded-xl px-4 py-3 
                            text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500/50 
                            focus:ring-1 focus:ring-cyan-500/50 transition-all font-mono text-sm 
                            resize-none overflow-hidden min-h-[44px] max-h-[120px]"
                        autoFocus
                    />
                    <button
                        onClick={handleSend}
                        disabled={!inputValue.trim()}
                        className="flex-shrink-0 w-11 h-11 rounded-xl bg-cyan-500/20 border border-cyan-500/30 
                            text-cyan-400 hover:bg-cyan-500/30 hover:text-cyan-300
                            disabled:opacity-30 disabled:cursor-not-allowed
                            transition-all duration-200 flex items-center justify-center"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                            <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                        </svg>
                    </button>
                </div>
                <div className="flex items-center justify-between mt-2">
                    <span className="text-[10px] text-gray-600 font-mono">
                        Shift+Enter for new line
                    </span>
                    <span className="text-[10px] text-gray-600 font-mono">
                        {messages.length} messages
                    </span>
                </div>
            </div>
        </div>
    )
}
