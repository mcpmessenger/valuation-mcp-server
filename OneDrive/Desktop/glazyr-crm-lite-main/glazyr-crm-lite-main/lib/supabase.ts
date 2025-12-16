import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

if (typeof window !== 'undefined') {
  // Client-side: log for debugging
  if (!supabaseUrl || !supabaseAnonKey) {
    console.warn('⚠️ Supabase credentials not found. Using localStorage fallback.')
    console.warn('URL:', supabaseUrl ? '✅ Set' : '❌ Missing')
    console.warn('Key:', supabaseAnonKey ? '✅ Set' : '❌ Missing')
  } else {
    console.log('✅ Supabase configured:', supabaseUrl.substring(0, 30) + '...')
  }
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: false
  }
})

