# AWS Amplify Deployment Guide

## Quick Setup

1. **Go to AWS Amplify Console**
   - https://console.aws.amazon.com/amplify
   - Sign in to your AWS account

2. **Connect Repository**
   - Click "New app" → "Host web app"
   - Select "GitHub" and authorize
   - Select repository: `mcpmessenger/glazyr-crm-lite`
   - Branch: `main`

3. **Configure Build Settings - CRITICAL STEP**
   - Go to your Amplify app → App settings → Build settings → Edit
   - **IMPORTANT**: Look for "Package manager" dropdown
   - **MUST SET**: Change from "Auto-detect" to "npm"
   - Set Node.js version to 18.x or 20.x
   - The `amplify.yml` file will handle the rest
   - **NOTE**: If you don't see "Package manager" option, you may need to:
     - Clear build cache (App settings → Build settings → Clear cache)
     - Or disconnect and reconnect the repository

4. **Add Environment Variables**
   - Go to App settings → Environment variables
   - Add:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

5. **Deploy**
   - Click "Save and deploy"
   - Wait for build to complete

## Advantages over Vercel
- More control over deployment
- Better for AWS ecosystem integration
- Free tier available

## After Deployment
- Your app will be available at: `https://[app-id].amplifyapp.com`
- You can add a custom domain in Amplify settings

