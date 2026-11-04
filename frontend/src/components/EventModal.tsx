import { useState, useEffect, type FormEvent } from "react"
import type { Event, EventCreateInput } from "../types/event"
import { XIcon } from "./Icons"

interface EventModalProps {
  isOpen: boolean
  onClose: () => void
  onSave: (data: EventCreateInput, eventId?: number) => Promise<void>
  initialData?: Event | null
}

const CATEGORIES = ["Technology", "Competition", "Workshop", "Cultural", "Seminar", "Sports", "Other"]
const STATUSES = ["Upcoming", "Ongoing", "Completed", "Cancelled"]

export function EventModal({ isOpen, onClose, onSave, initialData }: EventModalProps) {
  const isEditing = Boolean(initialData)

  const [formData, setFormData] = useState<EventCreateInput>({
    title: "",
    description: "",
    location: "",
    event_date: new Date().toISOString().split("T")[0],
    organizer: "",
    category: "Technology",
    capacity: 100,
    status: "Upcoming",
  })

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title,
        description: initialData.description,
        location: initialData.location,
        event_date: initialData.event_date,
        organizer: initialData.organizer,
        category: initialData.category,
        capacity: initialData.capacity,
        status: initialData.status,
      })
    } else {
      setFormData({
        title: "",
        description: "",
        location: "",
        event_date: new Date().toISOString().split("T")[0],
        organizer: "",
        category: "Technology",
        capacity: 100,
        status: "Upcoming",
      })
    }
    setError(null)
  }, [initialData, isOpen])

  if (!isOpen) return null

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)

    if (!formData.title.trim() || formData.title.trim().length < 2) {
      setError("Event title must be at least 2 characters.")
      return
    }
    if (!formData.description.trim() || formData.description.trim().length < 5) {
      setError("Please provide a descriptive explanation (at least 5 characters).")
      return
    }
    if (!formData.location.trim()) {
      setError("Venue or location is required.")
      return
    }
    if (!formData.organizer.trim()) {
      setError("Organizing department or club is required.")
      return
    }

    try {
      setIsSubmitting(true)
      await onSave(formData, initialData?.id)
      onClose()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save event.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <h2 className="modal-title">{isEditing ? "Edit University Event" : "Create New Event"}</h2>
            <p className="modal-subtitle">
              {isEditing ? "Update details for this event" : "Fill in the details to publish a new university event"}
            </p>
          </div>
          <button className="btn-icon" onClick={onClose} aria-label="Close dialog">
            <XIcon width={20} height={20} />
          </button>
        </div>

        {error && (
          <div className="alert alert-error">
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="event-form">
          <div className="form-group">
            <label htmlFor="title">Event Title *</label>
            <input
              id="title"
              type="text"
              className="form-input"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g. National Collegiate Programming Contest 2026"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="category">Category *</label>
              <select
                id="category"
                className="form-select"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="event_date">Event Date *</label>
              <input
                id="event_date"
                type="date"
                className="form-input"
                value={formData.event_date}
                onChange={(e) => setFormData({ ...formData, event_date: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="location">Location / Venue *</label>
              <input
                id="location"
                type="text"
                className="form-input"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                placeholder="e.g. Auditorium / Computer Lab 3"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="organizer">Organizer *</label>
              <input
                id="organizer"
                type="text"
                className="form-input"
                value={formData.organizer}
                onChange={(e) => setFormData({ ...formData, organizer: e.target.value })}
                placeholder="e.g. CSE Department / ACM Club"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="capacity">Max Capacity</label>
              <input
                id="capacity"
                type="number"
                min="1"
                max="10000"
                className="form-input"
                value={formData.capacity}
                onChange={(e) => setFormData({ ...formData, capacity: parseInt(e.target.value) || 1 })}
              />
            </div>

            <div className="form-group">
              <label htmlFor="status">Status</label>
              <select
                id="status"
                className="form-select"
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                {STATUSES.map((st) => (
                  <option key={st} value={st}>
                    {st}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="description">Description *</label>
            <textarea
              id="description"
              rows={4}
              className="form-textarea"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Provide event overview, schedule, rules, and speaker details..."
              required
            />
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
              {isSubmitting ? "Saving..." : isEditing ? "Save Changes" : "Create Event"}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
