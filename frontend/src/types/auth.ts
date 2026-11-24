export interface User {
  id: number
  name: string
  email: string
  role: "User" | "Admin" | string
  is_banned: boolean
  ban_reason?: string
  created_at?: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface UserSession {
  id: number
  user_agent?: string
  expires_at: string
  created_at: string
}
