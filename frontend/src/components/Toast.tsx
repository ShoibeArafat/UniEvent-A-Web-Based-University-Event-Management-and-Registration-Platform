import { useEffect } from "react"
import { XIcon } from "./Icons"

export interface ToastMessage {
  id: string
  type: "success" | "error" | "info"
  message: string
}

interface ToastProps {
  toasts: ToastMessage[]
  onDismiss: (id: string) => void
}

export function Toast({ toasts, onDismiss }: ToastProps) {
  useEffect(() => {
    if (toasts.length === 0) return
    const latest = toasts[toasts.length - 1]
    const timer = setTimeout(() => {
      onDismiss(latest.id)
    }, 4000)
    return () => clearTimeout(timer)
  }, [toasts, onDismiss])

  if (toasts.length === 0) return null

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast-${toast.type}`}>
          <div className="toast-message">{toast.message}</div>
          <button className="btn-icon btn-icon-sm" onClick={() => onDismiss(toast.id)}>
            <XIcon width={16} height={16} />
          </button>
        </div>
      ))}
    </div>
  )
}
