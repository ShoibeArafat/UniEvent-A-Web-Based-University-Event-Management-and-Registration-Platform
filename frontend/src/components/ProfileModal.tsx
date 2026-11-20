import React, { useState, useEffect } from "react"
import { useAuth } from "../context/AuthContext"
import type { UserSession } from "../types/auth"
import {
  updateUserProfile,
  changePassword,
  getUserSessions,
  revokeUserSession,
} from "../services/authApi"
import { CloseIcon, UsersIcon, SparklesIcon, CalendarIcon } from "./Icons"

interface ProfileModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: (message: string) => void
}

export function ProfileModal({ isOpen, onClose, onSuccess }: ProfileModalProps) {
  const { user, token, updateUser, logout } = useAuth()
  const [activeTab, setActiveTab] = useState<"profile" | "password" | "sessions">("profile")

  // Edit Name State
  const [name, setName] = useState(user?.name || "")

  // Password State
  const [currentPassword, setCurrentPassword] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  // Sessions State
  const [sessions, setSessions] = useState<UserSession[]>([])
  const [loadingSessions, setLoadingSessions] = useState(false)

  // Status
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (user) {
      setName(user.name)
    }
  }, [user])

  // Load sessions when the sessions tab is opened
  useEffect(() => {
    if (isOpen && activeTab === "sessions" && token) {
      loadSessions()
    }
  }, [isOpen, activeTab, token])

  const loadSessions = async () => {
    if (!token) return
    setLoadingSessions(true)
    try {
      const data = await getUserSessions(token)
      setSessions(data)
    } catch {
      // Ignore
    } finally {
      setLoadingSessions(false)
    }
  }

  if (!isOpen || !user) return null

  const handleUpdateName = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!token || !name.trim()) return
    setError(null)
    setLoading(true)
    try {
      const updated = await updateUserProfile(token, name.trim())
      updateUser(updated)
      onSuccess("Profile name updated successfully!")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update profile.")
    } finally {
      setLoading(false)
    }
  }

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!token) return
    setError(null)

    if (newPassword.length < 6) {
      setError("New password must be at least 6 characters.")
      return
    }

    if (newPassword !== confirmPassword) {
      setError("New passwords do not match.")
      return
    }

    setLoading(true)
    try {
      await changePassword(token, currentPassword, newPassword)
      onSuccess("Password changed successfully! Other active sessions were signed out.")
      setCurrentPassword("")
      setNewPassword("")
      setConfirmPassword("")
      onClose()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to change password.")
    } finally {
      setLoading(false)
    }
  }

  const handleRevokeSession = async (sessionId: number) => {
    if (!token) return
    try {
      await revokeUserSession(token, sessionId)
      onSuccess("Session revoked successfully.")
      await loadSessions()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to revoke session.")
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container profile-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <div className="profile-header-info">
            <div className="profile-avatar-large">
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <div className="profile-name-row">
                <h2 className="modal-title">{user.name}</h2>
                <span className={`role-badge ${user.role === "Admin" ? "role-admin" : "role-user"}`}>
                  {user.role}
                </span>
              </div>
              <p className="modal-subtitle">{user.email}</p>
            </div>
          </div>
          <button className="modal-close-btn" onClick={onClose} aria-label="Close modal">
            <CloseIcon width={20} height={20} />
          </button>
        </div>

        {/* Tab navigation */}
        <div className="auth-tab-row">
          <button
            type="button"
            className={`auth-tab-btn ${activeTab === "profile" ? "active" : ""}`}
            onClick={() => { setActiveTab("profile"); setError(null) }}
          >
            Edit Profile
          </button>
          <button
            type="button"
            className={`auth-tab-btn ${activeTab === "password" ? "active" : ""}`}
            onClick={() => { setActiveTab("password"); setError(null) }}
          >
            Change Password
          </button>
          <button
            type="button"
            className={`auth-tab-btn ${activeTab === "sessions" ? "active" : ""}`}
            onClick={() => { setActiveTab("sessions"); setError(null) }}
          >
            Active Sessions
          </button>
        </div>

        {error && (
          <div className="auth-error-banner">
            <span>{error}</span>
          </div>
        )}

        {/* Tab 1: Edit Profile */}
        {activeTab === "profile" && (
          <form onSubmit={handleUpdateName} className="modal-form">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                className="form-input"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Email (Cannot be modified)</label>
              <input
                type="email"
                className="form-input"
                value={user.email}
                disabled
              />
            </div>
            <div className="form-group">
              <label>Assigned Role</label>
              <input
                type="text"
                className="form-input"
                value={user.role}
                disabled
              />
            </div>
            <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
              {loading ? "Saving Changes..." : "Update Profile"}
            </button>
          </form>
        )}

        {/* Tab 2: Change Password */}
        {activeTab === "password" && (
          <form onSubmit={handleChangePassword} className="modal-form">
            <div className="form-group">
              <label>Current Password</label>
              <input
                type="password"
                className="form-input"
                placeholder="••••••••"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>New Password (min 6)</label>
              <input
                type="password"
                className="form-input"
                placeholder="••••••••"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                minLength={6}
              />
            </div>
            <div className="form-group">
              <label>Confirm New Password</label>
              <input
                type="password"
                className="form-input"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={6}
              />
            </div>
            <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
              {loading ? "Updating Password..." : "Change Password"}
            </button>
          </form>
        )}

        {/* Tab 3: Active Sessions */}
        {activeTab === "sessions" && (
          <div className="sessions-list-container">
            <p className="sessions-explanation">
              These are devices that currently hold an active, revocable refresh token session in your database.
            </p>
            {loadingSessions ? (
              <div className="loading-state">Loading active sessions...</div>
            ) : sessions.length === 0 ? (
              <p className="empty-sessions-notice">No other active sessions found.</p>
            ) : (
              <div className="sessions-items">
                {sessions.map((sess) => (
                  <div key={sess.id} className="session-item-row">
                    <div>
                      <div className="session-device-name">
                        {sess.user_agent ? sess.user_agent.slice(0, 45) : "Browser Session"}
                      </div>
                      <div className="session-meta">
                        Created: {new Date(sess.created_at).toLocaleDateString()} • Expires: {new Date(sess.expires_at).toLocaleDateString()}
                      </div>
                    </div>
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={() => handleRevokeSession(sess.id)}
                    >
                      Revoke
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
