"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Upload, Download, Filter, Search, AlertCircle, Info, RefreshCw, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ContactDialog } from "@/components/contact-dialog"
import { ContactDetailDialog } from "@/components/contact-detail-dialog"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ThemeToggle } from "@/components/theme-toggle"
import { loadContacts, saveContacts, saveContact, type Contact } from "@/lib/db"
import { supabase } from "@/lib/supabase"

type Contact = {
  id: string
  company: string
  parent: string
  tier: "Tier 1" | "Tier 2" | "Tier 3"
  targetRole: string
  strategicRationale: string
  headOfCorpDev?: string
  headOfAIStrategy?: string
  linkedinProfileSearch?: string
  companyContext?: string
  recommendedOutreachAngle?: string
  coldEmailInitial?: string
  linkedinDMShort?: string
  followUpEmail?: string
  contactName?: string
  email?: string
  linkedin?: string
  channel?: string
  status: "Not Yet Contacted" | "Reached Out" | "Follow-up Sent" | "Replied" | "Passed"
  firstTouchDate?: string
  followUpSent: boolean
  responseType?: "Curious" | "Neutral" | "Pass"
  interestLevel?: "Low" | "Medium" | "High"
  notes?: string
  whatTheyReactedTo?: string
  objections?: string
  suggestedNextStep?: "Demo" | "Check-in" | "None"
  contactCount: number
}

export default function GlazyrCRM() {
  const [contacts, setContacts] = useState<Contact[]>([])
  const [filteredContacts, setFilteredContacts] = useState<Contact[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [tierFilter, setTierFilter] = useState<string>("all")
  const [statusFilter, setStatusFilter] = useState<string>("all")
  const [showContactDialog, setShowContactDialog] = useState(false)
  const [selectedContact, setSelectedContact] = useState<Contact | null>(null)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [syncError, setSyncError] = useState<string | null>(null)
  const [showOnboarding, setShowOnboarding] = useState(true)
  const [isLoading, setIsLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [syncStatus, setSyncStatus] = useState<string>("")

  // Load contacts from Supabase or localStorage
  const fetchContacts = async () => {
    setIsLoading(true)
    setSyncError(null)
    try {
      const data = await loadContacts()
      console.log('Loaded contacts:', data.length)
      
      // Always update state, even if empty
      setContacts(data)
      
      if (data.length > 0) {
        setShowOnboarding(false)
        setSyncStatus(`Synced ${data.length} contacts`)
      } else {
        setShowOnboarding(true)
        setSyncStatus("No contacts found")
      }
    } catch (error) {
      console.error('Error loading contacts:', error)
      setSyncError(`Failed to load: ${error instanceof Error ? error.message : 'Unknown error'}`)
      setSyncStatus("Error loading contacts")
    } finally {
      setIsLoading(false)
      setIsRefreshing(false)
    }
  }

  // Load contacts on mount
  useEffect(() => {
    fetchContacts()
  }, [])

  // Manual refresh function
  const handleRefresh = async () => {
    setIsRefreshing(true)
    await fetchContacts()
  }

  // Clear all contacts
  const handleClearAll = async () => {
    if (window.confirm('Are you sure you want to delete all contacts? This cannot be undone.')) {
      setContacts([])
      await saveContacts([])
      setShowOnboarding(true)
    }
  }

  // Set up real-time subscription to Supabase
  useEffect(() => {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
    const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

    // Only set up real-time if Supabase is configured
    if (supabaseUrl && supabaseKey && typeof window !== 'undefined') {
      const channel = supabase
        .channel('contacts-changes')
        .on(
          'postgres_changes',
          {
            event: '*', // Listen to all changes (INSERT, UPDATE, DELETE)
            schema: 'public',
            table: 'contacts'
          },
          () => {
            // Reload contacts when database changes
            fetchContacts()
          }
        )
        .subscribe()

      return () => {
        supabase.removeChannel(channel)
      }
    }
  }, [])

  // Save to Supabase or localStorage whenever contacts change
  useEffect(() => {
    if (contacts.length > 0 && !isLoading) {
      setIsSaving(true)
      setSyncError(null)
      saveContacts(contacts)
        .then(() => {
          setIsSaving(false)
          setSyncStatus(`Saved ${contacts.length} contacts`)
          console.log('Successfully saved contacts to database')
        })
        .catch((error) => {
          console.error('Error saving contacts:', error)
          setSyncError(`Failed to save: ${error instanceof Error ? error.message : 'Unknown error'}`)
          setIsSaving(false)
        })
    }
  }, [contacts, isLoading])

  // Filter contacts based on search and filters
  useEffect(() => {
    let filtered = contacts

    if (searchTerm) {
      filtered = filtered.filter(
        (c) =>
          c.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.targetRole.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.parent.toLowerCase().includes(searchTerm.toLowerCase()),
      )
    }

    if (tierFilter !== "all") {
      filtered = filtered.filter((c) => c.tier === tierFilter)
    }

    if (statusFilter !== "all") {
      filtered = filtered.filter((c) => c.status === statusFilter)
    }

    setFilteredContacts(filtered)
  }, [contacts, searchTerm, tierFilter, statusFilter])

  // CSV parser that handles quoted fields with commas
  const parseCSVLine = (line: string): string[] => {
    const result: string[] = []
    let current = ""
    let inQuotes = false

    for (let i = 0; i < line.length; i++) {
      const char = line[i]
      const nextChar = line[i + 1]

      if (char === '"') {
        if (inQuotes && nextChar === '"') {
          // Escaped quote
          current += '"'
          i++ // Skip next quote
        } else {
          // Toggle quote state
          inQuotes = !inQuotes
        }
      } else if (char === "," && !inQuotes) {
        // End of field
        result.push(current.trim())
        current = ""
      } else {
        current += char
      }
    }
    // Push last field
    result.push(current.trim())
    return result
  }

  const handleCSVUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setUploadError(null)
    const reader = new FileReader()

    reader.onload = async (e) => {
      try {
        const text = e.target?.result as string
        const lines = text.split("\n").filter((line) => line.trim() && line.trim() !== ",")
        
        if (lines.length < 2) {
          setUploadError("CSV file must contain at least a header row and one data row")
          return
        }

        const headers = parseCSVLine(lines[0]).map((h) => h.trim())

        // Validate required columns
        const requiredColumns = ["Company", "Parent", "Tier", "Target Role", "Strategic Rationale"]
        const missingColumns = requiredColumns.filter((col) => !headers.includes(col))

        if (missingColumns.length > 0) {
          setUploadError(`Missing required columns: ${missingColumns.join(", ")}`)
          return
        }

        const newContacts: Contact[] = lines.slice(1)
          .filter((line) => line.trim() && !line.trim().match(/^,+$/)) // Filter out empty rows
          .map((line, index) => {
            const values = parseCSVLine(line)
            const row: Record<string, string> = {}
            headers.forEach((header, i) => {
              row[header] = values[i] || ""
            })

            return {
              id: `contact-${Date.now()}-${index}`,
              company: row["Company"] || "",
              parent: row["Parent"] || "",
              tier: (row["Tier"] as Contact["tier"]) || "Tier 2",
              targetRole: row["Target Role"] || "",
              strategicRationale: row["Strategic Rationale"] || "",
              headOfCorpDev: row["Head of Corp Dev / M&A"] || "",
              headOfAIStrategy: row["Head of AI Strategy / AI Platform"] || "",
              linkedinProfileSearch: row["LinkedIn Profile Search"] || "",
              companyContext: row["Company Context"] || "",
              recommendedOutreachAngle: row["Recommended Outreach Angle"] || "",
              coldEmailInitial: row["Cold Email (Initial)"] || "",
              linkedinDMShort: row["LinkedIn DM (Short)"] || "",
              followUpEmail: row["Follow-Up Email (Day 5–10)"] || "",
              contactName: row["Contact Name"] || "",
              email: row["Email"] || "",
              linkedin: row["LinkedIn"] || "",
              channel: row["Channel"] || "",
              status: "Not Yet Contacted",
              followUpSent: false,
              contactCount: 0,
            }
          })
          .filter((contact) => contact.company) // Filter out contacts without company name

        if (newContacts.length === 0) {
          setUploadError("No valid contacts found in CSV file")
          return
        }

        // Replace all contacts with new CSV data (don't append)
        setContacts(newContacts)
        await saveContacts(newContacts)
        setShowOnboarding(false)
        event.target.value = "" // Reset input
      } catch (error) {
        setUploadError(`Error parsing CSV file: ${error instanceof Error ? error.message : "Unknown error"}`)
      }
    }

    reader.readAsText(file)
  }

  const handleExportCSV = () => {
    const headers = [
      "Company",
      "Parent",
      "Tier",
      "Target Role",
      "Strategic Rationale",
      "Contact Name",
      "Email",
      "Status",
      "First Touch Date",
      "Response Type",
      "Interest Level",
      "Notes",
    ]

    const csvContent = [
      headers.join(","),
      ...filteredContacts.map((c) =>
        [
          c.company,
          c.parent,
          c.tier,
          c.targetRole,
          c.strategicRationale,
          c.contactName || "",
          c.email || "",
          c.status,
          c.firstTouchDate || "",
          c.responseType || "",
          c.interestLevel || "",
          c.notes?.replace(/,/g, ";") || "",
        ].join(","),
      ),
    ].join("\n")

    const blob = new Blob([csvContent], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `glazyr-export-${new Date().toISOString().split("T")[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleUpdateContact = async (updatedContact: Contact) => {
    const updatedContacts = contacts.map((c) => (c.id === updatedContact.id ? updatedContact : c))
    setContacts(updatedContacts)
    await saveContact(updatedContact)
    setSelectedContact(null)
  }

  const getTierColor = (tier: string) => {
    switch (tier) {
      case "Tier 1":
        return "bg-blue-500 text-white"
      case "Tier 2":
        return "bg-cyan-500 text-white"
      case "Tier 3":
        return "bg-slate-500 text-white"
      default:
        return "bg-muted text-muted-foreground"
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Not Yet Contacted":
        return "bg-muted text-muted-foreground"
      case "Reached Out":
        return "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200"
      case "Follow-up Sent":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200"
      case "Replied":
        return "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200"
      case "Passed":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
      default:
        return "bg-muted text-muted-foreground"
    }
  }

  const isOverdue = (contact: Contact) => {
    if (!contact.firstTouchDate || contact.status !== "Reached Out") return false
    const daysSince = Math.floor((Date.now() - new Date(contact.firstTouchDate).getTime()) / (1000 * 60 * 60 * 24))
    return daysSince > 7
  }

  const stats = {
    total: contacts.length,
    tier1: contacts.filter((c) => c.tier === "Tier 1").length,
    tier2: contacts.filter((c) => c.tier === "Tier 2").length,
    tier3: contacts.filter((c) => c.tier === "Tier 3").length,
    replied: contacts.filter((c) => c.status === "Replied").length,
    responseRate:
      contacts.filter((c) => c.status !== "Not Yet Contacted").length > 0
        ? (
            (contacts.filter((c) => c.status === "Replied").length /
              contacts.filter((c) => c.status !== "Not Yet Contacted").length) *
            100
          ).toFixed(1)
        : "0.0",
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="mx-auto max-w-screen-xl px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img src="/glazyr-logo.png" alt="Glazyr" className="h-10 w-10" />
              <div>
                <h1 className="text-2xl font-bold text-foreground">Glazyr CRM-Lite</h1>
                <p className="text-sm text-muted-foreground">Strategic Outreach Management</p>
              </div>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <ThemeToggle />
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleRefresh} 
                disabled={isRefreshing || isLoading}
                title="Refresh data from server"
              >
                <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''} sm:mr-2`} />
                <span className="hidden sm:inline">{isRefreshing ? 'Syncing...' : 'Refresh'}</span>
              </Button>
              {isSaving && (
                <Badge variant="secondary" className="text-xs">
                  Saving...
                </Badge>
              )}
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleClearAll} 
                disabled={contacts.length === 0 || isLoading}
                title={contacts.length === 0 ? "No contacts to clear" : "Clear all contacts"}
                className="text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-950"
              >
                <Trash2 className="h-4 w-4 sm:mr-2" />
                <span className="hidden sm:inline">Clear All</span>
              </Button>
              {/* Force deployment update */}
              <Button variant="outline" size="sm" onClick={handleExportCSV} disabled={contacts.length === 0}>
                <Download className="h-4 w-4 sm:mr-2" />
                <span className="hidden sm:inline">Export</span>
              </Button>
              <label htmlFor="csv-upload">
                <Button variant="default" size="sm" asChild>
                  <span>
                    <Upload className="h-4 w-4 sm:mr-2" />
                    <span className="hidden sm:inline">Import CSV</span>
                    <span className="sm:hidden">Import</span>
                  </span>
                </Button>
                <input id="csv-upload" type="file" accept=".csv" className="hidden" onChange={handleCSVUpload} />
              </label>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-screen-xl px-6 py-8">
        {/* Loading State */}
        {isLoading && (
          <Card className="p-8 mb-8 text-center">
            <p className="text-muted-foreground">Loading contacts...</p>
          </Card>
        )}

        {/* Onboarding */}
        {!isLoading && showOnboarding && contacts.length === 0 && (
          <Card className="p-8 mb-8 bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
            <div className="flex items-start gap-4">
              <Info className="h-6 w-6 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-1" />
              <div>
                <h2 className="text-xl font-semibold text-blue-900 dark:text-blue-100 mb-2">
                  Welcome to Glazyr CRM-Lite
                </h2>
                <p className="text-blue-800 dark:text-blue-200 mb-4 leading-relaxed">
                  Get started by importing your CSV file with buyer contacts. Your CSV should include: Company, Parent,
                  Tier, Target Role, and Strategic Rationale.
                </p>
                <div className="space-y-2 text-sm text-blue-700 dark:text-blue-300">
                  <p>
                    <strong>Tier 1:</strong> High strategic value - Start here
                  </p>
                  <p>
                    <strong>Tier 2:</strong> Strong fit but less critical
                  </p>
                  <p>
                    <strong>Tier 3:</strong> Exploratory or lower priority
                  </p>
                </div>
              </div>
            </div>
          </Card>
        )}

        {/* Error Alert */}
        {uploadError && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{uploadError}</AlertDescription>
          </Alert>
        )}
        {syncError && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{syncError}</AlertDescription>
          </Alert>
        )}
        {syncStatus && !syncError && !isLoading && (
          <Alert className="mb-6 bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
            <Info className="h-4 w-4 text-blue-600 dark:text-blue-400" />
            <AlertDescription className="text-blue-800 dark:text-blue-200">
              {syncStatus}
            </AlertDescription>
          </Alert>
        )}

        {/* Stats */}
        {!isLoading && contacts.length > 0 && (
          <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
            <Card className="p-4">
              <p className="text-sm text-muted-foreground mb-1">Total</p>
              <p className="text-3xl font-bold text-foreground">{stats.total}</p>
            </Card>
            <Card className="p-4">
              <p className="text-sm text-muted-foreground mb-1">Tier 1</p>
              <p className="text-3xl font-bold text-blue-600">{stats.tier1}</p>
            </Card>
            <Card className="p-4">
              <p className="text-sm text-muted-foreground mb-1">Tier 2</p>
              <p className="text-3xl font-bold text-cyan-600">{stats.tier2}</p>
            </Card>
            <Card className="p-4">
              <p className="text-sm text-muted-foreground mb-1">Tier 3</p>
              <p className="text-3xl font-bold text-slate-600">{stats.tier3}</p>
            </Card>
            <Card className="p-4">
              <p className="text-sm text-muted-foreground mb-1">Replied</p>
              <p className="text-3xl font-bold text-emerald-600">{stats.replied}</p>
            </Card>
            <Card className="p-4">
              <p className="text-sm text-muted-foreground mb-1">Response Rate</p>
              <p className="text-3xl font-bold text-foreground">{stats.responseRate}%</p>
            </Card>
          </div>
        )}

        {/* Filters */}
        {!isLoading && contacts.length > 0 && (
          <Card className="p-6 mb-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search companies, roles, or parent..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              <div className="flex gap-3">
                <Select value={tierFilter} onValueChange={setTierFilter}>
                  <SelectTrigger className="w-[140px]">
                    <Filter className="h-4 w-4 mr-2" />
                    <SelectValue placeholder="All Tiers" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Tiers</SelectItem>
                    <SelectItem value="Tier 1">Tier 1</SelectItem>
                    <SelectItem value="Tier 2">Tier 2</SelectItem>
                    <SelectItem value="Tier 3">Tier 3</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="All Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="Not Yet Contacted">Not Yet Contacted</SelectItem>
                    <SelectItem value="Reached Out">Reached Out</SelectItem>
                    <SelectItem value="Follow-up Sent">Follow-up Sent</SelectItem>
                    <SelectItem value="Replied">Replied</SelectItem>
                    <SelectItem value="Passed">Passed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </Card>
        )}

        {/* Contact List */}
        {!isLoading && contacts.length > 0 && (
          <Card>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b border-border bg-muted/50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Company</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger className="flex items-center gap-1">
                            Tier
                            <Info className="h-3 w-3" />
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Tier 1 = Highest priority strategic value</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Target Role</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Status</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger className="flex items-center gap-1">
                            Contacts
                            <Info className="h-3 w-3" />
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Max 2 contacts per company (training wheels)</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredContacts.map((contact) => (
                    <tr
                      key={contact.id}
                      className={`border-b border-border hover:bg-muted/50 transition-colors ${
                        isOverdue(contact) ? "bg-red-50 dark:bg-red-950/20" : ""
                      }`}
                    >
                      <td className="px-6 py-4">
                        <div>
                          <p className="font-medium text-foreground">{contact.company}</p>
                          <p className="text-sm text-muted-foreground">{contact.parent}</p>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <Badge className={getTierColor(contact.tier)}>{contact.tier}</Badge>
                      </td>
                      <td className="px-6 py-4 text-sm text-foreground">{contact.targetRole}</td>
                      <td className="px-6 py-4">
                        <Badge variant="secondary" className={getStatusColor(contact.status)}>
                          {contact.status}
                        </Badge>
                        {isOverdue(contact) && (
                          <p className="text-xs text-red-600 dark:text-red-400 mt-1">Overdue follow-up</p>
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-sm text-foreground">{contact.contactCount} / 2</span>
                      </td>
                      <td className="px-6 py-4">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setSelectedContact(contact)}
                          className="text-blue-600 dark:text-blue-400"
                        >
                          View Details
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}

        {/* Empty State */}
        {!isLoading && contacts.length > 0 && filteredContacts.length === 0 && (
          <Card className="p-12 text-center">
            <p className="text-muted-foreground">No contacts match your filters</p>
          </Card>
        )}
      </main>

      {/* Contact Dialog */}
      {showContactDialog && (
        <ContactDialog
          onClose={() => setShowContactDialog(false)}
          onSave={async (contact) => {
            const updatedContacts = [...contacts, contact]
            setContacts(updatedContacts)
            await saveContact(contact)
            setShowContactDialog(false)
          }}
        />
      )}

      {/* Contact Detail Dialog */}
      {selectedContact && (
        <ContactDetailDialog
          contact={selectedContact}
          onClose={() => setSelectedContact(null)}
          onSave={handleUpdateContact}
        />
      )}
    </div>
  )
}
