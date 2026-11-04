import { BuildingIcon, PlusIcon, SparklesIcon } from "./Icons"

interface NavbarProps {
  totalEvents: number
  onOpenCreate: () => void
}

export function Navbar({ totalEvents, onOpenCreate }: NavbarProps) {
  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="navbar-logo">
            <BuildingIcon className="w-6 h-6" width={24} height={24} />
          </div>
          <div>
            <div className="navbar-title-row">
              <h1 className="navbar-title">UniEvent</h1>
            </div>
            <p className="navbar-subtitle">University Event Management & Registration System</p>
          </div>
        </div>

        <div className="navbar-actions">
          <div className="event-count-badge">
            <SparklesIcon width={16} height={16} />
            <span>{totalEvents} {totalEvents === 1 ? "Event" : "Events"} Listed</span>
          </div>
          <button className="btn btn-primary" onClick={onOpenCreate}>
            <PlusIcon width={18} height={18} />
            <span>New Event</span>
          </button>
        </div>
      </div>
    </header>
  )
}
