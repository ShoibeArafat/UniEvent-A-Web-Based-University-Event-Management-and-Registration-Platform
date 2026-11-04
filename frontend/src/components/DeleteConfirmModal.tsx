import type { Event } from "../types/event"
import { TrashIcon, XIcon } from "./Icons"

interface DeleteConfirmModalProps {
  event: Event | null
  onClose: () => void
  onConfirm: (id: number) => Promise<void>
}

export function DeleteConfirmModal({ event, onClose, onConfirm }: DeleteConfirmModalProps) {
  if (!event) return null

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content modal-sm" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="flex items-center gap-2 text-danger">
            <TrashIcon width={22} height={22} />
            <h3 className="modal-title text-danger">Confirm Delete</h3>
          </div>
          <button className="btn-icon" onClick={onClose} aria-label="Close dialog">
            <XIcon width={20} height={20} />
          </button>
        </div>

        <div className="py-3">
          <p className="text-sm">
            Are you sure you want to permanently delete <strong>&ldquo;{event.title}&rdquo;</strong>?
          </p>
          <p className="text-xs text-muted mt-2">
            This action cannot be undone and will permanently remove the event record.
          </p>
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button
            className="btn btn-danger"
            onClick={async () => {
              await onConfirm(event.id)
              onClose()
            }}
          >
            Confirm Delete
          </button>
        </div>
      </div>
    </div>
  )
}
