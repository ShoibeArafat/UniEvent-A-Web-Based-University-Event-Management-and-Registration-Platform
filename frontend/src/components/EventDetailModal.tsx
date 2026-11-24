import { useState, useEffect } from "react"
import type { Event } from "../types/event"
import type { EventTeam, TeamRole } from "../types/team"
import { getEventById } from "../services/api"
import { getEventTeam, addTeamMember, updateTeamMemberRole, removeTeamMember } from "../services/teamApi"
import { CalendarIcon, MapPinIcon, UsersIcon, XIcon, EditIcon, TrashIcon, PlusIcon } from "./Icons"
import { useAuth } from "../context/AuthContext"

interface EventDetailModalProps {
  eventId: number | null
  onClose: () => void
  onEdit: (event: Event) => void
  onDelete: (event: Event) => void
}

export function EventDetailModal({ eventId, onClose, onEdit, onDelete }: EventDetailModalProps) {
  const { user, token } = useAuth()
  const [event, setEvent] = useState<Event | null>(null)
  const [team, setTeam] = useState<EventTeam | null>(null)
  const [activeTab, setActiveTab] = useState<"overview" | "team">("overview")
  const [loading, setLoading] = useState(false)
  const [teamLoading, setTeamLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [teamError, setTeamError] = useState<string | null>(null)

  // Invite member form state
  const [inviteEmail, setInviteEmail] = useState("")
  const [inviteRole, setInviteRole] = useState<TeamRole>("Editor")
  const [inviting, setInviting] = useState(false)

  const isOwner = Boolean(user && event?.creator_id && user.id === event.creator_id)
  const isAdmin = user?.role === "Admin"
  const isTeamEditor = Boolean(team?.members.some((m) => m.user_id === user?.id && (m.role === "Editor" || m.role === "Owner")))
  const canManage = isOwner || isAdmin || isTeamEditor
  const canManageTeam = isOwner || isAdmin

  // Load event details
  useEffect(() => {
    if (!eventId) {
      setEvent(null)
      setTeam(null)
      setActiveTab("overview")
      return
    }

    let isMounted = true
    setLoading(true)
    setError(null)

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

    // Load team in parallel
    setTeamLoading(true)
    getEventTeam(eventId, token)
      .then((data) => {
        if (isMounted) setTeam(data)
      })
      .catch(() => {
        // Ignore team load failure silently or show in tab
      })
      .finally(() => {
        if (isMounted) setTeamLoading(false)
      })

    return () => {
      isMounted = false
    }
  }, [eventId, token])

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

  const handleInviteSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!token || !inviteEmail.trim()) return

    setInviting(true)
    setTeamError(null)
    try {
      const updated = await addTeamMember(eventId, inviteEmail.trim(), inviteRole, token)
      setTeam(updated)
      setInviteEmail("")
    } catch (err) {
      setTeamError(err instanceof Error ? err.message : "Failed to invite member")
    } finally {
      setInviting(false)
    }
  }

  const handleRoleChange = async (userId: number, newRole: string) => {
    if (!token) return
    try {
      const updated = await updateTeamMemberRole(eventId, userId, newRole, token)
      setTeam(updated)
    } catch (err) {
      setTeamError(err instanceof Error ? err.message : "Failed to update role")
    }
  }

  const handleRemoveMember = async (userId: number) => {
    if (!token) return
    try {
      const updated = await removeTeamMember(eventId, userId, token)
      setTeam(updated)
    } catch (err) {
      setTeamError(err instanceof Error ? err.message : "Failed to remove member")
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

        {/* Tab switcher: Overview vs Organizing Team */}
        <div className="modal-tab-nav">
          <button
            type="button"
            className={`modal-tab-btn ${activeTab === "overview" ? "active" : ""}`}
            onClick={() => setActiveTab("overview")}
          >
            Overview
          </button>
          <button
            type="button"
            className={`modal-tab-btn ${activeTab === "team" ? "active" : ""}`}
            onClick={() => setActiveTab("team")}
          >
            Organizing Team ({team?.members.length || 0})
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
            {activeTab === "overview" ? (
              <>
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
              </>
            ) : (
              /* Organizing Team Tab */
              <div className="team-tab-content">
                <div className="team-tab-header">
                  <div>
                    <h4 className="font-bold text-base text-main">{team?.name || "Organizing Committee"}</h4>
                    <p className="text-xs text-muted">
                      Shared collaboration with 4 permission tiers: Owner, Editor, Coordinator, and Viewer.
                    </p>
                  </div>
                </div>

                {teamError && (
                  <div className="alert alert-error my-2">
                    <span>{teamError}</span>
                  </div>
                )}

                {/* Add member form for Owners / Admins */}
                {canManageTeam && (
                  <form onSubmit={handleInviteSubmit} className="team-invite-form">
                    <div className="form-group flex-1">
                      <input
                        type="email"
                        className="form-input text-sm"
                        placeholder="Invite student by email (e.g. organizer@unievent.edu)"
                        value={inviteEmail}
                        onChange={(e) => setInviteEmail(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <select
                        className="form-input text-sm"
                        value={inviteRole}
                        onChange={(e) => setInviteRole(e.target.value as TeamRole)}
                      >
                        <option value="Editor">Editor (Can edit event)</option>
                        <option value="Coordinator">Coordinator (Manage logistics)</option>
                        <option value="Viewer">Viewer (Read-only)</option>
                      </select>
                    </div>
                    <button type="submit" className="btn btn-primary btn-sm" disabled={inviting}>
                      <PlusIcon width={14} height={14} />
                      <span>{inviting ? "Adding..." : "Add Member"}</span>
                    </button>
                  </form>
                )}

                {/* Team roster */}
                {teamLoading ? (
                  <div className="p-4 text-center text-muted">Loading organizing team...</div>
                ) : (
                  <div className="team-members-list">
                    {team?.members.map((member) => (
                      <div key={member.id} className="team-member-row">
                        <div className="team-member-info">
                          <div className="user-avatar-small">
                            {member.user_name.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <div className="font-semibold text-sm text-main">{member.user_name}</div>
                            <div className="text-xs text-muted">{member.user_email}</div>
                          </div>
                        </div>

                        <div className="team-member-controls">
                          {canManageTeam && member.role !== "Owner" ? (
                            <select
                              className="role-select"
                              value={member.role}
                              onChange={(e) => handleRoleChange(member.user_id, e.target.value)}
                            >
                              <option value="Editor">Editor</option>
                              <option value="Coordinator">Coordinator</option>
                              <option value="Viewer">Viewer</option>
                            </select>
                          ) : (
                            <span className={`badge badge-role-${member.role.toLowerCase()}`}>
                              {member.role}
                            </span>
                          )}

                          {canManageTeam && member.role !== "Owner" && (
                            <button
                              type="button"
                              className="btn btn-icon text-danger"
                              onClick={() => handleRemoveMember(member.user_id)}
                              title="Remove from team"
                            >
                              <TrashIcon width={14} height={14} />
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            <div className="modal-footer">
              {canManage ? (
                <div className="flex gap-2">
                  <button
                    className="btn btn-outline"
                    onClick={() => {
                      onClose()
                      onEdit(event)
                    }}
                    title={isOwner ? "Edit your event" : "Edit as Editor / Admin"}
                  >
                    <EditIcon width={16} height={16} />
                    <span>Edit Event</span>
                  </button>
                  {isOwner || isAdmin ? (
                    <button
                      className="btn btn-danger"
                      onClick={() => {
                        onClose()
                        onDelete(event)
                      }}
                      title="Delete event permanently"
                    >
                      <TrashIcon width={16} height={16} />
                      <span>Delete</span>
                    </button>
                  ) : null}
                </div>
              ) : (
                <div className="text-sm text-muted">
                  Organized by <strong>{event.organizer}</strong>
                  {event.creator_name ? ` (Created by ${event.creator_name})` : ""}
                </div>
              )}

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
