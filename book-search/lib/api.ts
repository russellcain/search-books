import type { Book } from "./types"

export async function searchBooks(params: {
  q?: string
  rating?: number
  yearStart?: number
  yearEnd?: number
  publisher?: string[]
  author?: string[]
}): Promise<Book[]> {
  const searchParams = new URLSearchParams()

  if (params.q) searchParams.append("q", params.q)
  if (params.rating) searchParams.append("rating", params.rating.toString())
  if (params.yearStart) searchParams.append("yearStart", params.yearStart.toString())
  if (params.yearEnd) searchParams.append("yearEnd", params.yearEnd.toString())
  if (params.publisher) params.publisher.forEach((p) => searchParams.append("publisher", p))
  if (params.author) params.author.forEach((a) => searchParams.append("author", a))

  const response = await fetch(`http://127.0.0.1:5000/search?${searchParams.toString()}`)

  if (!response.ok) {
    throw new Error("Failed to fetch books")
  }

  return response.json() || [];
}

