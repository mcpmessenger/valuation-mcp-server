#!/bin/bash
# Test Package Stats Integration

ENDPOINT="https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke"

echo "🧪 Testing Package Stats Integration"
echo "====================================="
echo ""

# Test 1: React (npm package)
echo "Test 1: facebook/react (should find npm package)"
echo "-------------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "agent_executor",
    "arguments": {
      "input": "what is the unicorn score for facebook/react?"
    }
  }' > test_react.json

echo "✅ Response saved to test_react.json"
echo ""

# Test 2: FastAPI (PyPI package)
echo "Test 2: tiangolo/fastapi (should find PyPI package)"
echo "----------------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "agent_executor",
    "arguments": {
      "input": "what is the unicorn score for tiangolo/fastapi?"
    }
  }' > test_fastapi.json

echo "✅ Response saved to test_fastapi.json"
echo ""

# Test 3: Direct package stats tool
echo "Test 3: Direct get_package_stats for react"
echo "--------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_package_stats",
    "arguments": {
      "owner": "facebook",
      "repo": "react"
    }
  }' > test_react_package_stats.json

echo "✅ Response saved to test_react_package_stats.json"
echo ""

# Test 4: Repository without package (should handle gracefully)
echo "Test 4: mcpmessenger/slashmcp (may not have published package)"
echo "---------------------------------------------------------------"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "agent_executor",
    "arguments": {
      "input": "what is the unicorn score for mcpmessenger/slashmcp?"
    }
  }' > test_slashmcp.json

echo "✅ Response saved to test_slashmcp.json"
echo ""

echo "📊 Test Summary:"
echo "  - React analysis: test_react.json"
echo "  - FastAPI analysis: test_fastapi.json"
echo "  - React package stats: test_react_package_stats.json"
echo "  - SlashMCP analysis: test_slashmcp.json"
echo ""
echo "Review the JSON files to see package stats integration."
