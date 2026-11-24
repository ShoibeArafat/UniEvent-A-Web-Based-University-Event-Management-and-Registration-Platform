export interface AdminStats {
  total_users: number
  total_events: number
  total_teams: number
  active_sessions: number
  banned_users: number
  admin_count: number
}

export interface AuditLogEntry {
  id: number
  user_id?: number
  user_email?: string
  action: string
  resource_type: string
  resource_id?: string
  details?: string
  ip_address?: string
  created_at: string
}
