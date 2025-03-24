"use client"

import { useState, useEffect } from "react"
import { BookIcon, Search, Star } from "lucide-react"
import { Slider } from "@/components/ui/slider"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import Image from "next/image"
import { searchBooks } from "@/lib/api"
import type { Book } from "@/lib/types"

export default function BookSearchResults() {
  const [searchTerm, setSearchTerm] = useState("")
  const [yearRange, setYearRange] = useState([1900, 2023])
  const [ratingFilter, setRatingFilter] = useState(0)
  const [publisherFilters, setPublisherFilters] = useState<string[]>([])
  const [authorFilters, setAuthorFilters] = useState<string[]>([])
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(false)

  const uniquePublishers = Array.from(new Set(books.map((book) => book.publisher)))
  const uniqueAuthors = Array.from(new Set(books.flatMap((book) => book.authors)))
  useEffect(() => {
    fetchBooks()
  }, [searchTerm, yearRange, ratingFilter, publisherFilters, authorFilters])

  const fetchBooks = async () => {
    setLoading(true)
    try {
      const results = await searchBooks({
        q: searchTerm,
        rating: ratingFilter,
        yearStart: yearRange[0],
        yearEnd: yearRange[1],
        publisher: publisherFilters,
        author: authorFilters,
      })
      console.log("BOOK RESULTS", results)
      setBooks(results)
    } catch (error) {
      console.error("Failed to fetch books:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex gap-4">
        {/* Sidebar with filters */}
        <div className="w-1/4 space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-2">Publication Year</h3>
            <Slider min={1900} max={2023} step={1} value={yearRange} onValueChange={setYearRange} className="w-full" />
            <div className="flex justify-between mt-2 text-sm text-gray-600">
              <span>{yearRange[0]}</span>
              <span>{yearRange[1]}</span>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2">Minimum Rating</h3>
            <div className="flex items-center">
              {[1, 2, 3, 4, 5].map((star) => (
                <Star
                  key={star}
                  className={`w-6 h-6 cursor-pointer ${
                    star <= ratingFilter ? "text-yellow-400 fill-current" : "text-gray-300"
                  }`}
                  onClick={() => setRatingFilter(star)}
                />
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2">Publishers</h3>
            {uniquePublishers.map((publisher) => (
              <div key={publisher} className="flex items-center space-x-2">
                <Checkbox
                  id={`publisher-${publisher}`}
                  checked={publisherFilters.includes(publisher)}
                  onCheckedChange={(checked) => {
                    setPublisherFilters(
                      checked ? [...publisherFilters, publisher] : publisherFilters.filter((p) => p !== publisher),
                    )
                  }}
                />
                <label
                  htmlFor={`publisher-${publisher}`}
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  {publisher}
                </label>
              </div>
            ))}
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2">Authors</h3>
            {uniqueAuthors.map((author) => (
              <div key={author} className="flex items-center space-x-2">
                <Checkbox
                  id={`author-${author}`}
                  checked={authorFilters.includes(author)}
                  onCheckedChange={(checked) => {
                    setAuthorFilters(checked ? [...authorFilters, author] : authorFilters.filter((a) => a !== author))
                  }}
                />
                <label
                  htmlFor={`author-${author}`}
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  {author}
                </label>
              </div>
            ))}
          
          </div>
        </div>

        {/* Main content area */}
        <div className="w-3/4">
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search books..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
          </div>

          {loading ? (
            <div className="text-center">Loading...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {books.map((book) => (
                <Card key={book.id} className="flex flex-col">
                  <CardHeader>
                    <CardTitle>{book.title}</CardTitle>
                    <CardDescription>{book.authors.join(',')}</CardDescription>
                  </CardHeader>
                  <CardContent className="flex-grow">
                    <Image
                      src={book.coverArt || "/placeholder.svg"}
                      alt={`Cover of ${book.title}`}
                      width={200}
                      height={300}
                      className="w-full h-48 object-cover mb-4"
                    />
                    <p className="text-sm text-gray-600">{book.description}</p>
                  </CardContent>
                  <CardFooter className="flex justify-between">
                    <div className="flex items-center">
                      <BookIcon className="w-4 h-4 mr-1" />
                      <span className="text-sm">{book.publisher}</span>
                    </div>
                    <div className="flex items-center">
                      <Star className="w-4 h-4 mr-1 text-yellow-400 fill-current" />
                      <span className="text-sm">{book.rating.toFixed(1)}</span>
                    </div>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

