import { motion } from 'framer-motion'
import { Message } from '../../types'

interface MessageBubbleProps {
    message: Message
}

export function MessageBubble({ message }: MessageBubbleProps) {
    const isUser = message.role === 'user'

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
        >
            <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 backdrop-blur-sm ${isUser
                        ? 'bg-cyan-500/20 border border-cyan-500/30 text-cyan-100 rounded-tr-none'
                        : 'bg-gray-800/60 border border-gray-700 text-gray-200 rounded-tl-none'
                    }`}
            >
                <div className="text-sm whitespace-pre-wrap leading-relaxed">
                    {message.content}
                </div>
                <div className="mt-1 text-[10px] opacity-40 text-right">
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
            </div>
        </motion.div>
    )
}
