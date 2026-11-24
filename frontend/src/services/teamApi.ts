import type { EventTeam } from "../types/team"

const API_BASE = "/api/events"

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

export async function getEventTeam(eventId: number, token?: string | null): Promise<EventTeam> {
  const headers: Record<string, string> = {}
  if (token) headers["Authorization"] = `Bearer ${token}`
  const res = await fetch(`${API_BASE}/${eventId}/team`, { headers })
  return handleResponse<EventTeam>(res)
}

export async function addTeamMember(
  eventId: number,
  email: string,
  role: string,
  token: string
): Promise<EventTeam> {
  const res = await fetch(`${API_BASE}/${eventId}/team/members`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ email, role }),
  })
  return handleResponse<EventTeam>(res)
}

export async function updateTeamMemberRole(
  eventId: number,
  userId: number,
  role: string,
  token: string
): Promise<EventTeam> {
  const res = await fetch(`${API_BASE}/${eventId}/team/members/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ role }),
  })
  return handleResponse<EventTeam>(res)
}

export async function removeTeamMember(
  eventId: number,
  userId: number,
  token: string
): Promise<EventTeam> {
  const res = await fetch(`${API_BASE}/${eventId}/team/members/${userId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return handleResponse<EventTeam>(res)
}
