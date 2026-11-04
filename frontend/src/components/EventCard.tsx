import type { Event } from "../types/event"
import { CalendarIcon, MapPinIcon, UsersIcon, EditIcon, TrashIcon, EyeIcon } from "./Icons"

interface EventCardProps {
  event: Event
  onView: (event: Event) => void
  onEdit: (event: Event) => void
  onDelete: (event: Event) => void
}

export function EventCard({ event, onView, onEdit, onDelete }: EventCardProps) {
  // Format date nicely
  function formatDate(dateStr: string) {
    try {
      const d = new Date(dateStr)
      if (isNaN(d.getTime())) return dateStr
      return d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      })
    } catch {
      return dateStr
    }
  }

  // Category badge color class
  const getCategoryClass = (category: string) => {
    switch (category.toLowerCase()) {
      case "technology":
        return "badge-category-tech"
      case "competition":
        return "badge-category-comp"
      case "workshop":
        return "badge-category-workshop"
      case "cultural":
        return "badge-category-cultural"
      case "seminar":
        return "badge-category-seminar"
      default:
        return "badge-category-default"
    }
  }

  const getStatusClass = (status: string) => {
    switch (status.toLowerCase()) {
      case "upcoming":
        return "badge-status-upcoming"
      case "ongoing":
        return "badge-status-ongoing"
      case "completed":
        return "badge-status-completed"
      case "cancelled":
        return "badge-status-cancelled"
      default:
        return "badge-status-upcoming"
    }
  }

  return (
    <div className="event-card">
      <div className="event-card-header">
        <span className={`badge ${getCategoryClass(event.category)}`}>{event.category}</span>
        <span className={`badge ${getStatusClass(event.status)}`}>{event.status}</span>
      </div>

      <h3 className="event-title" title={event.title}>
        {event.title}
      </h3>

      <p className="event-description">
        {event.description}
      </p>

      <div className="event-meta-list">
        <div className="event-meta-item">
          <CalendarIcon width={16} height={16} className="meta-icon" />
          <span>{formatDate(event.event_date)}</span>
        </div>

        <div className="event-meta-item">
          <MapPinIcon width={16} height={16} className="meta-icon" />
          <span className="truncate">{event.location}</span>
        </div>

        <div className="event-meta-item">
          <UsersIcon width={16} height={16} className="meta-icon" />
          <span className="truncate">By {event.organizer} • Max {event.capacity}</span>
        </div>
      </div>

      <div className="event-card-footer">
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => onView(event)}
          title="View event details"
        >
          <EyeIcon width={15} height={15} />
          <span>Details</span>
        </button>

        <div className="event-card-actions">
          <button
            className="btn btn-outline btn-sm"
            onClick={() => onEdit(event)}
            title="Edit event"
          >
            <EditIcon width={15} height={15} />
            <span>Edit</span>
          </button>
          <button
            className="btn btn-danger btn-sm"
            onClick={() => onDelete(event)}
            title="Delete event"
          >
            <TrashIcon width={15} height={15} />
            <span>Delete</span>
          </button>
        </div>
      </div>
    </div>
  )
}
