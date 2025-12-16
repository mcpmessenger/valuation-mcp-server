# Supabase Setup Guide

Follow these steps to enable cross-device sync for your Glazyr CRM:

## Step 1: Create a Supabase Account

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up for a free account (no credit card required)
3. Create a new project

## Step 2: Create the Database Table

1. In your Supabase project dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy and paste the contents of `supabase-setup.sql`
4. Click **Run** to execute the SQL

## Step 3: Get Your API Keys

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (this is your `NEXT_PUBLIC_SUPABASE_URL`)
   - **anon/public key** (this is your `NEXT_PUBLIC_SUPABASE_ANON_KEY`)

## Step 4: Add Environment Variables

### For Local Development:

1. Create a `.env.local` file in the root of your project
2. Add the following:

```env
NEXT_PUBLIC_SUPABASE_URL=your-project-url-here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

### For Vercel Deployment:

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add the following variables:
   - `NEXT_PUBLIC_SUPABASE_URL` = your Supabase project URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = your Supabase anon key
4. Redeploy your application

## Step 5: Install Dependencies

Run this command to install the Supabase client:

```bash
npm install
```

## Step 6: Test It Out

1. Start your development server: `npm run dev`
2. Upload your CSV file
3. Check your Supabase dashboard → **Table Editor** → **contacts** to see your data
4. Open the app on your phone - your data should sync!

## Troubleshooting

- **Data not syncing?** Check the browser console for errors
- **Still using localStorage?** Make sure your environment variables are set correctly
- **Can't see data in Supabase?** Check that the SQL script ran successfully

## Security Note

The current setup allows public read/write access. If you want to add authentication later, you'll need to:
1. Set up Supabase Auth
2. Update the RLS policies in the SQL script
3. Add authentication to your Next.js app

For now, this setup works great for personal use and cross-device sync!


