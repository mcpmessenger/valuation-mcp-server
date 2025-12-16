"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Loader2, Plus, Server, CheckCircle, XCircle, Wrench } from "lucide-react"

interface MCPServer {
  id: string
  name: string
  url: string
  description: string
  isHealthy: boolean
  metadata?: {
    category?: string
    costPerCall?: number
  }
  tools: Array<{
    name: string
    description: string
  }>
}

export function ServerManagement() {
  const [servers, setServers] = useState<MCPServer[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isRegistering, setIsRegistering] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [dialogOpen, setDialogOpen] = useState(false)

  const [formData, setFormData] = useState({
    id: "",
    name: "",
    url: "",
    description: "",
    category: "",
    costPerCall: "",
  })

  useEffect(() => {
    fetchServers()
  }, [])

  const fetchServers = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch("/api/servers")
      if (!response.ok) throw new Error("Failed to fetch servers")

      const data = await response.json()
      setServers(data.servers || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred while fetching servers")
    } finally {
      setIsLoading(false)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsRegistering(true)
    setError(null)

    try {
      const payload: any = {
        id: formData.id,
        name: formData.name,
        url: formData.url,
        description: formData.description,
      }

      if (formData.category) payload.category = formData.category
      if (formData.costPerCall) payload.costPerCall = Number.parseFloat(formData.costPerCall)

      const response = await fetch("/api/admin/register-server", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (!response.ok) throw new Error("Failed to register server")

      await fetchServers()
      setDialogOpen(false)
      setFormData({ id: "", name: "", url: "", description: "", category: "", costPerCall: "" })
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred while registering the server")
    } finally {
      setIsRegistering(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-foreground">MCP Servers</h2>
          <p className="text-sm text-muted-foreground mt-1">Manage and monitor registered agent servers</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button className="gap-2">
              <Plus className="h-4 w-4" />
              Register Server
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>Register New Server</DialogTitle>
              <DialogDescription>Add a new MCP server to the orchestration system</DialogDescription>
            </DialogHeader>
            <form onSubmit={handleRegister} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="id">Server ID *</Label>
                <Input
                  id="id"
                  value={formData.id}
                  onChange={(e) => setFormData({ ...formData, id: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="name">Name *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="url">URL *</Label>
                <Input
                  id="url"
                  type="url"
                  value={formData.url}
                  onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="description">Description *</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={3}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="category">Category</Label>
                <Input
                  id="category"
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  placeholder="e.g., Weather, Finance"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="costPerCall">Cost Per Call</Label>
                <Input
                  id="costPerCall"
                  type="number"
                  step="0.0001"
                  value={formData.costPerCall}
                  onChange={(e) => setFormData({ ...formData, costPerCall: e.target.value })}
                  placeholder="0.001"
                />
              </div>
              <Button type="submit" disabled={isRegistering} className="w-full gap-2">
                {isRegistering ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Registering...
                  </>
                ) : (
                  "Register Server"
                )}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Servers Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {servers.map((server) => (
          <Card key={server.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                    <Server className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <CardTitle className="text-base">{server.name}</CardTitle>
                    {server.metadata?.category && (
                      <Badge variant="secondary" className="mt-1 text-xs">
                        {server.metadata.category}
                      </Badge>
                    )}
                  </div>
                </div>
                {server.isHealthy ? (
                  <CheckCircle className="h-5 w-5 text-chart-1" />
                ) : (
                  <XCircle className="h-5 w-5 text-destructive" />
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm text-muted-foreground leading-relaxed">{server.description}</p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Status</span>
                  <Badge variant={server.isHealthy ? "default" : "destructive"}>
                    {server.isHealthy ? "Healthy" : "Unhealthy"}
                  </Badge>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Tools</span>
                  <div className="flex items-center gap-1">
                    <Wrench className="h-3 w-3 text-muted-foreground" />
                    <span className="font-medium text-foreground">{server.tools.length}</span>
                  </div>
                </div>
                {server.metadata?.costPerCall !== undefined && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Cost/Call</span>
                    <span className="font-medium text-foreground">${server.metadata.costPerCall.toFixed(4)}</span>
                  </div>
                )}
              </div>
              <div className="pt-2 border-t border-border">
                <p className="text-xs text-muted-foreground break-all">{server.url}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {servers.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Server className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-lg font-medium text-foreground mb-2">No servers registered</p>
            <p className="text-sm text-muted-foreground mb-4">Get started by registering your first MCP server</p>
            <Button onClick={() => setDialogOpen(true)} className="gap-2">
              <Plus className="h-4 w-4" />
              Register Server
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
