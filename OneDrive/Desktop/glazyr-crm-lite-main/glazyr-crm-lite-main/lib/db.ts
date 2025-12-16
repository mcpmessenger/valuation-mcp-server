import { supabase } from './supabase'

export type Contact = {
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
  created_at?: string
  updated_at?: string
}

// Check if Supabase is configured
const isSupabaseConfigured = () => {
  if (typeof window === 'undefined') return false // Server-side check
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
  const configured = !!(url && key && url !== '' && key !== '')
  
  if (!configured) {
    console.warn('Supabase not configured. URL:', url ? 'set' : 'missing', 'Key:', key ? 'set' : 'missing')
  }
  
  return configured
}

// Convert database row (snake_case) to Contact (camelCase)
const dbRowToContact = (row: any): Contact => ({
  id: row.id,
  company: row.company,
  parent: row.parent,
  tier: row.tier,
  targetRole: row.target_role,
  strategicRationale: row.strategic_rationale,
  headOfCorpDev: row.head_of_corp_dev,
  headOfAIStrategy: row.head_of_ai_strategy,
  linkedinProfileSearch: row.linkedin_profile_search,
  companyContext: row.company_context,
  recommendedOutreachAngle: row.recommended_outreach_angle,
  coldEmailInitial: row.cold_email_initial,
  linkedinDMShort: row.linkedin_dm_short,
  followUpEmail: row.follow_up_email,
  contactName: row.contact_name,
  email: row.email,
  linkedin: row.linkedin,
  channel: row.channel,
  status: row.status,
  firstTouchDate: row.first_touch_date,
  followUpSent: row.follow_up_sent || false,
  responseType: row.response_type,
  interestLevel: row.interest_level,
  notes: row.notes,
  whatTheyReactedTo: row.what_they_reacted_to,
  objections: row.objections,
  suggestedNextStep: row.suggested_next_step,
  contactCount: row.contact_count || 0,
  created_at: row.created_at,
  updated_at: row.updated_at,
})

// Convert Contact (camelCase) to database row (snake_case)
const contactToDbRow = (contact: Contact): any => ({
  id: contact.id,
  company: contact.company,
  parent: contact.parent,
  tier: contact.tier,
  target_role: contact.targetRole,
  strategic_rationale: contact.strategicRationale,
  head_of_corp_dev: contact.headOfCorpDev || null,
  head_of_ai_strategy: contact.headOfAIStrategy || null,
  linkedin_profile_search: contact.linkedinProfileSearch || null,
  company_context: contact.companyContext || null,
  recommended_outreach_angle: contact.recommendedOutreachAngle || null,
  cold_email_initial: contact.coldEmailInitial || null,
  linkedin_dm_short: contact.linkedinDMShort || null,
  follow_up_email: contact.followUpEmail || null,
  contact_name: contact.contactName || null,
  email: contact.email || null,
  linkedin: contact.linkedin || null,
  channel: contact.channel || null,
  status: contact.status,
  first_touch_date: contact.firstTouchDate || null,
  follow_up_sent: contact.followUpSent || false,
  response_type: contact.responseType || null,
  interest_level: contact.interestLevel || null,
  notes: contact.notes || null,
  what_they_reacted_to: contact.whatTheyReactedTo || null,
  objections: contact.objections || null,
  suggested_next_step: contact.suggestedNextStep || null,
  contact_count: contact.contactCount || 0,
})

// Load contacts from Supabase or localStorage fallback
export const loadContacts = async (): Promise<Contact[]> => {
  if (isSupabaseConfigured()) {
    try {
      const { data, error } = await supabase
        .from('contacts')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) {
        console.error('Error loading contacts from Supabase:', error)
        // Fallback to localStorage
        return loadFromLocalStorage()
      }

      return (data || []).map(dbRowToContact)
    } catch (error) {
      console.error('Error loading contacts:', error)
      return loadFromLocalStorage()
    }
  }

  return loadFromLocalStorage()
}

// Save contacts to Supabase or localStorage fallback
export const saveContacts = async (contacts: Contact[]): Promise<void> => {
  console.log(`💾 Attempting to save ${contacts.length} contacts...`)
  
  if (!isSupabaseConfigured()) {
    console.warn('⚠️ Supabase not configured, saving to localStorage only')
    saveToLocalStorage(contacts)
    return
  }

  try {
    console.log(`🗑️ Deleting existing contacts from Supabase...`)
    
    // Delete all existing contacts and insert new ones
    const { error: deleteError } = await supabase
      .from('contacts')
      .delete()
      .neq('id', '') // Delete all

    if (deleteError) {
      console.error('❌ Error deleting contacts:', deleteError)
      throw new Error(`Failed to delete existing contacts: ${deleteError.message}`)
    }

    console.log('✅ Successfully deleted existing contacts')

    if (contacts.length > 0) {
      const dbRows = contacts.map(contactToDbRow)
      console.log(`📤 Inserting ${dbRows.length} contacts into Supabase...`)
      console.log('Sample row:', JSON.stringify(dbRows[0], null, 2))
      
      const { error: insertError, data } = await supabase
        .from('contacts')
        .insert(dbRows)
        .select()

      if (insertError) {
        console.error('❌ Error saving contacts to Supabase:', insertError)
        console.error('Error details:', JSON.stringify(insertError, null, 2))
        throw new Error(`Failed to save contacts: ${insertError.message}`)
      }
      
      console.log(`✅ Successfully saved ${data?.length || 0} contacts to Supabase`)
    } else {
      console.log('ℹ️ No contacts to save')
    }
    
    // Also save to localStorage as backup
    saveToLocalStorage(contacts)
  } catch (error) {
    console.error('❌ Error saving contacts:', error)
    // Save to localStorage as fallback
    saveToLocalStorage(contacts)
    throw error // Re-throw so caller knows it failed
  }
}

// Save a single contact (update or insert)
export const saveContact = async (contact: Contact): Promise<void> => {
  if (isSupabaseConfigured()) {
    try {
      const dbRow = contactToDbRow(contact)
      const { error } = await supabase
        .from('contacts')
        .upsert(dbRow, { onConflict: 'id' })

      if (error) {
        console.error('Error saving contact to Supabase:', error)
        // Fallback: reload all and save to localStorage
        const contacts = await loadContacts()
        const updated = contacts.map(c => c.id === contact.id ? contact : c)
        saveToLocalStorage(updated)
      }
    } catch (error) {
      console.error('Error saving contact:', error)
      const contacts = await loadContacts()
      const updated = contacts.map(c => c.id === contact.id ? contact : c)
      saveToLocalStorage(updated)
    }
  } else {
    const contacts = loadFromLocalStorage()
    const updated = contacts.map(c => c.id === contact.id ? contact : c)
    saveToLocalStorage(updated)
  }
}

// Delete a contact
export const deleteContact = async (contactId: string): Promise<void> => {
  if (isSupabaseConfigured()) {
    try {
      const { error } = await supabase
        .from('contacts')
        .delete()
        .eq('id', contactId)

      if (error) {
        console.error('Error deleting contact from Supabase:', error)
        // Fallback to localStorage
        const contacts = loadFromLocalStorage()
        const updated = contacts.filter(c => c.id !== contactId)
        saveToLocalStorage(updated)
      }
    } catch (error) {
      console.error('Error deleting contact:', error)
      const contacts = loadFromLocalStorage()
      const updated = contacts.filter(c => c.id !== contactId)
      saveToLocalStorage(updated)
    }
  } else {
    const contacts = loadFromLocalStorage()
    const updated = contacts.filter(c => c.id !== contactId)
    saveToLocalStorage(updated)
  }
}

// LocalStorage fallback functions
const loadFromLocalStorage = (): Contact[] => {
  if (typeof window === 'undefined') return []
  const saved = localStorage.getItem('glazyr-contacts')
  return saved ? JSON.parse(saved) : []
}

const saveToLocalStorage = (contacts: Contact[]): void => {
  if (typeof window === 'undefined') return
  localStorage.setItem('glazyr-contacts', JSON.stringify(contacts))
}

