# PowerShell deployment script for Valuation MCP Server to Google Cloud Run
# Version: 1.1.0 - Includes Unicorn Hunter feature

param(
    [string]$ProjectId = "",
    [string]$Region = "us-central1",
    [string]$ServiceName = "valuation-mcp-server"
)

$ErrorActionPreference = "Stop"

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Yellow "🚀 Deploying Valuation MCP Server to Google Cloud Run"
Write-Output ""

# Check if gcloud is installed
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-ColorOutput Red "❌ gcloud CLI is not installed. Please install it first."
    Write-Output "Download from: https://cloud.google.com/sdk/docs/install"
    exit 1
}

# Check if docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-ColorOutput Red "❌ Docker is not installed. Please install it first."
    Write-Output "Download from: https://www.docker.com/products/docker-desktop"
    exit 1
}

# Get project ID if not provided
if ([string]::IsNullOrEmpty($ProjectId)) {
    $ProjectId = $env:GCP_PROJECT_ID
    if ([string]::IsNullOrEmpty($ProjectId)) {
        Write-Output "Enter your GCP Project ID:"
        $ProjectId = Read-Host
        if ([string]::IsNullOrEmpty($ProjectId)) {
            Write-ColorOutput Red "❌ Project ID is required"
            exit 1
        }
    }
}

$ImageName = "gcr.io/$ProjectId/$ServiceName"

Write-Output "Project ID: $ProjectId"
Write-Output "Region: $Region"
Write-Output "Service: $ServiceName"
Write-Output "Image: $ImageName"
Write-Output ""

# Set the GCP project
Write-ColorOutput Yellow "Setting GCP project..."
gcloud config set project $ProjectId
if ($LASTEXITCODE -ne 0) {
    Write-ColorOutput Red "❌ Failed to set GCP project"
    exit 1
}

# Enable required APIs
Write-ColorOutput Yellow "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and push using Cloud Build (recommended for Windows)
Write-ColorOutput Yellow "🔨 Building and pushing Docker image using Cloud Build..."
gcloud builds submit --tag $ImageName
if ($LASTEXITCODE -ne 0) {
    Write-ColorOutput Red "❌ Cloud Build failed"
    exit 1
}
Write-ColorOutput Green "✅ Image built and pushed successfully"

# Deploy to Cloud Run
Write-ColorOutput Yellow "🚀 Deploying to Cloud Run..."
gcloud run deploy $ServiceName `
    --image $ImageName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --set-env-vars="LOG_LEVEL=INFO,ENVIRONMENT=production" `
    --port=8001 `
    --memory=512Mi `
    --cpu=1 `
    --timeout=300 `
    --max-instances=100

if ($LASTEXITCODE -ne 0) {
    Write-ColorOutput Red "❌ Cloud Run deployment failed"
    exit 1
}

Write-ColorOutput Green "✅ Deployment complete!"

# Get the service URL
$ServiceUrl = gcloud run services describe $ServiceName --region $Region --format='value(status.url)'
Write-Output ""
Write-ColorOutput Green "🌐 Service URL: $ServiceUrl"
Write-Output ""
Write-Output "Test the service with:"
Write-Output "  curl $ServiceUrl/health"
Write-Output "  curl $ServiceUrl/mcp/manifest"
Write-Output ""
Write-Output "Or in PowerShell:"
Write-Output ('  Invoke-RestMethod -Uri ' + $ServiceUrl + '/health')
Write-Output ('  Invoke-RestMethod -Uri ' + $ServiceUrl + '/mcp/manifest')


