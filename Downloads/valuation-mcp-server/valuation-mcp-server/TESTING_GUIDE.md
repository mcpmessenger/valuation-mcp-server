# Testing Guide for Valuation Analysis MCP Server

This guide shows multiple ways to test all endpoints of the MCP server.

## Prerequisites

Make sure the server is running:
```bash
python src/main.py
```

The server will start on `http://localhost:8001`

## Method 1: Using the Test Script (Recommended)

Run the comprehensive test script:

```bash
python test_endpoints.py
```

This will test all endpoints and show detailed results.

## Method 2: Using Python Requests

### Health Check
```python
import requests
response = requests.get("http://localhost:8001/health")
print(response.json())
```

### Root Endpoint
```python
import requests
response = requests.get("http://localhost:8001/")
print(response.json())
```

### Get MCP Manifest
```python
import requests
response = requests.get("http://localhost:8001/mcp/manifest")
print(response.json())
```

### Analyze GitHub Repository
```python
import requests
import json

payload = {
    "tool": "analyze_github_repository",
    "arguments": {
        "owner": "python",
        "repo": "cpython"
    }
}

response = requests.post(
    "http://localhost:8001/mcp/invoke",
    json=payload
)
print(json.dumps(response.json(), indent=2))
```

### Calculate Valuation
```python
import requests
import json

repo_data = {
    "metrics": {
        "stars": 250,
        "forks": 50
    },
    "scores": {
        "overall_score": 0.8,
        "health_score": 0.85,
        "activity_score": 0.8,
        "community_score": 0.75
    },
    "development": {
        "contributors": 15,
        "total_commits": 500
    }
}

payload = {
    "tool": "calculate_valuation",
    "arguments": {
        "repo_data": repo_data,
        "method": "scorecard",  # or "cost_based", "market_based", "income_based"
        "team_size": 2,
        "hourly_rate": 150.0,
        "development_months": 12
    }
}

response = requests.post(
    "http://localhost:8001/mcp/invoke",
    json=payload
)
print(json.dumps(response.json(), indent=2))
```

### Compare with Market
```python
import requests
import json

payload = {
    "tool": "compare_with_market",
    "arguments": {
        "repo_metrics": {
            "stars": 150,
            "forks": 30,
            "contributors": 8
        },
        "category": "mcp-server"
    }
}

response = requests.post(
    "http://localhost:8001/mcp/invoke",
    json=payload
)
print(json.dumps(response.json(), indent=2))
```

## Method 3: Using cURL (Command Line)

### Health Check
```bash
curl http://localhost:8001/health
```

### Root Endpoint
```bash
curl http://localhost:8001/
```

### Get MCP Manifest
```bash
curl http://localhost:8001/mcp/manifest
```

### Analyze GitHub Repository
```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "analyze_github_repository",
    "arguments": {
      "owner": "python",
      "repo": "cpython"
    }
  }'
```

### Calculate Valuation
```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "calculate_valuation",
    "arguments": {
      "repo_data": {
        "metrics": {"stars": 250, "forks": 50},
        "scores": {"overall_score": 0.8, "health_score": 0.85, "activity_score": 0.8, "community_score": 0.75},
        "development": {"contributors": 15, "total_commits": 500}
      },
      "method": "scorecard"
    }
  }'
```

## Method 4: Using Browser (GET endpoints only)

You can test GET endpoints directly in your browser:

- Health: http://localhost:8001/health
- Root: http://localhost:8001/
- Manifest: http://localhost:8001/mcp/manifest

## Method 5: Using PowerShell (Windows)

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/health" -Method Get
```

### Analyze Repository
```powershell
$body = @{
    tool = "analyze_github_repository"
    arguments = @{
        owner = "python"
        repo = "cpython"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/mcp/invoke" -Method Post -Body $body -ContentType "application/json"
```

## Available Valuation Methods

When using `calculate_valuation`, you can specify these methods:

1. **`cost_based`** - Development cost replacement value
2. **`market_based`** - Value based on market comparables
3. **`scorecard`** - Multi-factor scoring approach (returns range)
4. **`income_based`** - Revenue-based valuation
5. **`unicorn_hunter`** - 🦄 Speculative valuation with $1B maximum (returns unicorn score and ranges)

### Unicorn Hunter Example

```python
import requests
import json

repo_data = {
    "metrics": {
        "stars": 5000,
        "forks": 1200,
        "watchers": 300
    },
    "scores": {
        "overall_score": 0.85,
        "health_score": 0.9,
        "activity_score": 0.8,
        "community_score": 0.75
    },
    "development": {
        "contributors": 50,
        "total_commits": 2000,
        "commit_frequency": 8.5
    }
}

# Method 1: Use unicorn_hunter tool directly
payload = {
    "tool": "unicorn_hunter",
    "arguments": {
        "repo_data": repo_data
    }
}

response = requests.post("http://localhost:8001/mcp/invoke", json=payload)
result = json.loads(response.json()["content"][0]["text"])

print(f"🦄 Unicorn Score: {result['unicorn_score']}/100")
print(f"Status: {result['status']}")
print(f"Valuation Range: ${result['speculative_valuation_ranges']['conservative']:,.0f} - ${result['speculative_valuation_ranges']['optimistic']:,.0f}")

# Method 2: Use as valuation method
payload = {
    "tool": "calculate_valuation",
    "arguments": {
        "repo_data": repo_data,
        "method": "unicorn_hunter"
    }
}

response = requests.post("http://localhost:8001/mcp/invoke", json=payload)
result = json.loads(response.json()["content"][0]["text"])

print(json.dumps(result, indent=2))
```

## Example: Complete Workflow

### Method 1: Using Agent Executor (Recommended for Natural Language)

```python
import requests
import json

# Single natural language query - agent handles everything
payload = {
    "tool": "agent_executor",
    "arguments": {
        "input": "what's the unicorn score for langchain-ai/langchain?"
    }
}

response = requests.post("http://localhost:8001/mcp/invoke", json=payload)
result = json.loads(response.json()["content"][0]["text"])

print(f"Repository: {result['repository']}")
print(result['summary'])  # "🦄 Unicorn Score: 85.2/100 - 🚀 Soaring! ($500M+ potential)"
print(f"Full Analysis: {json.dumps(result['analysis'], indent=2)}")
```

### Method 2: Manual Tool Chaining

```python
import requests
import json

# Step 1: Analyze a repository
analyze_payload = {
    "tool": "analyze_github_repository",
    "arguments": {
        "owner": "fastapi",
        "repo": "fastapi"
    }
}

response = requests.post("http://localhost:8001/mcp/invoke", json=analyze_payload)
repo_data = json.loads(response.json()["content"][0]["text"])

# Step 2: Calculate valuation using the analyzed data
valuation_payload = {
    "tool": "calculate_valuation",
    "arguments": {
        "repo_data": repo_data,
        "method": "scorecard"
    }
}

response = requests.post("http://localhost:8001/mcp/invoke", json=valuation_payload)
valuation = json.loads(response.json()["content"][0]["text"])

print(f"Repository: {repo_data['basic_info']['name']}")
print(f"Stars: {repo_data['metrics']['stars']}")
print(f"Valuation Range: ${valuation['valuation_range']['low']:,.0f} - ${valuation['valuation_range']['high']:,.0f}")
```

## Troubleshooting

### Connection Error
If you get a connection error, make sure the server is running:
```bash
python src/main.py
```

### Port Already in Use
If port 8001 is already in use, you can change it:
```bash
set PORT=8002
python src/main.py
```

### GitHub API Rate Limits
If you hit GitHub API rate limits, set a GitHub token:
```bash
set GITHUB_TOKEN=your_token_here
python src/main.py
```


