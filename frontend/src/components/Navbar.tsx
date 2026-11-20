import { useState, useRef, useEffect } from "react"
import { BuildingIcon, PlusIcon, SparklesIcon, UsersIcon } from "./Icons"
import { useAuth } from "../context/AuthContext"

interface NavbarProps {
  totalEvents: number
  onOpenCreate: () => void
  onOpenProfile: () => void
  onLogoutToast: () => void
}

export function Navbar({
  totalEvents,
  onOpenCreate,
  onOpenProfile,
  onLogoutToast,
}: NavbarProps) {
  const { user, logout } = useAuth()
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const handleLogout = async () => {
    setDropdownOpen(false)
    await logout()
    onLogoutToast()
  }

  return (
    <header className="navbar">
      <div className="navbar-container">
        {/* Brand */}
        <div className="navbar-brand">
          <div className="navbar-logo">
            <BuildingIcon className="w-6 h-6" width={24} height={24} />
          </div>
          <div>
            <div className="navbar-title-row">
              <h1 className="navbar-title">UniEvent</h1>
            </div>
            <p className="navbar-subtitle">University Event Management & Registration Platform</p>
          </div>
        </div>

        {/* Actions & User State */}
        <div className="navbar-actions">
          <div className="event-count-badge">
            <SparklesIcon width={16} height={16} />
            <span>{totalEvents} {totalEvents === 1 ? "Event" : "Events"} Listed</span>
          </div>

          <button className="btn btn-primary" onClick={onOpenCreate}>
            <PlusIcon width={18} height={18} />
            <span>New Event</span>
          </button>

          {/* User Profile & Menu */}
          <div className="user-menu-container" ref={dropdownRef}>
              <button
                type="button"
                className="user-profile-button"
                onClick={() => setDropdownOpen(!dropdownOpen)}
                aria-expanded={dropdownOpen}
              >
                <div className="user-avatar-small">
                  {user?.name.charAt(0).toUpperCase()}
                </div>
                <div className="user-name-column">
                  <span className="user-display-name">{user?.name}</span>
                  <span className={`role-badge ${user?.role === "Admin" ? "role-admin" : "role-user"}`}>
                    {user?.role}
                  </span>
                </div>
              </button>

              {dropdownOpen && (
                <div className="user-dropdown-menu">
                  <div className="dropdown-user-header">
                    <p className="dropdown-name">{user?.name}</p>
                    <p className="dropdown-email">{user?.email}</p>
                  </div>
                  <hr className="dropdown-divider" />
                  <button
                    type="button"
                    className="dropdown-item"
                    onClick={() => {
                      setDropdownOpen(false)
                      onOpenProfile()
                    }}
                  >
                    My Profile & Sessions
                  </button>
                  <button
                    type="button"
                    className="dropdown-item text-danger"
                    onClick={handleLogout}
                  >
                    Sign Out
                  </button>
                </div>
              )}
            </div>
        </div>
      </div>
    </header>
  )
}
