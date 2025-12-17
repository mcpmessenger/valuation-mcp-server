#!/bin/bash
# Comprehensive test script for Valuation MCP Server
# Tests various endpoints and edge cases

ENDPOINT="https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke"
BASE_URL="https://valuation-mcp-server-554655392699.us-central1.run.app"

echo "🧪 Valuation MCP Server Test Suite"
echo "===================================="
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
echo "--------------------"
curl -s "$BASE_URL/health" | python -m json.tool 2>/dev/null || curl -s "$BASE_URL/health"
echo -e "\n"

# Test 2: Manifest Check
echo "Test 2: MCP Manifest"
echo "--------------------"
curl -s "$BASE_URL/mcp/manifest" | python -m json.tool 2>/dev/null || curl -s "$BASE_URL/mcp/manifest" | head -20
echo -e "\n"

# Test 3: Basic repository analysis (well-known project)
echo "Test 3: Basic Analysis - facebook/react"
echo "----------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"tool": "agent_executor", "arguments": {"input": "analyze facebook/react"}}' \
  -o test_react.json 2>/dev/null
echo "Response saved to test_react.json"
echo -e "\n"

# Test 4: Deep codebase analysis
echo "Test 4: Deep Codebase Analysis - vercel/next.js"
echo "------------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"tool": "agent_executor", "arguments": {"input": "analyze vercel/next.js with deep codebase analysis and calculate unicorn score"}}' \
  -o test_nextjs.json 2>/dev/null
echo "Response saved to test_nextjs.json"
echo -e "\n"

# Test 5: Unicorn score for small project
echo "Test 5: Unicorn Score - mcpmessenger/slashmcp"
echo "----------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"tool": "agent_executor", "arguments": {"input": "what is the unicorn score for mcpmessenger/slashmcp with codebase analysis?"}}' \
  -o test_slashmcp.json 2>/dev/null
echo "Response saved to test_slashmcp.json"
echo -e "\n"

# Test 6: Edge Case - Non-existent repository
echo "Test 6: Error Handling - Non-existent Repository"
echo "------------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"tool": "agent_executor", "arguments": {"input": "analyze this/does-not-exist-repo-12345"}}' \
  -o test_error.json 2>/dev/null
echo "Response saved to test_error.json"
echo -e "\n"

# Test 7: Direct tool invocation - analyze_github_repository
echo "Test 7: Direct Tool - analyze_github_repository"
echo "------------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"tool": "analyze_github_repository", "arguments": {"owner": "langchain-ai", "repo": "langchain"}}' \
  -o test_langchain.json 2>/dev/null
echo "Response saved to test_langchain.json"
echo -e "\n"

# Test 8: Codebase analysis tool
echo "Test 8: Direct Tool - analyze_codebase"
echo "----------------------------------------"
# First get repo_data, then analyze codebase
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"tool": "analyze_github_repository", "arguments": {"owner": "fastapi", "repo": "fastapi"}}' \
  -o test_fastapi_repo.json 2>/dev/null
echo "Repository analysis saved to test_fastapi_repo.json"
echo -e "\n"

# Test 9: Invalid request format
echo "Test 9: Error Handling - Invalid Request Format"
echo "------------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "agent_executor", "tool_input": {"input": "test"}}' \
  -o test_invalid_format.json 2>/dev/null
echo "Response saved to test_invalid_format.json"
echo -e "\n"

echo "✅ Test suite completed!"
echo ""
echo "📊 Summary:"
echo "  - Health check: test_health.json"
echo "  - React analysis: test_react.json"
echo "  - Next.js analysis: test_nextjs.json"
echo "  - SlashMCP analysis: test_slashmcp.json"
echo "  - Error handling: test_error.json, test_invalid_format.json"
echo "  - Direct tools: test_langchain.json, test_fastapi_repo.json"
echo ""
echo "Review the JSON files to validate responses."
