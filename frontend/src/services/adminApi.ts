import type { User } from "../types/auth"
import type { AdminStats, AuditLogEntry } from "../types/admin"

const API_BASE = "/api/admin"

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMsg = `HTTP error ${res.status}`
    try {
      const err = await res.json()
      if (err.detail) errorMsg = err.detail
    } catch {
      // fallback
    }
    throw new Error(errorMsg)
  }
  return res.json() as Promise<T>
}

export async function getAdminStats(token: string): Promise<AdminStats> {
  const res = await fetch(`${API_BASE}/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return handleResponse<AdminStats>(res)
}

export async function getAdminUsers(
  token: string,
  params?: { search?: string; role?: string; status?: string }
): Promise<User[]> {
  const query = new URLSearchParams()
  if (params?.search) query.set("search", params.search)
  if (params?.role && params.role !== "All") query.set("role", params.role)
  if (params?.status && params.status !== "All") query.set("status", params.status)

  const url = query.toString() ? `${API_BASE}/users?${query.toString()}` : `${API_BASE}/users`
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return handleResponse<User[]>(res)
}

export async function updateUserStatus(
  userId: number,
  isBanned: boolean,
  banReason: string | undefined,
  token: string
): Promise<User> {
  const res = await fetch(`${API_BASE}/users/${userId}/status`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ is_banned: isBanned, ban_reason: banReason }),
  })
  return handleResponse<User>(res)
}

export async function updateUserRole(
  userId: number,
  role: string,
  token: string
): Promise<User> {
  const res = await fetch(`${API_BASE}/users/${userId}/role`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ role }),
  })
  return handleResponse<User>(res)
}

export async function getAuditLogs(
  token: string,
  limit: number = 50,
  action?: string
): Promise<AuditLogEntry[]> {
  const query = new URLSearchParams({ limit: String(limit) })
  if (action) query.set("action", action)

  const res = await fetch(`${API_BASE}/audit-logs?${query.toString()}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return handleResponse<AuditLogEntry[]>(res)
}
