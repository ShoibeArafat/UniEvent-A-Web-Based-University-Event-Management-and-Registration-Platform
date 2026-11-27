export type TeamRole = "Owner" | "Editor" | "Coordinator" | "Viewer"

export interface TeamMember {
  id: number
  user_id: number
  user_name: string
  user_email: string
  role: TeamRole
  joined_at: string
}

export interface EventTeam {
  id: number
  event_id: number
  name: string
  created_at: string
  members: TeamMember[]
}
