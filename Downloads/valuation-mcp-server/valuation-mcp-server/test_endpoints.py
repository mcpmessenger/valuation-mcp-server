#!/usr/bin/env python3
"""
Test script for Valuation Analysis MCP Server endpoints
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8001"

def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_health():
    """Test health check endpoint"""
    print("\n[TEST] Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print("\n[TEST] Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)
    return response.status_code == 200

def test_manifest():
    """Test MCP manifest endpoint"""
    print("\n[TEST] Testing MCP Manifest Endpoint...")
    response = requests.get(f"{BASE_URL}/mcp/manifest")
    print_response("MCP Manifest", response)
    return response.status_code == 200

def test_analyze_repository(owner: str = "python", repo: str = "cpython"):
    """Test analyze_github_repository tool"""
    print(f"\n[TEST] Testing Analyze GitHub Repository: {owner}/{repo}...")
    payload = {
        "tool": "analyze_github_repository",
        "arguments": {
            "owner": owner,
            "repo": repo
        }
    }
    response = requests.post(f"{BASE_URL}/mcp/invoke", json=payload)
    print_response(f"Analyze Repository: {owner}/{repo}", response)
    
    if response.status_code == 200:
        result = response.json()
        if not result.get("isError"):
            repo_data = json.loads(result["content"][0]["text"])
            print(f"\n[SUCCESS] Repository Analysis Successful!")
            print(f"   - Stars: {repo_data.get('metrics', {}).get('stars', 'N/A')}")
            print(f"   - Forks: {repo_data.get('metrics', {}).get('forks', 'N/A')}")
            print(f"   - Overall Score: {repo_data.get('scores', {}).get('overall_score', 'N/A'):.2f}")
            return True
    return False

def test_calculate_valuation(method: str = "scorecard"):
    """Test calculate_valuation tool"""
    print(f"\n[TEST] Testing Calculate Valuation (method: {method})...")
    
    # Sample repo data
    repo_data = {
        "metrics": {
            "stars": 250,
            "forks": 50,
            "watchers": 30,
            "open_issues": 8
        },
        "scores": {
            "health_score": 0.85,
            "activity_score": 0.8,
            "community_score": 0.75,
            "overall_score": 0.8
        },
        "development": {
            "total_commits": 500,
            "contributors": 15,
            "last_commit_date": "2024-12-16",
            "commit_frequency": 8.5
        }
    }
    
    payload = {
        "tool": "calculate_valuation",
        "arguments": {
            "repo_data": repo_data,
            "method": method,
            "team_size": 2,
            "hourly_rate": 150.0,
            "development_months": 12
        }
    }
    
    response = requests.post(f"{BASE_URL}/mcp/invoke", json=payload)
    print_response(f"Calculate Valuation ({method})", response)
    
    if response.status_code == 200:
        result = response.json()
        if not result.get("isError"):
            valuation_data = json.loads(result["content"][0]["text"])
            print(f"\n[SUCCESS] Valuation Calculation Successful!")
            if method == "scorecard":
                print(f"   - Total Score: {valuation_data.get('total_score', 'N/A')}")
                print(f"   - Valuation Range: ${valuation_data.get('valuation_range', {}).get('low', 'N/A'):,.0f} - ${valuation_data.get('valuation_range', {}).get('high', 'N/A'):,.0f}")
            else:
                print(f"   - Valuation: ${valuation_data.get('valuation', 'N/A'):,.2f}")
            return True
    return False

def test_compare_with_market():
    """Test compare_with_market tool"""
    print("\n[TEST] Testing Compare with Market...")
    
    repo_metrics = {
        "stars": 150,
        "forks": 30,
        "contributors": 8,
        "open_issues": 5
    }
    
    payload = {
        "tool": "compare_with_market",
        "arguments": {
            "repo_metrics": repo_metrics,
            "category": "mcp-server"
        }
    }
    
    response = requests.post(f"{BASE_URL}/mcp/invoke", json=payload)
    print_response("Compare with Market", response)
    return response.status_code == 200

def test_all_valuation_methods():
    """Test all valuation methods"""
    methods = ["cost_based", "market_based", "scorecard", "income_based"]
    print("\n[TEST] Testing All Valuation Methods...")
    for method in methods:
        test_calculate_valuation(method)

def main():
    """Run all tests"""
    print("="*60)
    print("Valuation Analysis MCP Server - Endpoint Tests")
    print("="*60)
    
    results = []
    
    # Basic endpoints
    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    results.append(("MCP Manifest", test_manifest()))
    
    # Tool invocations
    results.append(("Analyze Repository", test_analyze_repository()))
    results.append(("Calculate Valuation (Scorecard)", test_calculate_valuation("scorecard")))
    results.append(("Compare with Market", test_compare_with_market()))
    
    # Test all valuation methods
    test_all_valuation_methods()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to server.")
        print("   Make sure the server is running on http://localhost:8001")
        print("   Start it with: python src/main.py")
    except Exception as e:
        print(f"[ERROR] {e}")

