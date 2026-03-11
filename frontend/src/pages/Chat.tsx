import { useState, useRef, useEffect, useCallback } from 'react'
import { Send, Loader2, FileText, Bot, User } from 'lucide-react'
import { useSearchParams } from 'react-router-dom'

interface Message {
    role: 'user' | 'assistant'
    content: string
    sources?: { page_start: number; page_end: number }[]
    streaming?: boolean
}

export default function ChatPage() {
    const [searchParams] = useSearchParams()
    const [documentId, setDocumentId] = useState(searchParams.get('doc') || '')
    const [question, setQuestion] = useState('')
    const [messages, setMessages] = useState<Message[]>([])
    const [isStreaming, setIsStreaming] = useState(false)
    const [wsError, setWsError] = useState('')
    const wsRef = useRef<WebSocket | null>(null)
    const messagesEndRef = useRef<HTMLDivElement>(null)
    const inputRef = useRef<HTMLInputElement>(null)

    // Auto-scroll
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    const closeWs = useCallback(() => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.close()
        }
        wsRef.current = null
    }, [])

    useEffect(() => () => closeWs(), [closeWs])

    const sendQuestion = useCallback(() => {
        const q = question.trim()
        const docId = parseInt(documentId, 10)
        if (!q || !docId || isStreaming) return

        setQuestion('')
        setWsError('')
        setIsStreaming(true)

        // Add user message
        setMessages((prev) => [...prev, { role: 'user', content: q }])
        // Add empty assistant message for streaming
        setMessages((prev) => [...prev, { role: 'assistant', content: '', streaming: true }])

        closeWs()

        const apiUrl = import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`
        const wsUrl = apiUrl.replace(/^http/, 'ws') + '/ws/chat'
        const ws = new WebSocket(wsUrl)
        wsRef.current = ws

        let fullAnswer = ''

        ws.onopen = () => {
            ws.send(JSON.stringify({ document_id: docId, question: q }))
        }

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)

            if (data.type === 'token') {
                fullAnswer += data.delta
                setMessages((prev) => {
                    const updated = [...prev]
                    const last = updated[updated.length - 1]
                    if (last?.role === 'assistant') {
                        updated[updated.length - 1] = { ...last, content: fullAnswer }
                    }
                    return updated
                })
            } else if (data.type === 'done') {
                setMessages((prev) => {
                    const updated = [...prev]
                    const last = updated[updated.length - 1]
                    if (last?.role === 'assistant') {
                        updated[updated.length - 1] = {
                            ...last,
                            content: data.answer,
                            sources: data.sources,
                            streaming: false,
                        }
                    }
                    return updated
                })
                setIsStreaming(false)
                closeWs()
                inputRef.current?.focus()
            } else if (data.type === 'error') {
                setWsError(data.message)
                setIsStreaming(false)
                // Remove the empty assistant msg
                setMessages((prev) => {
                    const updated = [...prev]
                    const last = updated[updated.length - 1]
                    if (last?.role === 'assistant' && last.content === '') {
                        updated.pop()
                    }
                    return updated
                })
                closeWs()
            }
        }

        ws.onerror = () => {
            setWsError('WebSocket connection failed')
            setIsStreaming(false)
            closeWs()
        }

        ws.onclose = () => {
            if (isStreaming) setIsStreaming(false)
        }
    }, [question, documentId, isStreaming, closeWs])

    return (
        <div className="max-w-3xl mx-auto flex flex-col h-[calc(100vh-12rem)]">
            {/* Header */}
            <div className="flex items-center gap-4 mb-4">
                <h1 className="text-2xl font-bold text-foreground">Chat</h1>
                <div className="flex items-center gap-2 ml-auto">
                    <label className="text-sm text-muted-foreground">Doc ID:</label>
                    <input
                        type="number"
                        value={documentId}
                        onChange={(e) => setDocumentId(e.target.value)}
                        placeholder="1"
                        className="w-20 px-2 py-1 text-sm rounded-md border border-input bg-card text-foreground
              focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto rounded-xl border border-border bg-card p-4 space-y-4 mb-4">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
                        <Bot className="w-12 h-12 mb-3 opacity-40" />
                        <p>Ask a question about your document</p>
                    </div>
                )}

                {messages.map((msg, i) => (
                    <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                        {msg.role === 'assistant' && (
                            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                                <Bot className="w-4 h-4 text-primary" />
                            </div>
                        )}
                        <div
                            className={`max-w-[80%] rounded-xl px-4 py-3 ${msg.role === 'user'
                                ? 'bg-primary text-primary-foreground'
                                : 'bg-muted text-foreground'
                                }`}
                        >
                            <p className="whitespace-pre-wrap text-sm leading-relaxed">
                                {msg.content}
                                {msg.streaming && <span className="inline-block w-1.5 h-4 ml-0.5 bg-primary animate-pulse rounded-sm" />}
                            </p>
                            {/* Source badges */}
                            {msg.sources && msg.sources.length > 0 && (
                                <div className="flex flex-wrap gap-1.5 mt-2 pt-2 border-t border-border/40">
                                    <FileText className="w-3.5 h-3.5 text-muted-foreground" />
                                    {msg.sources.map((s, si) => (
                                        <span
                                            key={si}
                                            className="text-xs px-1.5 py-0.5 rounded bg-background text-muted-foreground border border-border"
                                        >
                                            p.{s.page_start}–{s.page_end}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>
                        {msg.role === 'user' && (
                            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                                <User className="w-4 h-4 text-primary-foreground" />
                            </div>
                        )}
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Error */}
            {wsError && (
                <p className="text-sm text-destructive mb-2">{wsError}</p>
            )}

            {/* Input */}
            <form
                onSubmit={(e) => {
                    e.preventDefault()
                    sendQuestion()
                }}
                className="flex gap-2"
            >
                <input
                    ref={inputRef}
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question about your document..."
                    disabled={isStreaming || !documentId}
                    className="flex-1 px-4 py-3 rounded-xl border border-input bg-card text-foreground
            placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring
            disabled:opacity-50"
                />
                <button
                    type="submit"
                    disabled={isStreaming || !question.trim() || !documentId}
                    className="px-4 py-3 rounded-xl bg-primary text-primary-foreground
            hover:opacity-90 transition-opacity disabled:opacity-40 disabled:cursor-not-allowed"
                >
                    {isStreaming ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                </button>
            </form>
        </div>
    )
}
