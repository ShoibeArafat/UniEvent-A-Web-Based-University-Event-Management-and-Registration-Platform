import type { Event, EventCreateInput, EventUpdateInput } from "../types/event"

const API_BASE_URL = "/api/events"

/**
 * Helper to handle HTTP errors and format descriptive messages.
 */
async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMessage = `Request failed with status ${res.status}`
    try {
      const errorData = await res.json()
      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail
      } else if (Array.isArray(errorData.detail)) {
        // Pydantic validation error array
        errorMessage = errorData.detail
          .map((err: { loc?: string[]; msg?: string }) => `${err.loc?.slice(-1)[0] || "Field"}: ${err.msg}`)
          .join(", ")
      } else if (errorData.message) {
        errorMessage = errorData.message
      }
    } catch {
      // Fallback if response body isn't JSON
    }
    throw new Error(errorMessage)
  }
  return res.json() as Promise<T>
}

/**
 * 1. Read List: Fetch all events, optionally filtered by category and search query.
 */
export async function getEvents(params?: { category?: string; search?: string }): Promise<Event[]> {
  const query = new URLSearchParams()
  if (params?.category && params.category !== "All") {
    query.set("category", params.category)
  }
  if (params?.search && params.search.trim()) {
    query.set("search", params.search.trim())
  }

  const url = query.toString() ? `${API_BASE_URL}?${query.toString()}` : API_BASE_URL
  const res = await fetch(url)
  return handleResponse<Event[]>(res)
}

/**
 * 2. Read Single: Fetch a single event by its ID.
 */
export async function getEventById(id: number): Promise<Event> {
  const res = await fetch(`${API_BASE_URL}/${id}`)
  return handleResponse<Event>(res)
}

/**
 * 3. Create: Add a new event record.
 */
export async function createEvent(data: EventCreateInput): Promise<Event> {
  const res = await fetch(API_BASE_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  return handleResponse<Event>(res)
}

/**
 * 4. Update: Edit an existing event record by ID.
 */
export async function updateEvent(id: number, data: EventUpdateInput): Promise<Event> {
  const res = await fetch(`${API_BASE_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  return handleResponse<Event>(res)
}

/**
 * 5. Delete: Delete an event record by ID.
 */
export async function deleteEvent(id: number): Promise<{ message: string; id?: number }> {
  const res = await fetch(`${API_BASE_URL}/${id}`, {
    method: "DELETE",
  })
  return handleResponse<{ message: string; id?: number }>(res)
}
