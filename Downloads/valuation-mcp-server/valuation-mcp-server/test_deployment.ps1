# Test Deployment - Version 1.3.0 with Package Stats

$baseUrl = "https://valuation-mcp-server-554655392699.us-central1.run.app"

Write-Host "🧪 Testing Deployment - Version 1.3.0" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/health"
    Write-Host "  ✅ Version: $($health.version)" -ForegroundColor Green
    Write-Host "  ✅ Status: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Health check failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Package Stats Tool
Write-Host "Test 2: Package Stats for React" -ForegroundColor Yellow
try {
    $body = @{
        tool = "get_package_stats"
        arguments = @{
            owner = "facebook"
            repo = "react"
        }
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "$baseUrl/mcp/invoke" -Method Post -Body $body -ContentType "application/json"
    $result = $response.content[0].text | ConvertFrom-Json
    
    Write-Host "  ✅ Package Manager: $($result.package_manager)" -ForegroundColor Green
    Write-Host "  ✅ Package Name: $($result.package_name)" -ForegroundColor Green
    Write-Host "  ✅ Weekly Downloads: $($result.stats.weekly_downloads)" -ForegroundColor Green
    Write-Host "  ✅ Latest Version: $($result.stats.latest_version)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Package stats test failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Full Analysis with Agent Executor
Write-Host "Test 3: Full Analysis with Package Stats (React)" -ForegroundColor Yellow
try {
    $body = @{
        tool = "agent_executor"
        arguments = @{
            input = "what is the unicorn score for facebook/react?"
        }
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "$baseUrl/mcp/invoke" -Method Post -Body $body -ContentType "application/json"
    $resultText = $response.content[0].text
    $result = $resultText | ConvertFrom-Json
    
    Write-Host "  ✅ Repository: $($result.repository)" -ForegroundColor Green
    if ($result.package_stats) {
        Write-Host "  ✅ Package Stats Found: $($result.package_stats.package_manager)" -ForegroundColor Green
        Write-Host "  ✅ Ecosystem Adoption Score: $($result.ecosystem_adoption_score)/100" -ForegroundColor Green
    }
    if ($result.unicorn_hunter) {
        Write-Host "  ✅ Unicorn Score: $($result.unicorn_hunter.unicorn_score)/100" -ForegroundColor Green
        Write-Host "  ✅ Status: $($result.unicorn_hunter.status)" -ForegroundColor Green
    }
    Write-Host "  ✅ Summary: $($result.summary)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Full analysis test failed: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "✅ Deployment Testing Complete!" -ForegroundColor Cyan
