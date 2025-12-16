"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Loader2,
  Send,
  Play,
  CheckCircle,
  TrendingUp,
  Clock,
  DollarSign,
  ArrowRight,
  Mic,
  Paperclip,
  X,
} from "lucide-react"

interface RouteDecision {
  routingDecisionId: string
  primaryServer: {
    id: string
    name: string
    confidence: number
    reasoning: string
  }
  executionPlan: {
    steps: Array<{
      serverId: string
      serverName: string
      toolName: string
      order: number
    }>
  }
}

interface ExecutionResult {
  content: Array<{ text: string }>
  executionResult: {
    totalLatency: number
    totalCost: number
    executedServers: Array<{
      serverId: string
      serverName: string
      latency: number
      cost: number
    }>
  }
}

export function QueryOrchestration() {
  const [query, setQuery] = useState("")
  const [isRouting, setIsRouting] = useState(false)
  const [isExecuting, setIsExecuting] = useState(false)
  const [routeDecision, setRouteDecision] = useState<RouteDecision | null>(null)
  const [executionResult, setExecutionResult] = useState<ExecutionResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isRecording, setIsRecording] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)

  const handleRoute = async () => {
    if (!query.trim()) return

    setIsRouting(true)
    setError(null)
    setRouteDecision(null)
    setExecutionResult(null)

    try {
      const response = await fetch("/api/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      })

      if (!response.ok) throw new Error("Failed to route query")

      const data = await response.json()
      setRouteDecision(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred while routing")
    } finally {
      setIsRouting(false)
    }
  }

  const handleExecute = async () => {
    if (!routeDecision) return

    setIsExecuting(true)
    setError(null)

    try {
      const response = await fetch("/api/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          routingDecisionId: routeDecision.routingDecisionId,
        }),
      })

      if (!response.ok) throw new Error("Failed to execute query")

      const data = await response.json()
      setExecutionResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred during execution")
    } finally {
      setIsExecuting(false)
    }
  }

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      const audioChunks: BlobPart[] = []

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data)
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" })
        const formData = new FormData()
        formData.append("file", audioBlob, "recording.webm")

        try {
          const response = await fetch("/api/transcribe", {
            method: "POST",
            body: formData,
          })

          if (!response.ok) throw new Error("Failed to transcribe audio")

          const { text } = await response.json()
          setQuery((prev) => (prev ? `${prev} ${text}` : text))
        } catch (err) {
          setError("Failed to transcribe audio")
        }

        stream.getTracks().forEach((track) => track.stop())
      }

      mediaRecorder.start()
      mediaRecorderRef.current = mediaRecorder
      setIsRecording(true)
    } catch (err) {
      setError("Failed to access microphone")
    }
  }

  const handleStopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    setUploadedFiles((prev) => [...prev, ...files])
  }

  const handleRemoveFile = (index: number) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-6">
      {/* Query Input */}
      <Card className="rounded-2xl border-border/50">
        <CardHeader>
          <CardTitle>Submit Query</CardTitle>
          <CardDescription>Enter your natural language query to route to the appropriate agent</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {uploadedFiles.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {uploadedFiles.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center gap-2 rounded-full border border-border/50 bg-muted/50 px-3 py-1.5 text-sm"
                >
                  <Paperclip className="h-3 w-3 text-muted-foreground" />
                  <span className="text-foreground">{file.name}</span>
                  <button
                    onClick={() => handleRemoveFile(index)}
                    className="text-muted-foreground hover:text-foreground"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </div>
              ))}
            </div>
          )}

          <div className="relative">
            <Textarea
              placeholder="e.g., What's the weather in San Francisco?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              rows={4}
              className="resize-none rounded-2xl border-border/50 pr-24 focus-visible:border-primary/50 focus-visible:ring-1 focus-visible:ring-primary/20"
            />

            <div className="absolute bottom-3 right-3 flex items-center gap-1.5">
              <input ref={fileInputRef} type="file" multiple onChange={handleFileUpload} className="hidden" />

              <Button
                variant="ghost"
                size="icon"
                onClick={() => fileInputRef.current?.click()}
                className="h-8 w-8 rounded-full hover:bg-primary/10"
                type="button"
              >
                <Paperclip className="h-4 w-4 text-muted-foreground" />
              </Button>

              <Button
                variant="ghost"
                size="icon"
                onClick={isRecording ? handleStopRecording : handleStartRecording}
                className={`h-8 w-8 rounded-full ${
                  isRecording ? "bg-destructive/10 hover:bg-destructive/20" : "hover:bg-primary/10"
                }`}
                type="button"
              >
                <Mic
                  className={`h-4 w-4 ${isRecording ? "text-destructive animate-pulse" : "text-muted-foreground"}`}
                />
              </Button>

              <Button
                onClick={handleRoute}
                disabled={!query.trim() || isRouting}
                size="icon"
                className="h-8 w-8 rounded-full"
              >
                {isRouting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Routing Decision */}
      {routeDecision && (
        <Card className="rounded-2xl border-primary/20 bg-primary/5">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-primary" />
                  Routing Decision
                </CardTitle>
                <CardDescription className="mt-1">Agent selected with confidence analysis</CardDescription>
              </div>
              <Badge variant="secondary" className="rounded-full text-sm">
                {Math.round(routeDecision.primaryServer.confidence * 100)}% Confidence
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Primary Server */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-primary">
                  <TrendingUp className="h-4 w-4 text-primary-foreground" />
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Primary Agent</p>
                  <p className="text-lg font-semibold text-foreground">{routeDecision.primaryServer.name}</p>
                </div>
              </div>
              <div className="rounded-2xl border border-border/50 bg-muted/50 p-4">
                <p className="text-sm font-medium text-foreground mb-2">Reasoning</p>
                <p className="text-sm text-muted-foreground leading-relaxed">{routeDecision.primaryServer.reasoning}</p>
              </div>
            </div>

            {/* Execution Plan */}
            <div className="space-y-3">
              <p className="text-sm font-medium text-foreground">Execution Plan</p>
              <div className="space-y-2">
                {routeDecision.executionPlan.steps.map((step, index) => (
                  <div key={index} className="flex items-center gap-3 rounded-2xl border border-border/50 bg-card p-3">
                    <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                      {step.order}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-foreground">{step.serverName}</p>
                      <p className="text-xs text-muted-foreground">{step.toolName}</p>
                    </div>
                    {index < routeDecision.executionPlan.steps.length - 1 && (
                      <ArrowRight className="h-4 w-4 text-muted-foreground" />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Execute Button */}
            {!executionResult && (
              <Button onClick={handleExecute} disabled={isExecuting} className="w-full gap-2 rounded-full" size="lg">
                {isExecuting ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Executing...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    Execute Query
                  </>
                )}
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      {/* Execution Result */}
      {executionResult && (
        <Card className="rounded-2xl border-chart-1/20 bg-chart-1/5">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-chart-1" />
              Execution Complete
            </CardTitle>
            <CardDescription>Final result and performance metrics</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Result */}
            <div className="rounded-2xl border border-border/50 bg-card p-4">
              <p className="text-sm font-medium text-foreground mb-3">Response</p>
              <p className="text-sm text-foreground leading-relaxed">{executionResult.content[0]?.text}</p>
            </div>

            {/* Metrics */}
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="flex items-center gap-3 rounded-2xl border border-border/50 bg-card p-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-chart-2/10">
                  <Clock className="h-5 w-5 text-chart-2" />
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Latency</p>
                  <p className="text-lg font-semibold text-foreground">
                    {executionResult.executionResult.totalLatency}ms
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 rounded-2xl border border-border/50 bg-card p-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-chart-4/10">
                  <DollarSign className="h-5 w-5 text-chart-4" />
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Cost</p>
                  <p className="text-lg font-semibold text-foreground">
                    ${executionResult.executionResult.totalCost.toFixed(4)}
                  </p>
                </div>
              </div>
            </div>

            {/* Server Breakdown */}
            <div className="space-y-3">
              <p className="text-sm font-medium text-foreground">Server Execution Details</p>
              <div className="space-y-2">
                {executionResult.executionResult.executedServers.map((server, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between rounded-2xl border border-border/50 bg-card p-3"
                  >
                    <div>
                      <p className="text-sm font-medium text-foreground">{server.serverName}</p>
                      <p className="text-xs text-muted-foreground">{server.serverId}</p>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <p className="text-xs text-muted-foreground">Latency</p>
                        <p className="text-sm font-medium text-foreground">{server.latency}ms</p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-muted-foreground">Cost</p>
                        <p className="text-sm font-medium text-foreground">${server.cost.toFixed(4)}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
