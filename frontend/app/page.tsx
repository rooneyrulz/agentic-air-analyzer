"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Search, Sparkles, Microscope, HelpCircle, Loader } from "lucide-react"
import { useState } from "react"

const exampleQueries = [
  "How does the temperature in Room A change by hour of the day?",
  "How does CO2 vary by day of the week?",
  "Which room had the highest temperature reading last week?",
  "Which room had the biggest variation in CO2 levels?",
  "List the rooms in order of hottest to coolest using average temperature",
  "What is the average temperature of each room in mornings and evenings?"
]

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("")
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = () => {
    // TODO: Replace with actual search logic
    setIsSearching(true);
    setTimeout(() => {
      console.log("Searching for:", searchQuery)
      setIsSearching(false);
    }, 1000)
  }

  return (
    <div className="flex flex-col bg-accent h-screen overflow-y-auto">
      <header className="w-full border-b bg-background/80 backdrop-blur-sm shadow-md mb-12">
        <div className="container mx-auto flex items-center gap-4 py-6 px-4">
          <span className="rounded-full bg-primary/10 p-2">
            <Sparkles className="size-8 text-primary" />
          </span>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Agentic Air Analyzer</h1>
            <p className="text-muted-foreground text-sm">Gain insights into rooms air quality with a single click.</p>
          </div>
        </div>
      </header>
      <main className="flex flex-col gap-6 container mx-auto">
        <Card className="w-full">
          <CardContent className="p-6">
            <div className="flex gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-6 w-6 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Enter location or room name..."
                  className="pl-12 py-4 text-base h-14"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <Button
                size="lg"
                disabled={!searchQuery || isSearching}
                onClick={handleSearch}
                className="h-14 px-8 text-base cursor-pointer"
              >
                {isSearching ? (
                  <Loader className="mr-2 animate-spin" />
                ) : (
                  <Microscope className="mr-2" />
                )}
                Analyze Air
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="w-full">
          <CardHeader className="pb-3">
            <CardTitle className="text-xl font-medium flex items-center gap-2">
              <HelpCircle className="h-5 w-5" />
              Example queries
            </CardTitle>
          </CardHeader>
          <CardContent className="grid gap-2">
            {exampleQueries.map((query, index) => (
              <button
                key={index}
                onClick={() => setSearchQuery(query)}
                className="text-left px-4 py-4 h-14 text-base rounded-md hover:bg-muted transition-colors duration-200 text-muted-foreground hover:text-foreground w-full flex items-center cursor-pointer"
              >
                {query}
              </button>
            ))}
          </CardContent>
        </Card>
      </main>
    </div>
  )
}