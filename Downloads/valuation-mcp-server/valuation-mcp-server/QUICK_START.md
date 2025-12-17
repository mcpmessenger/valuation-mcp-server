# Quick Start Guide - Valuation MCP Server

## Service URL
**Production:** `https://valuation-mcp-server-554655392699.us-central1.run.app`

## Correct Request Format

The `/mcp/invoke` endpoint expects this exact format:

```json
{
  "tool": "tool_name",
  "arguments": { ... }
}
```

⚠️ **Common Mistakes:**
- ❌ `{"tool_name": "..."}` → ✅ `{"tool": "..."}`
- ❌ `{"tool_input": {...}}` → ✅ `{"arguments": {...}}`
- ❌ `{"input": "..."}` → ✅ `{"arguments": {"input": "..."}}`

## Working Examples

### 1. Agent Executor (Natural Language)

```bash
curl -X POST "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "agent_executor",
    "arguments": {
      "input": "what'\''s the unicorn score for mcpmessenger/slashmcp?"
    }
  }'
```

### 2. Analyze Repository

```bash
curl -X POST "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "analyze_github_repository",
    "arguments": {
      "owner": "mcpmessenger",
      "repo": "slashmcp"
    }
  }'
```

### 3. Unicorn Hunter (requires repo_data from analyze_github_repository)

**Step 1: Analyze**
```bash
curl -X POST "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "analyze_github_repository",
    "arguments": {
      "owner": "mcpmessenger",
      "repo": "slashmcp"
    }
  }' > analysis.json
```

**Step 2: Extract repo_data and calculate unicorn score**
```bash
# Use the repo_data from analysis.json in the unicorn_hunter call
curl -X POST "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "unicorn_hunter",
    "arguments": {
      "repo_data": <paste_repo_data_from_analysis.json>
    }
  }'
```

**Or use agent_executor (recommended):**
```bash
curl -X POST "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "agent_executor",
    "arguments": {
      "input": "calculate unicorn score for mcpmessenger/slashmcp"
    }
  }'
```

## PowerShell Examples

### Agent Executor
```powershell
$body = @{
    tool = "agent_executor"
    arguments = @{
        input = "what's the unicorn score for mcpmessenger/slashmcp?"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

### Analyze Repository
```powershell
$body = @{
    tool = "analyze_github_repository"
    arguments = @{
        owner = "mcpmessenger"
        repo = "slashmcp"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

## Python Examples

```python
import requests
import json

# Agent Executor
response = requests.post(
    "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke",
    json={
        "tool": "agent_executor",
        "arguments": {
            "input": "what's the unicorn score for mcpmessenger/slashmcp?"
        }
    }
)
print(json.dumps(response.json(), indent=2))
```

## Available Tools

1. **agent_executor** - Natural language queries (recommended)
2. **analyze_github_repository** - Get repository metrics
3. **calculate_valuation** - Calculate valuations using various methods
4. **unicorn_hunter** - Get unicorn scores (requires repo_data)
5. **compare_with_market** - Compare with market benchmarks

## Troubleshooting

### Error: "Tool 'None' not found"
**Cause:** Wrong field names in request  
**Fix:** Use `tool` and `arguments` (not `tool_name` and `tool_input`)

### Error: "Missing repo_data"
**Cause:** Trying to use unicorn_hunter without analyzing first  
**Fix:** Use `agent_executor` which handles this automatically, or call `analyze_github_repository` first

### Error: "Could not extract repository information"
**Cause:** Repository format not recognized in query  
**Fix:** Ensure query contains `owner/repo` format (e.g., "mcpmessenger/slashmcp")

## Health Check

```bash
curl https://valuation-mcp-server-554655392699.us-central1.run.app/health
```

## Get Manifest

```bash
curl https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/manifest
```

