# Valuation Analysis MCP Server

A Model Context Protocol (MCP) server for analyzing and valuing GitHub repositories. Built with FastAPI and designed for deployment on Google Cloud Platform (GCP).

## Overview

The Valuation Analysis MCP Server provides tools for:

- **Repository Analysis**: Comprehensive GitHub repository metrics including health scores, activity levels, and community engagement
- **Valuation Calculation**: Multiple valuation methodologies (cost-based, market-based, scorecard, income-based)
- **Market Comparison**: Benchmarking against similar projects and market data

## Features

- 🚀 **FastAPI-based MCP Server**: RESTful API following MCP standards
- 📊 **Multiple Valuation Methods**: Cost-based, market-based, scorecard, and income-based approaches
- 🔍 **GitHub Integration**: Direct API integration for repository analysis
- 🌐 **GCP Cloud Run Ready**: Optimized for serverless deployment
- 🐳 **Docker Support**: Multi-stage build for minimal image size
- 📈 **Health Checks**: Built-in health endpoints for monitoring
- 🔒 **CORS Enabled**: Configurable cross-origin resource sharing

## Project Structure

```
valuation-mcp-server/
├── src/
│   ├── main.py                 # FastAPI application and MCP endpoints
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── github_analysis.py  # GitHub repository analysis tool
│   │   └── valuation_models.py # Valuation calculation models
├── tests/
│   └── test_valuation_tools.py # Unit tests
├── Dockerfile                   # Multi-stage Docker build
├── deploy-gcp.sh               # GCP Cloud Run deployment script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
└── README.md                   # This file
```

## Installation

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Google Cloud SDK (for GCP deployment)
- GitHub token (optional, for higher API rate limits)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd valuation-mcp-server
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the server**
   ```bash
   python src/main.py
   ```

The server will start on `http://localhost:8001`

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8001 | Server port |
| `ENVIRONMENT` | development | Environment (development/production) |
| `LOG_LEVEL` | INFO | Logging level |
| `GITHUB_TOKEN` | (empty) | GitHub API token for higher rate limits |
| `ALLOWED_ORIGINS` | * | CORS allowed origins |
| `GCP_PROJECT_ID` | (empty) | GCP project ID |
| `GCP_REGION` | us-central1 | GCP region |

## API Endpoints

### Health Check
```bash
GET /health
```

Returns server health status.

### MCP Manifest
```bash
GET /mcp/manifest
```

Returns the MCP manifest with available tools.

### Tool Invocation
```bash
POST /mcp/invoke
Content-Type: application/json

{
  "tool": "tool_name",
  "arguments": { ... }
}
```

**Important:** The request body must use `tool` (not `tool_name`) and `arguments` (not `tool_input` or `input`).

**Example:**
```bash
curl -X POST https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "agent_executor",
    "arguments": {
      "input": "what'\''s the unicorn score for langchain-ai/langchain?"
    }
  }'
```

## Available Tools

### 1. Analyze GitHub Repository

Analyzes a GitHub repository and returns comprehensive metrics.

**Request:**
```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "analyze_github_repository",
    "arguments": {
      "owner": "mcpmessenger",
      "repo": "LangchainMCP"
    }
  }'
```

**Response:**
```json
{
  "basic_info": {
    "name": "mcpmessenger/LangchainMCP",
    "description": "...",
    "primary_language": "Python",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-12-16T00:00:00Z"
  },
  "metrics": {
    "stars": 150,
    "forks": 30,
    "watchers": 10,
    "open_issues": 5
  },
  "scores": {
    "health_score": 0.8,
    "activity_score": 0.75,
    "community_score": 0.65,
    "overall_score": 0.73
  },
  "development": {
    "total_commits": 250,
    "contributors": 8,
    "last_commit_date": "2024-12-16",
    "commit_frequency": 5.2
  }
}
```

### 2. Calculate Valuation

Calculates repository valuation using specified methodology.

**Request:**
```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "calculate_valuation",
    "arguments": {
      "repo_data": { ... },
      "method": "scorecard",
      "team_size": 2,
      "hourly_rate": 150.0,
      "development_months": 12
    }
  }'
```

**Supported Methods:**
- `cost_based`: Development cost replacement value
- `market_based`: Value based on market comparables
- `scorecard`: Multi-factor scoring approach
- `income_based`: Revenue-based valuation
- `unicorn_hunter`: 🦄 Speculative valuation with $1B maximum - returns unicorn score (0-100) and speculative ranges

### 3. Compare with Market

Compares repository metrics against market benchmarks.

**Request:**
```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "compare_with_market",
    "arguments": {
      "repo_metrics": { ... },
      "category": "mcp-server"
    }
  }'
```

### 4. Unicorn Hunter 🦄

Calculates speculative valuation ranges with $1B maximum. Returns a unicorn score (0-100) and speculative valuation estimates.

### 5. Agent Executor (Natural Language)

Intelligent agent that handles natural language queries and automatically chains tool calls. Perfect for conversational interfaces.

**Request:**
```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "agent_executor",
    "arguments": {
      "input": "what'\''s the unicorn score for langchain-ai/langchain?"
    }
  }'
```

**Response:**
```json
{
  "repository": "langchain-ai/langchain",
  "analysis": { ... },
  "unicorn_hunter": {
    "unicorn_score": 85.2,
    "status": "🚀 Soaring! ($500M+ potential)",
    ...
  },
  "summary": "🦄 Unicorn Score: 85.2/100 - 🚀 Soaring! ($500M+ potential)"
}
```

**Supported Query Formats:**
- "what's the unicorn score for owner/repo?"
- "analyze owner/repo"
- "calculate valuation of owner/repo using unicorn_hunter"
- "what's the value of owner/repo?"

**Request:**
```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "unicorn_hunter",
    "arguments": {
      "repo_data": { ... }
    }
  }'
```

**Or use as a valuation method:**
```bash
curl -X POST http://localhost:8001/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "calculate_valuation",
    "arguments": {
      "repo_data": { ... },
      "method": "unicorn_hunter"
    }
  }'
```

**Response:**
```json
{
  "method": "unicorn_hunter",
  "unicorn_score": 75.5,
  "status": "🚀 Soaring! ($500M+ potential)",
  "tier": "soaring",
  "component_scores": {
    "community_momentum": 82.3,
    "development_velocity": 71.5,
    "technology_quality": 78.0,
    "market_potential": 68.2,
    "network_effects": 73.1
  },
  "speculative_valuation_ranges": {
    "conservative": 45000000.0,
    "realistic": 89000000.0,
    "optimistic": 175000000.0,
    "maximum_cap": 1000000000,
    "currency": "USD"
  },
  "interpretation": {
    "score_meaning": "Score of 75.5/100 indicates 🚀 soaring! ($500m+ potential)",
    "valuation_note": "These are speculative estimates based on GitHub metrics and should not be considered financial advice.",
    "factors_considered": ["community_momentum", "development_velocity", "technology_quality", "market_potential", "network_effects"]
  }
}
```

## Deployment

### Local Docker Build

```bash
docker build -t valuation-mcp-server:latest .
docker run -p 8001:8001 -e GITHUB_TOKEN=your_token valuation-mcp-server:latest
```

### GCP Cloud Run Deployment

1. **Set up GCP credentials**
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   ```

2. **Make the deployment script executable**
   ```bash
   chmod +x deploy-gcp.sh
   ```

3. **Deploy to Cloud Run**
   ```bash
   export GCP_PROJECT_ID=your-project-id
   export GCP_REGION=us-central1
   ./deploy-gcp.sh
   ```

The script will:
- Build the Docker image
- Push to Google Container Registry
- Deploy to Cloud Run
- Output the service URL

### Manual GCP Deployment

```bash
# Build and push image
docker build -t gcr.io/YOUR_PROJECT_ID/valuation-mcp-server:latest .
docker push gcr.io/YOUR_PROJECT_ID/valuation-mcp-server:latest

# Deploy to Cloud Run
gcloud run deploy valuation-mcp-server \
  --image gcr.io/YOUR_PROJECT_ID/valuation-mcp-server:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8001 \
  --memory 512Mi \
  --cpu 1
```

## Testing

### Run Unit Tests

```bash
pytest tests/
```

### Test Endpoints

```bash
# Health check
curl http://localhost:8001/health

# Get manifest
curl http://localhost:8001/mcp/manifest

# Analyze a repository
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

## Integration with LangChain Agent

To integrate with your existing LangChain agent:

```python
from langchain_mcp_adapters import MultiServerMCPClient

client = MultiServerMCPClient({
    "valuation_server": {
        "transport": "http",
        "url": "https://valuation-mcp-server-xyz.run.app/mcp"
    }
})

tools = await client.get_tools()
```

## Performance Considerations

- **Rate Limiting**: GitHub API has rate limits (60 requests/hour unauthenticated, 5000/hour authenticated)
- **Caching**: Consider implementing Redis for caching GitHub API responses
- **Timeouts**: API requests have 10-second timeouts
- **Scaling**: Cloud Run automatically scales based on demand

## Security

- Non-root user execution in Docker
- CORS configuration for production
- Environment variable-based secrets management
- Health checks for monitoring
- Proper error handling without exposing sensitive information

## Monitoring and Logging

The server includes:
- Structured logging with configurable levels
- Health check endpoint for monitoring
- Request/response logging
- Error tracking and reporting

## Future Enhancements

- Redis caching layer for API responses
- Additional data sources (Crunchbase, npm, PyPI)
- Advanced scoring algorithms
- Batch processing for multiple repositories
- WebSocket support for real-time updates
- Authentication and API key management
- Prometheus metrics endpoint

## Troubleshooting

### GitHub API Rate Limit Exceeded

Set a GitHub token in `.env`:
```
GITHUB_TOKEN=your_github_token_here
```

### Port Already in Use

Change the port in `.env`:
```
PORT=8002
```

### Docker Build Fails

Ensure Docker is running and you have sufficient disk space:
```bash
docker system prune -a
```

### Cloud Run Deployment Fails

Check GCP credentials and project configuration:
```bash
gcloud auth list
gcloud config list
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the deployment logs

## Changelog

### Version 1.0.0 (2024-12-16)
- Initial release
- GitHub repository analysis
- Multiple valuation methodologies
- GCP Cloud Run deployment support
- Comprehensive documentation
