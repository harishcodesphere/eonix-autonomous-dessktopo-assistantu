import { motion } from 'framer-motion'
import { Message } from '../../types'

interface MessageBubbleProps {
    message: Message
}

/** Simple markdown-to-JSX renderer for chat messages */
function renderMarkdown(text: string) {
    // Split by code blocks first
    const parts = text.split(/(```[\s\S]*?```)/g)

    return parts.map((part, i) => {
        // Code blocks
        if (part.startsWith('```') && part.endsWith('```')) {
            const lines = part.slice(3, -3).split('\n')
            const lang = lines[0]?.trim() || ''
            const code = lang ? lines.slice(1).join('\n') : lines.join('\n')
            return (
                <div key={i} className="my-2 rounded-lg overflow-hidden">
                    {lang && (
                        <div className="bg-gray-900 px-3 py-1 text-[10px] text-gray-500 font-mono uppercase">
                            {lang}
                        </div>
                    )}
                    <pre className="bg-gray-900/90 px-3 py-2 overflow-x-auto text-xs font-mono text-green-300 leading-relaxed">
                        {code}
                    </pre>
                </div>
            )
        }

        // Inline formatting
        return (
            <span key={i}>
                {part.split('\n').map((line, j) => {
                    // Process inline formatting
                    let processed = line
                        // Bold
                        .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
                        // Italic
                        .replace(/\*(.+?)\*/g, '<i>$1</i>')
                        // Inline code
                        .replace(/`(.+?)`/g, '<code class="bg-gray-800 px-1 py-0.5 rounded text-cyan-300 text-xs font-mono">$1</code>')
                        // Bullet points
                        .replace(/^[-•]\s+(.*)/, '<span class="flex gap-2"><span class="text-cyan-500">•</span><span>$1</span></span>')
                        // Numbered lists
                        .replace(/^(\d+)\.\s+(.*)/, '<span class="flex gap-2"><span class="text-cyan-500 font-semibold">$1.</span><span>$2</span></span>')

                    return (
                        <span key={j}>
                            {j > 0 && <br />}
                            <span dangerouslySetInnerHTML={{ __html: processed }} />
                        </span>
                    )
                })}
            </span>
        )
    })
}

export function MessageBubble({ message }: MessageBubbleProps) {
    const isUser = message.role === 'user'
    const isSystem = message.role === 'system'

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
        >
            <div
                className={`max-w-[85%] rounded-2xl px-4 py-3 backdrop-blur-sm ${isUser
                    ? 'bg-cyan-500/20 border border-cyan-500/30 text-cyan-100 rounded-tr-none'
                    : isSystem
                        ? 'bg-yellow-500/10 border border-yellow-500/20 text-yellow-200 rounded-tl-none'
                        : 'bg-gray-800/60 border border-gray-700 text-gray-200 rounded-tl-none'
                    }`}
            >
                {/* Brain badge for assistant messages */}
                {!isUser && message.brain && (
                    <div className="flex items-center gap-1.5 mb-1.5">
                        <span className={`inline-flex items-center px-1.5 py-0.5 rounded text-[9px] font-mono uppercase tracking-wider
                            ${message.brain === 'gemini'
                                ? 'bg-purple-500/20 text-purple-300 border border-purple-500/20'
                                : message.brain === 'local'
                                    ? 'bg-green-500/20 text-green-300 border border-green-500/20'
                                    : 'bg-gray-500/20 text-gray-400 border border-gray-500/20'
                            }`}
                        >
                            {message.brain === 'local' ? '🧠 Ollama' : message.brain === 'gemini' ? '✨ Gemini' : `⚙️ ${message.brain}`}
                        </span>
                    </div>
                )}

                {/* Message content with markdown rendering */}
                <div className="text-sm whitespace-pre-wrap leading-relaxed">
                    {isUser ? message.content : renderMarkdown(message.content)}
                </div>

                {/* Action badges */}
                {message.actions && message.actions.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                        {message.actions.map((action, i) => (
                            <span
                                key={i}
                                className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono
                                    ${action.success
                                        ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                                        : 'bg-red-500/10 text-red-400 border border-red-500/20'
                                    }`}
                            >
                                {action.success ? '✓' : '✗'} {action.tool}
                            </span>
                        ))}
                    </div>
                )}

                {/* Timestamp */}
                <div className="mt-1 text-[10px] opacity-40 text-right">
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
            </div>
        </motion.div>
    )
}
