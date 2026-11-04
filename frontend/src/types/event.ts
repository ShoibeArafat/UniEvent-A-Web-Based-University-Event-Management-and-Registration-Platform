export interface Event {
  id: number
  title: string
  description: string
  location: string
  event_date: string
  organizer: string
  category: string
  capacity: number
  status: string
  created_at?: string
  updated_at?: string
}

export interface EventCreateInput {
  title: string
  description: string
  location: string
  event_date: string
  organizer: string
  category: string
  capacity: number
  status: string
}

export type EventUpdateInput = Partial<EventCreateInput>

export type EventCategory =
  | "Technology"
  | "Competition"
  | "Workshop"
  | "Cultural"
  | "Seminar"
  | "Sports"
  | "Other"

export type EventStatus = "Upcoming" | "Ongoing" | "Completed" | "Cancelled"
