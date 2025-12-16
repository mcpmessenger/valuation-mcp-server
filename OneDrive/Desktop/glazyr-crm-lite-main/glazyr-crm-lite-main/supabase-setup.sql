-- Run this SQL in your Supabase SQL Editor to create the contacts table

CREATE TABLE IF NOT EXISTS contacts (
  id TEXT PRIMARY KEY,
  company TEXT NOT NULL,
  parent TEXT NOT NULL,
  tier TEXT NOT NULL CHECK (tier IN ('Tier 1', 'Tier 2', 'Tier 3')),
  target_role TEXT NOT NULL,
  strategic_rationale TEXT NOT NULL,
  head_of_corp_dev TEXT,
  head_of_ai_strategy TEXT,
  linkedin_profile_search TEXT,
  company_context TEXT,
  recommended_outreach_angle TEXT,
  cold_email_initial TEXT,
  linkedin_dm_short TEXT,
  follow_up_email TEXT,
  contact_name TEXT,
  email TEXT,
  linkedin TEXT,
  channel TEXT,
  status TEXT NOT NULL DEFAULT 'Not Yet Contacted' CHECK (status IN ('Not Yet Contacted', 'Reached Out', 'Follow-up Sent', 'Replied', 'Passed')),
  first_touch_date TEXT,
  follow_up_sent BOOLEAN DEFAULT FALSE,
  response_type TEXT CHECK (response_type IN ('Curious', 'Neutral', 'Pass')),
  interest_level TEXT CHECK (interest_level IN ('Low', 'Medium', 'High')),
  notes TEXT,
  what_they_reacted_to TEXT,
  objections TEXT,
  suggested_next_step TEXT CHECK (suggested_next_step IN ('Demo', 'Check-in', 'None')),
  contact_count INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS) - for now, allow all operations
-- You can restrict this later if you add authentication
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations (public access)
-- Remove this and add proper auth if you want security
CREATE POLICY "Allow all operations on contacts" ON contacts
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- Create an index for faster queries
CREATE INDEX IF NOT EXISTS idx_contacts_company ON contacts(company);
CREATE INDEX IF NOT EXISTS idx_contacts_tier ON contacts(tier);
CREATE INDEX IF NOT EXISTS idx_contacts_status ON contacts(status);


