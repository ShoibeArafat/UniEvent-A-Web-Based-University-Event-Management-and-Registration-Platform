/** authentication frontend */

import React, { createContext, useContext, useState, useEffect, useCallback } from "react"
import type { User } from "../types/auth"
import {
  loginUser,
  signupUser,
  refreshAccessToken,
  logoutUser,
  getCurrentUserProfile,
} from "../services/authApi"

interface AuthContextType {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (name: string, email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshSession: () => Promise<string | null>
  updateUser: (user: User) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const REFRESH_TOKEN_KEY = "unievent_refresh_token"

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Silently refresh token and fetch profile
  const refreshSession = useCallback(async (): Promise<string | null> => {
    const savedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)
    if (!savedRefreshToken) {
      setUser(null)
      setToken(null)
      return null
    }

    try {
      const data = await refreshAccessToken(savedRefreshToken)
      const newAccessToken = data.access_token
      setToken(newAccessToken)

      // Fetch user profile
      const profile = await getCurrentUserProfile(newAccessToken)
      setUser(profile)
      return newAccessToken
    } catch {
      // Refresh token is revoked or expired
      localStorage.removeItem(REFRESH_TOKEN_KEY)
      setUser(null)
      setToken(null)
      return null
    }
  }, [])

  // Restore session on initial application load
  useEffect(() => {
    async function initAuth() {
      await refreshSession()
      setIsLoading(false)
    }
    initAuth()
  }, [refreshSession])

  const login = async (email: string, password: string) => {
    const data = await loginUser(email, password)
    localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh_token)
    setToken(data.access_token)
    setUser(data.user)
  }

  const signup = async (name: string, email: string, password: string) => {
    const data = await signupUser(name, email, password)
    localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh_token)
    setToken(data.access_token)
    setUser(data.user)
  }

  const logout = async () => {
    const savedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)
    if (savedRefreshToken) {
      try {
        await logoutUser(savedRefreshToken)
      } catch {
        // Ignore logout network failure and clear local state
      }
    }
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    setUser(null)
    setToken(null)
  }

  const updateUser = (updated: User) => {
    setUser(updated)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        login,
        signup,
        logout,
        refreshSession,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
