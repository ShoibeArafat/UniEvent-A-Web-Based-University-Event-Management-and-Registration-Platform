import type { User, AuthTokens, UserSession } from "../types/auth"

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMessage = `Request failed with status ${res.status}`
    try {
      const errorData = await res.json()
      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail
      } else if (Array.isArray(errorData.detail)) {
        errorMessage = errorData.detail
          .map((err: { loc?: string[]; msg?: string }) => `${err.loc?.slice(-1)[0] || "Field"}: ${err.msg}`)
          .join(", ")
      } else if (errorData.message) {
        errorMessage = errorData.message
      }
    } catch {
      // Fallback if not json
    }
    throw new Error(errorMessage)
  }
  return res.json() as Promise<T>
}

export async function loginUser(email: string, password: string): Promise<AuthTokens> {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
  return handleResponse<AuthTokens>(res)
}

export async function signupUser(name: string, email: string, password: string): Promise<AuthTokens> {
  const res = await fetch("/api/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  })
  return handleResponse<AuthTokens>(res)
}

export async function refreshAccessToken(refreshToken: string): Promise<{ access_token: string; token_type: string }> {
  const res = await fetch("/api/auth/refresh", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
  return handleResponse<{ access_token: string; token_type: string }>(res)
}

export async function logoutUser(refreshToken: string): Promise<{ message: string }> {
  const res = await fetch("/api/auth/logout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
  return handleResponse<{ message: string }>(res)
}

export async function getCurrentUserProfile(token: string): Promise<User> {
  const res = await fetch("/api/users/me", {
    headers: { Authorization: `Bearer ${token}` },
  })
  return handleResponse<User>(res)
}

export async function updateUserProfile(token: string, name: string): Promise<User> {
  const res = await fetch("/api/users/me", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name }),
  })
  return handleResponse<User>(res)
}

export async function changePassword(
  token: string,
  currentPassword: string,
  newPassword: string
): Promise<{ message: string }> {
  const res = await fetch("/api/users/change-password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      current_password: currentPassword,
      new_password: newPassword,
    }),
  })
  return handleResponse<{ message: string }>(res)
}

export async function getUserSessions(token: string): Promise<UserSession[]> {
  const res = await fetch("/api/users/me/sessions", {
    headers: { Authorization: `Bearer ${token}` },
  })
  return handleResponse<UserSession[]>(res)
}

export async function revokeUserSession(token: string, sessionId: number): Promise<{ message: string }> {
  const res = await fetch(`/api/users/me/sessions/${sessionId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  })
  return handleResponse<{ message: string }>(res)
}
