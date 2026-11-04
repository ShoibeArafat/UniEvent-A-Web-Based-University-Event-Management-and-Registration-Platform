import { useState, useEffect } from "react"
import type { Event } from "../types/event"
import { getEventById } from "../services/api"
import { CalendarIcon, MapPinIcon, UsersIcon, XIcon, EditIcon, TrashIcon } from "./Icons"

interface EventDetailModalProps {
  eventId: number | null
  onClose: () => void
  onEdit: (event: Event) => void
  onDelete: (event: Event) => void
}

export function EventDetailModal({ eventId, onClose, onEdit, onDelete }: EventDetailModalProps) {
  const [event, setEvent] = useState<Event | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!eventId) {
      setEvent(null)
      return
    }

    let isMounted = true
    setLoading(true)
    setError(null)

    // Fires GET /api/events/{id} (Read Single)
    getEventById(eventId)
      .then((data) => {
        if (isMounted) setEvent(data)
      })
      .catch((err) => {
        if (isMounted) setError(err instanceof Error ? err.message : "Failed to load event details")
      })
      .finally(() => {
        if (isMounted) setLoading(false)
      })

    return () => {
      isMounted = false
    }
  }, [eventId])

  if (!eventId) return null

  function formatDate(dateStr?: string) {
    if (!dateStr) return "N/A"
    try {
      const d = new Date(dateStr)
      if (isNaN(d.getTime())) return dateStr
      return d.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric",
        year: "numeric",
      })
    } catch {
      return dateStr
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content modal-detail" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <div className="detail-tags-row">
              {event && <span className="badge badge-primary">{event.category}</span>}
              {event && <span className="badge badge-secondary">{event.status}</span>}
              <span className="badge badge-outline">ID: #{eventId}</span>
            </div>
            <h2 className="modal-title mt-2">{event?.title || "Loading Event Details..."}</h2>
          </div>
          <button className="btn-icon" onClick={onClose} aria-label="Close dialog">
            <XIcon width={20} height={20} />
          </button>
        </div>

        {loading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading event details...</p>
          </div>
        )}

        {error && (
          <div className="alert alert-error">
            <span>{error}</span>
          </div>
        )}

        {event && !loading && (
          <div className="detail-body">
            <div className="detail-grid">
              <div className="detail-info-card">
                <CalendarIcon width={18} height={18} className="meta-icon text-primary" />
                <div>
                  <div className="text-xs text-muted">Date & Time</div>
                  <div className="text-sm font-semibold">{formatDate(event.event_date)}</div>
                </div>
              </div>

              <div className="detail-info-card">
                <MapPinIcon width={18} height={18} className="meta-icon text-primary" />
                <div>
                  <div className="text-xs text-muted">Venue / Location</div>
                  <div className="text-sm font-semibold">{event.location}</div>
                </div>
              </div>

              <div className="detail-info-card">
                <UsersIcon width={18} height={18} className="meta-icon text-primary" />
                <div>
                  <div className="text-xs text-muted">Organizing Body</div>
                  <div className="text-sm font-semibold">{event.organizer}</div>
                </div>
              </div>

              <div className="detail-info-card">
                <UsersIcon width={18} height={18} className="meta-icon text-primary" />
                <div>
                  <div className="text-xs text-muted">Maximum Capacity</div>
                  <div className="text-sm font-semibold">{event.capacity} seats</div>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h4 className="detail-section-title">About this Event</h4>
              <p className="detail-description-text">{event.description}</p>
            </div>

            <div className="modal-footer">
              <div className="flex gap-2">
                <button
                  className="btn btn-outline"
                  onClick={() => {
                    onClose()
                    onEdit(event)
                  }}
                >
                  <EditIcon width={16} height={16} />
                  <span>Edit Event</span>
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => {
                    onClose()
                    onDelete(event)
                  }}
                >
                  <TrashIcon width={16} height={16} />
                  <span>Delete</span>
                </button>
              </div>

              <button className="btn btn-secondary" onClick={onClose}>
                Close
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
