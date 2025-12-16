# Agent Orchestrator Frontend

This repo powers the public-facing UI that orchestrates your AI agents. It is wired directly to your `v0.app` chat deployment and keeps everything in sync with each push.

[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/sentilabs/v0-agent-orchestrator-frontend) [![Built with v0](https://img.shields.io/badge/Built%20with-v0.app-black?style=for-the-badge)](https://v0.app/chat/eE3GXgFOAV1)

## What Makes It Fire

- **Modern Next.js + Tailwind stack**: Structured routing, clean global styles, and a tokenized utility layer make it simple to expand screens.
- **Composable UI primitives**: `components/ui` contains reusable controls that mirror the v0 experience but allow you to extend interactions when needed.
- **Agent orchestration focus**: `components/query-orchestration.tsx` and `components/server-management.tsx` wrap the experience around multi-agent execution and deployment oversight.
- **Auto-deploy workflow**: Changes committed here can flow through Vercel for preview/staging with your v0-backed backend staying live and upgraded.

## Local development

1. Clone the repo and install dependencies:
   ```
   pnpm install
   ```
2. Start the dev server (hot reload + Fast Refresh):
   ```
   pnpm dev
   ```
3. Open `http://localhost:3000` to see the Orchestrator UI and experiment with agent queries.

## Deployments

- **Live site**: [https://vercel.com/sentilabs/v0-agent-orchestrator-frontend](https://vercel.com/sentilabs/v0-agent-orchestrator-frontend)
- **Authoring workspace**: [https://v0.app/chat/eE3GXgFOAV1](https://v0.app/chat/eE3GXgFOAV1)

## Keep it synced

1. Make your UI edits locally or inside [v0.app](https://v0.app).
2. Commit and push to this repo (`git push agent-orchestrator main`).
3. Vercel automatically deploys the latest build, and your v0 chat stays in sync.

If something feels off, rerun `git fetch agent-orchestrator` and merge carefully—this repo and the `agent-orchestrator` remote can diverge because the stack lives inside your parent directory.
