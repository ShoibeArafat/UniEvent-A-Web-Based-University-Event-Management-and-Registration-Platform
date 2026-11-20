import { useState, useEffect, useCallback } from "react"
import type { Event, EventCreateInput } from "./types/event"
import { getEvents, createEvent, updateEvent, deleteEvent } from "./services/api"
import { useAuth } from "./context/AuthContext"
import Login from "./Pages/Login"
import { Navbar } from "./components/Navbar"
import { EventCard } from "./components/EventCard"
import { EventModal } from "./components/EventModal"
import { EventDetailModal } from "./components/EventDetailModal"
import { DeleteConfirmModal } from "./components/DeleteConfirmModal"
import { ProfileModal } from "./components/ProfileModal"
import { Toast, type ToastMessage } from "./components/Toast"
import { SearchIcon, PlusIcon, CalendarIcon, SparklesIcon, UsersIcon } from "./components/Icons"

const CATEGORIES = ["All", "Technology", "Competition", "Workshop", "Cultural", "Seminar"]

export default function App() {
  const { user, token, isAuthenticated, isLoading } = useAuth()

  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Filtering states
  const [selectedCategory, setSelectedCategory] = useState("All")
  const [searchQuery, setSearchQuery] = useState("")

  // Event modal states
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingEvent, setEditingEvent] = useState<Event | null>(null)
  const [viewingEventId, setViewingEventId] = useState<number | null>(null)
  const [deletingEvent, setDeletingEvent] = useState<Event | null>(null)

  // Profile modal state
  const [profileModalOpen, setProfileModalOpen] = useState(false)

  // Toast feedback
  const [toasts, setToasts] = useState<ToastMessage[]>([])

  const addToast = (type: "success" | "error" | "info", message: string) => {
    const id = Math.random().toString(36).substring(2, 9)
    setToasts((prev) => [...prev, { id, type, message }])
  }

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }

  // Load events from API (Read List)
  const loadEvents = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getEvents({
        category: selectedCategory,
        search: searchQuery,
      })
      setEvents(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to connect to the UniEvent backend server.")
    } finally {
      setLoading(false)
    }
  }, [selectedCategory, searchQuery])

  useEffect(() => {
    if (isAuthenticated) {
      loadEvents()
    }
  }, [isAuthenticated, loadEvents])

  // Save Event (Create or Update)
  async function handleSaveEvent(data: EventCreateInput, eventId?: number) {
    if (eventId) {
      // PUT /api/events/{id} (Update)
      const updated = await updateEvent(eventId, data, token)
      addToast("success", `Event "${updated.title}" updated successfully!`)
    } else {
      // POST /api/events (Create)
      const created = await createEvent(data, token)
      addToast("success", `Event "${created.title}" published successfully!`)
    }
    await loadEvents()
  }

  // Delete Event (DELETE /api/events/{id})
  async function handleDeleteEvent(id: number) {
    try {
      const res = await deleteEvent(id, token)
      addToast("info", res.message || "Event removed successfully.")
      await loadEvents()
    } catch (err) {
      addToast("error", err instanceof Error ? err.message : "Failed to delete event.")
    }
  }

  // Modal open helpers
  function handleOpenCreate() {
    setEditingEvent(null)
    setIsModalOpen(true)
  }

  function handleOpenEdit(event: Event) {
    setEditingEvent(event)
    setIsModalOpen(true)
  }

  function handleOpenView(event: Event) {
    setViewingEventId(event.id)
  }

  function handleOpenDelete(event: Event) {
    setDeletingEvent(event)
  }

  // 1. Session Loading Screen
  if (isLoading) {
    return (
      <div className="login-loading-screen">
        <div className="spinner"></div>
        <p className="mt-3 text-muted">Checking authentication session...</p>
      </div>
    )
  }

  // 2. Unauthenticated: Show dedicated, standalone Login Page first
  if (!isAuthenticated) {
    return (
      <>
        <Login onSuccess={() => addToast("success", "Welcome to UniEvent Dashboard!")} />
        <Toast toasts={toasts} onDismiss={removeToast} />
      </>
    )
  }

  // 3. Authenticated: Render Full Dashboard
  const upcomingCount = events.filter((e) => e.status.toLowerCase() === "upcoming").length
  const uniqueOrganizers = new Set(events.map((e) => e.organizer)).size

  return (
    <div className="app-layout">
      {/* Navbar with brand, live user profile, role badge, and sign out */}
      <Navbar
        totalEvents={events.length}
        onOpenCreate={handleOpenCreate}
        onOpenProfile={() => setProfileModalOpen(true)}
        onLogoutToast={() => addToast("info", "You have signed out successfully.")}
      />

      {/* Main Container */}
      <main className="main-content">
        {/* Hero & Statistics Bar */}
        <section className="hero-section">
          <div className="hero-header">
            <div>
              <h2 className="hero-title">University Events Dashboard</h2>
              <p className="hero-subtitle">
                Welcome back, {user?.name}! Explore, schedule, and organize academic seminars, tech competitions, and activities.
              </p>
            </div>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon-wrapper bg-blue">
                <CalendarIcon width={22} height={22} className="text-primary" />
              </div>
              <div>
                <div className="stat-value">{events.length}</div>
                <div className="stat-label">Total Events</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon-wrapper bg-green">
                <SparklesIcon width={22} height={22} className="text-success" />
              </div>
              <div>
                <div className="stat-value">{upcomingCount}</div>
                <div className="stat-label">Upcoming Events</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon-wrapper bg-purple">
                <UsersIcon width={22} height={22} className="text-accent" />
              </div>
              <div>
                <div className="stat-value">{uniqueOrganizers}</div>
                <div className="stat-label">Active Organizers</div>
              </div>
            </div>
          </div>
        </section>

        {/* Filter and Search Bar */}
        <section className="filter-section">
          <div className="search-bar">
            <SearchIcon width={18} height={18} className="search-icon" />
            <input
              type="text"
              className="search-input"
              placeholder="Search by title, description, or organizer..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            {searchQuery && (
              <button className="search-clear" onClick={() => setSearchQuery("")}>
                Clear
              </button>
            )}
          </div>

          <div className="category-pills">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                className={`category-pill ${selectedCategory === cat ? "active" : ""}`}
                onClick={() => setSelectedCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </section>

        {/* Error notification banner */}
        {error && (
          <div className="alert alert-error my-4">
            <div>
              <strong>Connection Error:</strong> {error}
            </div>
            <button className="btn btn-secondary btn-sm" onClick={loadEvents}>
              Retry
            </button>
          </div>
        )}

        {/* Events Grid */}
        <section className="events-section">
          <div className="events-header">
            <h3 className="section-title">
              {selectedCategory === "All" ? "All Events" : `${selectedCategory} Events`}
            </h3>
            <span className="text-muted text-sm">
              Showing {events.length} {events.length === 1 ? "result" : "results"}
            </span>
          </div>

          {loading ? (
            <div className="loading-container">
              <div className="spinner"></div>
              <p className="mt-3 text-muted">Loading events...</p>
            </div>
          ) : events.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">
                <CalendarIcon width={48} height={48} />
              </div>
              <h4 className="empty-state-title">No events found</h4>
              <p className="empty-state-text">
                {searchQuery || selectedCategory !== "All"
                  ? "Try adjusting your search terms or category filter to discover more university events."
                  : "No events have been created yet. Be the first to publish a new university event!"}
              </p>
              <button className="btn btn-primary mt-4" onClick={handleOpenCreate}>
                <PlusIcon width={18} height={18} />
                <span>Create New Event</span>
              </button>
            </div>
          ) : (
            <div className="events-grid">
              {events.map((event) => (
                <EventCard
                  key={event.id}
                  event={event}
                  onView={handleOpenView}
                  onEdit={handleOpenEdit}
                  onDelete={handleOpenDelete}
                />
              ))}
            </div>
          )}
        </section>
      </main>

      {/* Modals */}
      {/* 1. Create / Edit Event Modal */}
      <EventModal
        isOpen={isModalOpen}
        initialData={editingEvent}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSaveEvent}
      />

      {/* 2. Read Single Event Detail Modal */}
      <EventDetailModal
        eventId={viewingEventId}
        onClose={() => setViewingEventId(null)}
        onEdit={(event) => {
          setViewingEventId(null)
          handleOpenEdit(event)
        }}
        onDelete={(event) => {
          setViewingEventId(null)
          handleOpenDelete(event)
        }}
      />

      {/* 3. Delete Confirmation Modal */}
      <DeleteConfirmModal
        event={deletingEvent}
        onClose={() => setDeletingEvent(null)}
        onConfirm={handleDeleteEvent}
      />

      {/* 4. User Profile & Active Sessions Modal */}
      <ProfileModal
        isOpen={profileModalOpen}
        onClose={() => setProfileModalOpen(false)}
        onSuccess={(msg) => addToast("success", msg)}
      />

      {/* Toast notifications */}
      <Toast toasts={toasts} onDismiss={removeToast} />
    </div>
  )
}
