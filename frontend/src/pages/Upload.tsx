import { useState, useRef, useCallback } from 'react'
import { Upload as UploadIcon, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

type UploadState = 'idle' | 'uploading' | 'processing' | 'ready' | 'error'

interface DocInfo {
    document_id: number
    filename: string
    status: string
    page_count: number | null
}

const API_BASE = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api`

export default function UploadPage() {
    const [state, setState] = useState<UploadState>('idle')
    const [docInfo, setDocInfo] = useState<DocInfo | null>(null)
    const [error, setError] = useState('')
    const [dragOver, setDragOver] = useState(false)
    const fileInputRef = useRef<HTMLInputElement>(null)
    const navigate = useNavigate()

    const pollStatus = useCallback(async (docId: number, filename: string) => {
        const maxAttempts = 60
        for (let i = 0; i < maxAttempts; i++) {
            await new Promise((r) => setTimeout(r, 2000))
            try {
                const res = await fetch(`${API_BASE}/documents/${docId}/status`)
                if (!res.ok) continue
                const data = await res.json()
                if (data.status === 'ready') {
                    setDocInfo({ document_id: docId, filename, status: 'ready', page_count: data.page_count })
                    setState('ready')
                    return
                }
                if (data.status === 'failed') {
                    setError('Document processing failed.')
                    setState('error')
                    return
                }
            } catch {
                // keep polling
            }
        }
        setError('Timed out waiting for processing.')
        setState('error')
    }, [])

    const uploadFile = useCallback(
        async (file: File) => {
            if (file.type !== 'application/pdf') {
                setError('Only PDF files are accepted.')
                setState('error')
                return
            }
            setState('uploading')
            setError('')
            setDocInfo(null)

            const formData = new FormData()
            formData.append('file', file)

            try {
                const res = await fetch(`${API_BASE}/documents/upload`, {
                    method: 'POST',
                    body: formData,
                })
                if (!res.ok) {
                    const body = await res.json().catch(() => ({}))
                    throw new Error(body.detail || `Upload failed (${res.status})`)
                }
                const data = await res.json()
                setDocInfo({ document_id: data.document_id, filename: file.name, status: 'processing', page_count: null })
                setState('processing')
                pollStatus(data.document_id, file.name)
            } catch (e: any) {
                setError(e.message || 'Upload failed')
                setState('error')
            }
        },
        [pollStatus],
    )

    const onDrop = useCallback(
        (e: React.DragEvent) => {
            e.preventDefault()
            setDragOver(false)
            const file = e.dataTransfer.files[0]
            if (file) uploadFile(file)
        },
        [uploadFile],
    )

    const onFileSelect = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            const file = e.target.files?.[0]
            if (file) uploadFile(file)
        },
        [uploadFile],
    )

    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <div className="text-center">
                <h1 className="text-4xl font-bold mb-2 text-foreground">Upload Document</h1>
                <p className="text-muted-foreground">Upload a PDF to start chatting with it</p>
            </div>

            {/* Drop zone */}
            <div
                onDragOver={(e) => {
                    e.preventDefault()
                    setDragOver(true)
                }}
                onDragLeave={() => setDragOver(false)}
                onDrop={onDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`
          relative border-2 border-dashed rounded-xl p-12 text-center cursor-pointer
          transition-all duration-200
          ${dragOver ? 'border-primary bg-primary/5 scale-[1.01]' : 'border-border hover:border-primary/50 hover:bg-card'}
          ${state === 'uploading' || state === 'processing' ? 'pointer-events-none opacity-60' : ''}
        `}
            >
                <input ref={fileInputRef} type="file" accept=".pdf" className="hidden" onChange={onFileSelect} />
                <UploadIcon className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-lg font-medium text-foreground">
                    Drop your PDF here, or <span className="text-primary underline">browse</span>
                </p>
                <p className="text-sm text-muted-foreground mt-1">Up to 100 MB</p>
            </div>

            {/* Status card */}
            {state !== 'idle' && (
                <div className="rounded-xl border border-border bg-card p-6 shadow-sm space-y-4">
                    {state === 'uploading' && (
                        <div className="flex items-center gap-3 text-foreground">
                            <Loader2 className="w-5 h-5 animate-spin text-primary" />
                            <span>Uploading...</span>
                        </div>
                    )}

                    {state === 'processing' && (
                        <div className="space-y-3">
                            <div className="flex items-center gap-3 text-foreground">
                                <Loader2 className="w-5 h-5 animate-spin text-primary" />
                                <span>Processing "{docInfo?.filename}"...</span>
                            </div>
                            <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                                <div className="h-full bg-primary rounded-full animate-pulse w-2/3" />
                            </div>
                            <p className="text-sm text-muted-foreground">Extracting text and creating chunks</p>
                        </div>
                    )}

                    {state === 'ready' && docInfo && (
                        <div className="space-y-4">
                            <div className="flex items-center gap-3 text-accent">
                                <CheckCircle className="w-5 h-5" />
                                <span className="font-medium">Ready!</span>
                            </div>
                            <div className="flex items-center gap-3 text-foreground">
                                <FileText className="w-5 h-5 text-muted-foreground" />
                                <div>
                                    <p className="font-medium">{docInfo.filename}</p>
                                    <p className="text-sm text-muted-foreground">
                                        {docInfo.page_count} pages · Document #{docInfo.document_id}
                                    </p>
                                </div>
                            </div>
                            <button
                                onClick={() => navigate(`/chat?doc=${docInfo.document_id}`)}
                                className="w-full py-2.5 px-4 bg-primary text-primary-foreground rounded-lg font-medium
                  hover:opacity-90 transition-opacity"
                            >
                                Chat with this document →
                            </button>
                        </div>
                    )}

                    {state === 'error' && (
                        <div className="flex items-center gap-3 text-destructive">
                            <AlertCircle className="w-5 h-5" />
                            <span>{error}</span>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
