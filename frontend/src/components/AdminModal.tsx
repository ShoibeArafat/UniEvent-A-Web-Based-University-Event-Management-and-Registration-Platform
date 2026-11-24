import React, { useState, useEffect, useCallback } from "react"
import { useAuth } from "../context/AuthContext"
import type { User } from "../types/auth"
import type { AdminStats, AuditLogEntry } from "../types/admin"
import {
  getAdminStats,
  getAdminUsers,
  updateUserStatus,
  updateUserRole,
  getAuditLogs,
  downloadCsvReport,
} from "../services/adminApi"
import {
  UsersIcon,
  CalendarIcon,
  SparklesIcon,
  SearchIcon,
  XIcon,
} from "./Icons"

interface AdminModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccessToast?: (msg: string) => void
}

export function AdminModal({ isOpen, onClose, onSuccessToast }: AdminModalProps) {
  const { user, token } = useAuth()
  const [activeTab, setActiveTab] = useState<"overview" | "users" | "audit">("overview")

  // Data states
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [users, setUsers] = useState<User[]>([])
  const [auditLogs, setAuditLogs] = useState<AuditLogEntry[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // User filters
  const [searchQuery, setSearchQuery] = useState("")
  const [roleFilter, setRoleFilter] = useState("All")
  const [statusFilter, setStatusFilter] = useState("All")

  // Load Admin Stats
  const loadStats = useCallback(async () => {
    if (!token) return
    try {
      const data = await getAdminStats(token)
      setStats(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load admin stats")
    }
  }, [token])

  // Load User Directory
  const loadUsers = useCallback(async () => {
    if (!token) return
    try {
      setLoading(true)
      const data = await getAdminUsers(token, {
        search: searchQuery,
        role: roleFilter,
        status: statusFilter,
      })
      setUsers(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load user directory")
    } finally {
      setLoading(false)
    }
  }, [token, searchQuery, roleFilter, statusFilter])

  // Load Audit Trail
  const loadAuditLogs = useCallback(async () => {
    if (!token) return
    try {
      setLoading(true)
      const data = await getAuditLogs(token, 50)
      setAuditLogs(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load audit logs")
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    if (!isOpen || !token) return
    loadStats()
    if (activeTab === "users") loadUsers()
    if (activeTab === "audit") loadAuditLogs()
  }, [isOpen, activeTab, token, loadStats, loadUsers, loadAuditLogs])

  if (!isOpen || user?.role !== "Admin") return null

  // Handle Ban / Unban
  const handleToggleBan = async (targetUser: User) => {
    if (!token) return
    if (user?.email !== "admin1@unievent.edu") {
      alert("Permission denied: Only Primary Administrator (admin1@unievent.edu) can ban or unban accounts.")
      return
    }
    const willBan = !targetUser.is_banned
    let reason: string | undefined = undefined

    if (willBan) {
      const promptReason = window.prompt(
        `Enter the suspension reason for ${targetUser.name} (${targetUser.email}):`,
        "Violation of university event conduct policy"
      )
      if (promptReason === null) return // cancelled
      reason = promptReason || "Policy violation"
    }

    try {
      await updateUserStatus(targetUser.id, willBan, reason, token)
      onSuccessToast?.(
        willBan
          ? `User ${targetUser.name} has been suspended.`
          : `User ${targetUser.name} has been reactivated.`
      )
      await loadUsers()
      await loadStats()
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to update user status")
    }
  }

  // Handle Role Change
  const handleRoleChange = async (userId: number, newRole: string) => {
    if (!token) return
    try {
      await updateUserRole(userId, newRole, token)
      onSuccessToast?.(`User role updated to ${newRole}.`)
      await loadUsers()
      await loadStats()
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to change user role")
    }
  }

  // Handle CSV Export
  const handleExport = async (type: "events" | "users") => {
    if (!token) return
    try {
      await downloadCsvReport(type, token)
      onSuccessToast?.(`Downloaded ${type} CSV report!`)
    } catch (err) {
      alert(err instanceof Error ? err.message : "Export failed")
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content modal-admin" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <div>
            <div className="flex items-center gap-2">
              <span className="badge badge-admin-control">Admin Center</span>
              <span className="text-xs text-muted">System Administration & Oversight</span>
            </div>
            <h2 className="modal-title mt-1">Platform Admin Dashboard</h2>
          </div>
          <button className="btn-icon" onClick={onClose} aria-label="Close dialog">
            <XIcon width={20} height={20} />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="modal-tab-nav">
          <button
            type="button"
            className={`modal-tab-btn ${activeTab === "overview" ? "active" : ""}`}
            onClick={() => setActiveTab("overview")}
          >
            Overview & KPIs
          </button>
          <button
            type="button"
            className={`modal-tab-btn ${activeTab === "users" ? "active" : ""}`}
            onClick={() => setActiveTab("users")}
          >
            User Directory ({stats?.total_users || 0})
          </button>
          <button
            type="button"
            className={`modal-tab-btn ${activeTab === "audit" ? "active" : ""}`}
            onClick={() => setActiveTab("audit")}
          >
            Audit Trail
          </button>
        </div>

        {error && (
          <div className="alert alert-error my-3">
            <span>{error}</span>
          </div>
        )}

        <div className="admin-body">
          {/* TAB 1: OVERVIEW */}
          {activeTab === "overview" && stats && (
            <div className="admin-overview">
              <div className="admin-kpi-grid">
                <div className="admin-kpi-card">
                  <div className="admin-kpi-icon bg-blue">
                    <UsersIcon width={24} height={24} className="text-primary" />
                  </div>
                  <div>
                    <div className="admin-kpi-value">{stats.total_users}</div>
                    <div className="admin-kpi-label">Registered Accounts</div>
                  </div>
                </div>

                <div className="admin-kpi-card">
                  <div className="admin-kpi-icon bg-green">
                    <CalendarIcon width={24} height={24} className="text-success" />
                  </div>
                  <div>
                    <div className="admin-kpi-value">{stats.total_events}</div>
                    <div className="admin-kpi-label">University Events</div>
                  </div>
                </div>

                <div className="admin-kpi-card">
                  <div className="admin-kpi-icon bg-purple">
                    <SparklesIcon width={24} height={24} className="text-accent" />
                  </div>
                  <div>
                    <div className="admin-kpi-value">{stats.total_teams}</div>
                    <div className="admin-kpi-label">Organizing Teams</div>
                  </div>
                </div>

                <div className="admin-kpi-card">
                  <div className="admin-kpi-icon bg-amber">
                    <UsersIcon width={24} height={24} className="text-warning" />
                  </div>
                  <div>
                    <div className="admin-kpi-value">{stats.active_sessions}</div>
                    <div className="admin-kpi-label">Active Sessions</div>
                  </div>
                </div>

                <div className="admin-kpi-card">
                  <div className="admin-kpi-icon bg-red">
                    <XIcon width={24} height={24} className="text-danger" />
                  </div>
                  <div>
                    <div className="admin-kpi-value">{stats.banned_users}</div>
                    <div className="admin-kpi-label">Suspended Accounts</div>
                  </div>
                </div>

                <div className="admin-kpi-card">
                  <div className="admin-kpi-icon bg-blue">
                    <UsersIcon width={24} height={24} className="text-primary" />
                  </div>
                  <div>
                    <div className="admin-kpi-value">{stats.admin_count}</div>
                    <div className="admin-kpi-label">System Admins</div>
                  </div>
                </div>
              </div>

              {/* Reports & Exports */}
              <div className="admin-export-section mt-6">
                <h4 className="font-bold text-sm text-main mb-2">Export Official Reports (CSV)</h4>
                <p className="text-xs text-muted mb-3">
                  Download spreadsheet data for faculty committee meetings, university records, and audits.
                </p>
                <div className="flex gap-3">
                  <button
                    type="button"
                    className="btn btn-secondary btn-sm"
                    onClick={() => handleExport("events")}
                  >
                    Download Events CSV
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary btn-sm"
                    onClick={() => handleExport("users")}
                  >
                    Download Users CSV
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: USER DIRECTORY */}
          {activeTab === "users" && (
            <div className="admin-users-tab">
              {/* Search & Filter Bar */}
              <div className="admin-filter-bar">
                <div className="search-bar flex-1">
                  <SearchIcon width={16} height={16} className="search-icon" />
                  <input
                    type="text"
                    className="search-input text-sm"
                    placeholder="Search users by name or email..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
                <div className="flex gap-2">
                  <select
                    className="form-input text-sm"
                    value={roleFilter}
                    onChange={(e) => setRoleFilter(e.target.value)}
                  >
                    <option value="All">All Roles</option>
                    <option value="Admin">Admin</option>
                    <option value="User">User</option>
                  </select>
                  <select
                    className="form-input text-sm"
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                  >
                    <option value="All">All Statuses</option>
                    <option value="Active">Active</option>
                    <option value="Banned">Suspended</option>
                  </select>
                </div>
              </div>

              {/* Table */}
              {loading ? (
                <div className="p-8 text-center text-muted">Loading users...</div>
              ) : (
                <div className="admin-table-wrapper">
                  <table className="admin-table">
                    <thead>
                      <tr>
                        <th>User</th>
                        <th>Role</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.map((u) => {
                        const isSelf = u.id === user.id
                        const isTargetPrimaryAdmin = u.email === "admin1@unievent.edu"
                        const isPrimaryAdmin = user?.email === "admin1@unievent.edu"
                        return (
                          <tr key={u.id}>
                            <td>
                              <div className="font-semibold text-sm text-main">
                                {u.name} {isSelf && <span className="text-xs text-muted">(You)</span>}
                              </div>
                              <div className="text-xs text-muted">{u.email}</div>
                              {u.is_banned && u.ban_reason && (
                                <div className="text-xs text-danger mt-0.5">Reason: {u.ban_reason}</div>
                              )}
                            </td>
                            <td>
                              {!isSelf && !isTargetPrimaryAdmin ? (
                                <select
                                  className="role-select"
                                  value={u.role}
                                  onChange={(e) => handleRoleChange(u.id, e.target.value)}
                                >
                                  <option value="User">User</option>
                                  <option value="Admin">Admin</option>
                                </select>
                              ) : (
                                <span className="badge badge-admin-control">{u.role}</span>
                              )}
                            </td>
                            <td>
                              <span className={`badge ${u.is_banned ? "badge-status-cancelled" : "badge-status-ongoing"}`}>
                                {u.is_banned ? "Suspended" : "Active"}
                              </span>
                            </td>
                            <td>
                              {!isSelf && (
                                isPrimaryAdmin ? (
                                  <button
                                    type="button"
                                    className={`btn btn-sm ${u.is_banned ? "btn-secondary" : "btn-danger"}`}
                                    onClick={() => handleToggleBan(u)}
                                    disabled={isTargetPrimaryAdmin}
                                    title={isTargetPrimaryAdmin ? "Primary Admin cannot be suspended" : undefined}
                                  >
                                    {u.is_banned ? "Reactivate" : "Suspend"}
                                  </button>
                                ) : (
                                  <span className="text-xs text-muted" title="Only Primary Admin (admin1) has ban/unban authority">
                                    Admin1 Only
                                  </span>
                                )
                              )}
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* TAB 3: AUDIT TRAIL */}
          {activeTab === "audit" && (
            <div className="admin-audit-tab">
              {loading ? (
                <div className="p-8 text-center text-muted">Loading audit logs...</div>
              ) : auditLogs.length === 0 ? (
                <div className="p-8 text-center text-muted">No audit activity logged yet.</div>
              ) : (
                <div className="admin-table-wrapper">
                  <table className="admin-table">
                    <thead>
                      <tr>
                        <th>Timestamp</th>
                        <th>Action</th>
                        <th>Actor</th>
                        <th>Resource</th>
                        <th>Details</th>
                      </tr>
                    </thead>
                    <tbody>
                      {auditLogs.map((log) => (
                        <tr key={log.id}>
                          <td className="text-xs text-muted whitespace-nowrap">
                            {new Date(log.created_at).toLocaleString()}
                          </td>
                          <td>
                            <span className="badge badge-primary text-xs">{log.action}</span>
                          </td>
                          <td className="text-xs font-semibold">{log.user_email || "System"}</td>
                          <td className="text-xs text-muted">
                            {log.resource_type} {log.resource_id ? `#${log.resource_id}` : ""}
                          </td>
                          <td className="text-xs text-muted">{log.details || "—"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="modal-footer">
          <span className="text-xs text-muted">
            Logged in as Administrator: <strong>{user.name}</strong>
          </span>
          <button className="btn btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  )
}
