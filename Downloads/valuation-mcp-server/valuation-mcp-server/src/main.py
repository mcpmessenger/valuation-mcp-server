from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
from typing import Dict, Any, Optional, Tuple
import os
import logging

import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from tools.github_analysis import GitHubAnalysisTool
from tools.valuation_models import ValuationCalculator, ValuationInputs
from tools.codebase_analysis import CodebaseAnalysisTool
from tools.package_stats import PackageStatsTool
import re

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Initialize tools
github_tool = GitHubAnalysisTool()
valuation_calculator = ValuationCalculator()
codebase_tool = CodebaseAnalysisTool()
package_stats_tool = PackageStatsTool()


def extract_repo_from_query(query: str) -> Optional[Tuple[str, str]]:
    """
    Extract owner/repo from natural language queries.
    Handles formats like: 'owner/repo', 'analyze owner/repo', 'what's the valuation of owner/repo'
    """
    # Pattern to match owner/repo format
    patterns = [
        r'([a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38})/([a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,100})',  # owner/repo
        r'repository\s+([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',  # repository owner/repo
        r'repo\s+([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',  # repo owner/repo
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return (match.group(1), match.group(2))
    
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager for startup/shutdown"""
    # Startup
    logger.info("🚀 Valuation MCP Server starting...")
    yield
    # Shutdown
    logger.info("👋 Valuation MCP Server shutting down...")


app = FastAPI(
    title="Valuation Analysis MCP Server",
    version="1.3.0",
    description="MCP Server for analyzing and valuing GitHub repositories - Now with Unicorn Hunter 🦄 and Package Stats 📦",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


# MCP Manifest Endpoint
@app.get("/mcp/manifest")
async def get_manifest():
    """Return MCP manifest declaring available tools"""
    return {
        "name": "valuation-analysis-mcp-server",
        "version": "1.3.0",
        "description": "Tools for analyzing and valuing GitHub repositories - Now with Unicorn Hunter 🦄 and Package Stats 📦",
        "tools": [
            {
                "name": "analyze_github_repository",
                "description": "ALWAYS USE THIS FIRST when analyzing a repository. Comprehensive analysis of a GitHub repository including metrics, scores, and development activity. Extract owner and repo from user queries like 'analyze owner/repo' or 'what's the valuation of owner/repo'. Returns repo_data needed for other tools.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "owner": {"type": "string", "description": "GitHub repository owner (e.g., 'langchain-ai' from 'langchain-ai/langchain')"},
                        "repo": {"type": "string", "description": "GitHub repository name (e.g., 'langchain' from 'langchain-ai/langchain')"}
                    },
                    "required": ["owner", "repo"]
                }
            },
            {
                "name": "calculate_valuation",
                "description": "Calculate repository valuation using multiple methodologies. REQUIRES repo_data from analyze_github_repository. Use 'unicorn_hunter' method when users ask for 'unicorn score' or 'unicorn valuation'.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_data": {"type": "object", "description": "Repository analysis data from analyze_github_repository tool - MUST call analyze_github_repository first"},
                        "method": {"type": "string", "enum": ["cost_based", "market_based", "scorecard", "income_based", "unicorn_hunter"], "description": "Valuation methodology. Use 'unicorn_hunter' for unicorn scores, 'scorecard' for general valuation ranges"},
                        "team_size": {"type": "integer", "description": "Development team size (optional, default: 1)"},
                        "hourly_rate": {"type": "number", "description": "Hourly development rate (optional, default: 100.0)"},
                        "development_months": {"type": "integer", "description": "Development duration in months (optional, default: 6)"},
                        "market_multiplier": {"type": "number", "description": "Market multiplier (optional, default: 10.0)"}
                    },
                    "required": ["repo_data", "method"]
                }
            },
            {
                "name": "compare_with_market",
                "description": "Compare repository with market benchmarks and similar projects. Requires repo_metrics from analyze_github_repository.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_metrics": {"type": "object", "description": "Repository metrics from analyze_github_repository tool"},
                        "category": {"type": "string", "description": "Project category (e.g., 'mcp-server', 'langchain', optional)"}
                    },
                    "required": ["repo_metrics"]
                }
            },
            {
                "name": "agent_executor",
                "description": "Intelligent agent that handles natural language queries about repository valuation. Automatically extracts repository info and chains tool calls. Use this for queries like 'what's the unicorn score for owner/repo?' or 'analyze owner/repo'. This tool will automatically call analyze_github_repository and other tools as needed.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "input": {"type": "string", "description": "Natural language query about repository valuation, analysis, or unicorn scores. Examples: 'what's the unicorn score for langchain-ai/langchain?', 'analyze mcpmessenger/slashmcp', 'calculate valuation of owner/repo using unicorn_hunter'"}
                    },
                    "required": ["input"]
                }
            },
            {
                "name": "analyze_codebase",
                "description": "Analyze codebase quality, complexity, architecture, dependencies, and documentation. Provides comprehensive code analysis including complexity metrics, test coverage, security vulnerabilities, and architecture patterns. REQUIRES repo_data from analyze_github_repository.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_data": {"type": "object", "description": "Repository data from analyze_github_repository tool"},
                        "analysis_depth": {"type": "string", "enum": ["quick", "standard", "deep"], "description": "Depth of analysis - quick (5min), standard (15min), deep (30min)", "default": "standard"},
                        "include_metrics": {"type": "array", "items": {"type": "string", "enum": ["complexity", "quality", "tests", "dependencies", "architecture", "documentation", "technology"]}, "description": "Which analysis categories to include", "default": ["all"]}
                    },
                    "required": ["repo_data"]
                }
            },
            {
                "name": "get_package_stats",
                "description": "Get package download statistics from npm, PyPI, or Cargo registries. Provides ecosystem adoption metrics beyond GitHub stars. Automatically detects package manager and fetches download stats.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "owner": {"type": "string", "description": "GitHub repository owner"},
                        "repo": {"type": "string", "description": "GitHub repository name"},
                        "package_name": {"type": "string", "description": "Optional explicit package name (if different from repo name)"}
                    },
                    "required": ["owner", "repo"]
                }
            },
            {
                "name": "unicorn_hunter",
                "description": "🦄 Unicorn Hunter: Calculate speculative valuation ranges with $1B maximum. Returns unicorn score (0-100) and speculative valuation estimates. Enhanced with codebase analysis and package stats when available. USE THIS when users ask for 'unicorn score', 'unicorn valuation', or 'what's the unicorn potential'. REQUIRES repo_data from analyze_github_repository - MUST call analyze_github_repository first. Optionally accepts codebase_analysis and package_stats for enhanced scoring.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_data": {"type": "object", "description": "Repository analysis data from analyze_github_repository tool - MUST call analyze_github_repository first to get this data"},
                        "codebase_analysis": {"type": "object", "description": "Optional codebase analysis from analyze_codebase tool for enhanced scoring"},
                        "include_codebase_analysis": {"type": "boolean", "description": "Whether to include codebase analysis in valuation (if codebase_analysis provided)", "default": True}
                    },
                    "required": ["repo_data"]
                }
            }
        ]
    }


# MCP Tool Invocation Endpoint
@app.post("/mcp/invoke")
async def invoke_tool(request: Dict[str, Any]):
    """Invoke a valuation analysis tool"""
    tool_name = request.get("tool")
    arguments = request.get("arguments", {})
    
    # Provide helpful error messages for common mistakes
    if not tool_name:
        # Check for common alternative field names
        if "tool_name" in request:
            raise HTTPException(
                status_code=400, 
                detail="Invalid request format. Use 'tool' instead of 'tool_name'. Expected format: {'tool': 'tool_name', 'arguments': {...}}"
            )
        if "tool_input" in request or "input" in request:
            raise HTTPException(
                status_code=400,
                detail="Invalid request format. Use 'tool' and 'arguments' fields. Expected format: {'tool': 'tool_name', 'arguments': {...}}"
            )
        raise HTTPException(
            status_code=400,
            detail="Missing 'tool' field. Expected format: {'tool': 'tool_name', 'arguments': {...}}"
        )
    
    try:
        if tool_name == "analyze_github_repository":
            owner = arguments.get("owner")
            repo = arguments.get("repo")
            if not owner or not repo:
                raise HTTPException(status_code=400, detail="Missing owner or repo")
            
            logger.info(f"Analyzing repository: {owner}/{repo}")
            result = github_tool.analyze_repository(owner, repo)
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False
            }
        
        elif tool_name == "calculate_valuation":
            repo_data = arguments.get("repo_data")
            method = arguments.get("method", "scorecard")
            
            if not repo_data:
                raise HTTPException(status_code=400, detail="Missing repo_data")
            
            logger.info(f"Calculating valuation using method: {method}")
            
            inputs = ValuationInputs(
                repo_data=repo_data,
                team_size=arguments.get("team_size", 1),
                hourly_rate=arguments.get("hourly_rate", 100.0),
                development_months=arguments.get("development_months", 6),
                market_multiplier=arguments.get("market_multiplier", 10.0)
            )
            
            if method == "cost_based":
                value = valuation_calculator.calculate_cost_based(inputs)
                result = {"method": method, "valuation": round(value, 2), "currency": "USD"}
            elif method == "market_based":
                value = valuation_calculator.calculate_market_based(inputs)
                result = {"method": method, "valuation": round(value, 2), "currency": "USD"}
            elif method == "scorecard":
                result = valuation_calculator.calculate_scorecard(inputs)
            elif method == "income_based":
                result = valuation_calculator.calculate_income_based(inputs)
            elif method == "unicorn_hunter":
                result = valuation_calculator.calculate_unicorn_hunter(inputs)
            else:
                raise HTTPException(status_code=400, detail=f"Unknown valuation method: {method}")
            
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False
            }
        
        elif tool_name == "compare_with_market":
            repo_metrics = arguments.get("repo_metrics")
            category = arguments.get("category", "general")
            
            if not repo_metrics:
                raise HTTPException(status_code=400, detail="Missing repo_metrics")
            
            logger.info(f"Comparing with market benchmarks for category: {category}")
            
            # Placeholder for market comparison logic
            result = {
                "category": category,
                "repo_metrics": repo_metrics,
                "market_benchmarks": {
                    "average_stars": 150,
                    "average_forks": 30,
                    "average_contributors": 5,
                    "median_valuation": 50000
                },
                "comparison": {
                    "stars_percentile": 75,
                    "forks_percentile": 60,
                    "activity_percentile": 70
                }
            }
            
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False
            }
        
        elif tool_name == "analyze_codebase":
            repo_data = arguments.get("repo_data")
            
            if not repo_data:
                raise HTTPException(status_code=400, detail="Missing repo_data")
            
            basic_info = repo_data.get("basic_info", {})
            repo_name = basic_info.get("name", "")
            
            if not repo_name:
                raise HTTPException(status_code=400, detail="Invalid repo_data: missing basic_info.name")
            
            # Extract owner/repo from name
            parts = repo_name.split("/")
            if len(parts) != 2:
                raise HTTPException(status_code=400, detail="Invalid repository name format")
            
            owner, repo = parts
            
            analysis_depth = arguments.get("analysis_depth", "standard")
            include_metrics = arguments.get("include_metrics", ["all"])
            
            logger.info(f"Analyzing codebase: {owner}/{repo} (depth: {analysis_depth})")
            
            result = codebase_tool.analyze_codebase(
                owner=owner,
                repo=repo,
                analysis_depth=analysis_depth,
                include_metrics=include_metrics
            )
            
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": result.get("status") == "failed"
            }
        
        elif tool_name == "get_package_stats":
            owner = arguments.get("owner")
            repo = arguments.get("repo")
            package_name = arguments.get("package_name")
            
            if not owner or not repo:
                raise HTTPException(status_code=400, detail="Missing owner or repo")
            
            logger.info(f"Fetching package stats: {owner}/{repo}")
            
            result = package_stats_tool.get_package_stats(owner, repo, package_name)
            
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": result.get("status") != "success"
            }
        
        elif tool_name == "unicorn_hunter":
            repo_data = arguments.get("repo_data")
            codebase_analysis = arguments.get("codebase_analysis")
            include_codebase = arguments.get("include_codebase_analysis", True)
            
            if not repo_data:
                raise HTTPException(status_code=400, detail="Missing repo_data")
            
            logger.info("🦄 Running Unicorn Hunter analysis...")
            
            inputs = ValuationInputs(
                repo_data=repo_data,
                team_size=arguments.get("team_size", 1),
                hourly_rate=arguments.get("hourly_rate", 100.0),
                development_months=arguments.get("development_months", 6),
                market_multiplier=arguments.get("market_multiplier", 10.0)
            )
            
            # Use codebase analysis if provided and enabled
            if codebase_analysis and include_codebase:
                result = valuation_calculator.calculate_unicorn_hunter(inputs, codebase_analysis=codebase_analysis)
            else:
                result = valuation_calculator.calculate_unicorn_hunter(inputs)
            
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False
            }
        
        elif tool_name == "agent_executor":
            user_input = arguments.get("input", "")
            
            if not user_input:
                raise HTTPException(status_code=400, detail="Missing input query")
            
            logger.info(f"Agent executor processing query: {user_input}")
            
            # Extract repository info from query
            repo_info = extract_repo_from_query(user_input.lower())
            
            if not repo_info:
                return {
                    "content": [{"type": "text", "text": json.dumps({
                        "error": "Could not extract repository information from query",
                        "hint": "Please provide repository in format 'owner/repo' (e.g., 'langchain-ai/langchain')",
                        "example_queries": [
                            "what's the unicorn score for langchain-ai/langchain?",
                            "analyze mcpmessenger/slashmcp",
                            "calculate valuation of owner/repo using unicorn_hunter"
                        ]
                    }, indent=2)}],
                    "isError": True
                }
            
            owner, repo = repo_info
            logger.info(f"Extracted repository: {owner}/{repo}")
            
            # Step 1: Analyze repository
            try:
                repo_data = github_tool.analyze_repository(owner, repo)
                if "error" in repo_data:
                    return {
                        "content": [{"type": "text", "text": json.dumps(repo_data, indent=2)}],
                        "isError": True
                    }
            except Exception as e:
                logger.error(f"Error analyzing repository: {e}")
                return {
                    "content": [{"type": "text", "text": json.dumps({
                        "error": f"Failed to analyze repository: {str(e)}",
                        "repository": f"{owner}/{repo}"
                    }, indent=2)}],
                    "isError": True
                }
            
            # Step 2: Determine what the user wants
            query_lower = user_input.lower()
            result = {
                "repository": f"{owner}/{repo}",
                "analysis": repo_data
            }
            
            # Check for unicorn score requests
            if any(keyword in query_lower for keyword in ["unicorn", "unicorn score", "unicorn valuation", "unicorn potential"]):
                logger.info("User requested unicorn score - calculating...")
                
                # Fetch package stats for ecosystem adoption metrics
                package_stats = None
                try:
                    logger.info("Fetching package statistics for ecosystem adoption...")
                    package_stats = package_stats_tool.get_package_stats(owner, repo)
                    if package_stats.get("status") == "success":
                        result["package_stats"] = package_stats
                        adoption_score = package_stats_tool.calculate_adoption_score(package_stats)
                        result["ecosystem_adoption_score"] = round(adoption_score, 1)
                except Exception as e:
                    logger.warning(f"Package stats fetch failed, continuing without it: {e}")
                
                # Optionally perform codebase analysis for enhanced scoring
                # Check if user wants deep analysis or if it's a standard request
                perform_codebase_analysis = "deep" in query_lower or "codebase" in query_lower or "code" in query_lower
                
                codebase_analysis = None
                if perform_codebase_analysis:
                    try:
                        logger.info("Performing codebase analysis for enhanced scoring...")
                        codebase_analysis = codebase_tool.analyze_codebase(
                            owner=owner,
                            repo=repo,
                            analysis_depth="standard",
                            include_metrics=["all"]
                        )
                        if codebase_analysis.get("status") == "success":
                            result["codebase_analysis"] = codebase_analysis
                    except Exception as e:
                        logger.warning(f"Codebase analysis failed, continuing without it: {e}")
                
                inputs = ValuationInputs(repo_data=repo_data)
                if codebase_analysis and codebase_analysis.get("status") == "success":
                    unicorn_result = valuation_calculator.calculate_unicorn_hunter(inputs, codebase_analysis=codebase_analysis)
                else:
                    unicorn_result = valuation_calculator.calculate_unicorn_hunter(inputs)
                
                # Add package stats info to summary if available
                if package_stats and package_stats.get("status") == "success":
                    pkg_mgr = package_stats.get("package_manager", "unknown")
                    adoption = result.get("ecosystem_adoption_score", 0)
                    unicorn_result["ecosystem_adoption"] = {
                        "package_manager": pkg_mgr,
                        "adoption_score": adoption,
                        "package_name": package_stats.get("package_name")
                    }
                    result["summary"] = f"🦄 Unicorn Score: {unicorn_result['unicorn_score']}/100 - {unicorn_result['status']} | 📦 {pkg_mgr.upper()} Adoption: {adoption}/100"
                else:
                    result["summary"] = f"🦄 Unicorn Score: {unicorn_result['unicorn_score']}/100 - {unicorn_result['status']}"
                
                result["unicorn_hunter"] = unicorn_result
            
            # Check for general valuation requests
            elif any(keyword in query_lower for keyword in ["valuation", "value", "worth", "price"]):
                method = "scorecard"
                if "cost" in query_lower or "cost-based" in query_lower:
                    method = "cost_based"
                elif "market" in query_lower or "market-based" in query_lower:
                    method = "market_based"
                elif "income" in query_lower or "revenue" in query_lower:
                    method = "income_based"
                
                logger.info(f"User requested valuation - calculating using {method} method...")
                inputs = ValuationInputs(repo_data=repo_data)
                
                if method == "cost_based":
                    value = valuation_calculator.calculate_cost_based(inputs)
                    result["valuation"] = {"method": method, "valuation": round(value, 2), "currency": "USD"}
                elif method == "market_based":
                    value = valuation_calculator.calculate_market_based(inputs)
                    result["valuation"] = {"method": method, "valuation": round(value, 2), "currency": "USD"}
                elif method == "scorecard":
                    result["valuation"] = valuation_calculator.calculate_scorecard(inputs)
                elif method == "income_based":
                    result["valuation"] = valuation_calculator.calculate_income_based(inputs)
            
            # Default: just return analysis with suggestion
            else:
                result["suggestion"] = "Repository analyzed. Use 'unicorn_hunter' for unicorn scores or 'calculate_valuation' for detailed valuations."
            
            return {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False
            }
        
        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error invoking tool {tool_name}: {str(e)}")
        return {
            "content": [{"type": "text", "text": f"Error: {str(e)}"}],
            "isError": True
        }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {
        "status": "healthy",
        "service": "valuation-mcp-server",
        "version": "1.3.0",
        "features": ["analyze_github_repository", "calculate_valuation", "compare_with_market", "unicorn_hunter"]
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "name": "Valuation Analysis MCP Server",
        "version": "1.3.0",
        "description": "MCP Server for analyzing and valuing GitHub repositories - Now with Unicorn Hunter 🦄",
        "endpoints": {
            "manifest": "/mcp/manifest",
            "invoke": "/mcp/invoke",
            "health": "/health"
        },
        "features": {
            "unicorn_hunter": "Speculative valuation with $1B maximum cap"
        }
    }


if __name__ == "__main__":
    import uvicorn
    # Cloud Run provides PORT env var, default to 8001 for local development
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
