"use client"

import { useState } from "react"
import { QueryOrchestration } from "@/components/query-orchestration"
import { ServerManagement } from "@/components/server-management"
import { Button } from "@/components/ui/button"
import { Network, Server, Moon, Sun } from "lucide-react"

export default function Home() {
  const [activeView, setActiveView] = useState<"query" | "servers">("query")
  const [isDarkMode, setIsDarkMode] = useState(true)

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
    document.documentElement.classList.toggle("dark")
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary">
                <Network className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-foreground">Agent Orchestrator</h1>
                <p className="text-sm text-muted-foreground">Intelligent Multi-Agent System</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant={activeView === "query" ? "default" : "ghost"}
                size="sm"
                onClick={() => setActiveView("query")}
                className="gap-2 rounded-full"
              >
                <Network className="h-4 w-4" />
                Query
              </Button>
              <Button
                variant={activeView === "servers" ? "default" : "ghost"}
                size="sm"
                onClick={() => setActiveView("servers")}
                className="gap-2 rounded-full"
              >
                <Server className="h-4 w-4" />
                Servers
              </Button>
              <div className="ml-2 h-6 w-px bg-border/50" />
              <Button variant="ghost" size="icon" onClick={toggleDarkMode} className="h-9 w-9 rounded-full">
                {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {activeView === "query" ? <QueryOrchestration /> : <ServerManagement />}
      </main>
    </div>
  )
}
