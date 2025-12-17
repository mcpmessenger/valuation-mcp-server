# Google Cloud Deployment Guide

This guide will help you deploy the Valuation MCP Server to Google Cloud Run using the gcloud CLI.

## Prerequisites

1. **Google Cloud Account**: Sign up at https://cloud.google.com
2. **Google Cloud SDK (gcloud CLI)**: Install from https://cloud.google.com/sdk/docs/install
3. **Docker Desktop** (optional, if using local Docker build): https://www.docker.com/products/docker-desktop
4. **GCP Project**: Create a project in Google Cloud Console

## Step 1: Install Google Cloud SDK

### Windows
1. Download the installer from: https://cloud.google.com/sdk/docs/install
2. Run the installer and follow the prompts
3. Restart your terminal/PowerShell

### Verify Installation
```powershell
gcloud --version
```

## Step 2: Authenticate and Configure

### Login to Google Cloud
```powershell
gcloud auth login
```
This will open a browser window for authentication.

### Set Your Project ID
```powershell
# List available projects
gcloud projects list

# Set your project (replace YOUR_PROJECT_ID with your actual project ID)
gcloud config set project YOUR_PROJECT_ID
```

### Verify Configuration
```powershell
gcloud config list
```

## Step 3: Enable Required APIs

```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## Step 4: Deploy to Cloud Run

### Option A: Using PowerShell Script (Recommended for Windows)

```powershell
# Set your project ID as environment variable
$env:GCP_PROJECT_ID = "your-project-id"

# Run the deployment script
.\deploy-gcp.ps1 -ProjectId "your-project-id" -Region "us-central1"
```

Or without parameters (will prompt for project ID):
```powershell
.\deploy-gcp.ps1
```

### Option B: Manual Deployment with gcloud CLI

#### Step 1: Build and Push Image
```powershell
# Set variables
$PROJECT_ID = "your-project-id"
$REGION = "us-central1"
$SERVICE_NAME = "valuation-mcp-server"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Build and push using Cloud Build (recommended)
gcloud builds submit --tag $IMAGE_NAME
```

#### Step 2: Deploy to Cloud Run
```powershell
gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --set-env-vars="LOG_LEVEL=INFO,ENVIRONMENT=production" `
    --port=8001 `
    --memory=512Mi `
    --cpu=1 `
    --timeout=300 `
    --max-instances=100
```

### Option C: Using Cloud Build with Dockerfile

If you prefer to use local Docker (requires Docker Desktop):

```powershell
# Build locally
docker build -t $IMAGE_NAME:latest .

# Configure Docker to use gcloud as credential helper
gcloud auth configure-docker

# Push to Google Container Registry
docker push $IMAGE_NAME:latest

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_NAME:latest `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --port=8001 `
    --memory=512Mi `
    --cpu=1
```

## Step 5: Get Service URL

After deployment, get your service URL:

```powershell
gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)'
```

Or view all services:
```powershell
gcloud run services list
```

## Step 6: Test Your Deployment

```powershell
# Get the service URL
$SERVICE_URL = gcloud run services describe valuation-mcp-server --region us-central1 --format='value(status.url)'

# Test health endpoint
Invoke-RestMethod -Uri "$SERVICE_URL/health"

# Test manifest endpoint
Invoke-RestMethod -Uri "$SERVICE_URL/mcp/manifest"

# Test tool invocation
$body = @{
    tool = "analyze_github_repository"
    arguments = @{
        owner = "python"
        repo = "cpython"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "$SERVICE_URL/mcp/invoke" -Method Post -Body $body -ContentType "application/json"
```

## Environment Variables

You can set environment variables during deployment:

```powershell
gcloud run deploy valuation-mcp-server `
    --image $IMAGE_NAME:latest `
    --set-env-vars="GITHUB_TOKEN=your_token_here,LOG_LEVEL=INFO,ENVIRONMENT=production" `
    --region $REGION
```

Or update existing service:
```powershell
gcloud run services update valuation-mcp-server `
    --set-env-vars="GITHUB_TOKEN=your_token_here" `
    --region $REGION
```

## Update Deployment

To update your service with new code:

```powershell
# Rebuild and push
gcloud builds submit --tag $IMAGE_NAME

# Redeploy (Cloud Run will automatically use the new image)
gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_NAME `
    --region $REGION
```

## View Logs

```powershell
# View recent logs
gcloud run services logs read valuation-mcp-server --region $REGION

# Follow logs in real-time
gcloud run services logs tail valuation-mcp-server --region $REGION
```

## Delete Service

To remove the service:

```powershell
gcloud run services delete valuation-mcp-server --region $REGION
```

## Troubleshooting

### Authentication Issues
```powershell
# Re-authenticate
gcloud auth login

# Set application default credentials
gcloud auth application-default login
```

### Build Failures
- Check that Dockerfile is correct
- Verify all dependencies in requirements.txt
- Check Cloud Build logs in Google Cloud Console

### Deployment Failures
- Ensure APIs are enabled
- Check service quotas
- Verify project billing is enabled

### Service Not Accessible
- Check that `--allow-unauthenticated` flag was used
- Verify IAM permissions
- Check service logs for errors

## Cost Considerations

Cloud Run pricing:
- **Free Tier**: 2 million requests/month, 400,000 GB-seconds, 200,000 vCPU-seconds
- **Pay-as-you-go**: $0.40 per million requests, $0.00002400 per GB-second, $0.00001000 per vCPU-second

The service is configured with:
- 512Mi memory
- 1 CPU
- Auto-scaling (0 to 100 instances)

## Security Best Practices

1. **Use Service Accounts**: Create dedicated service accounts for production
2. **Secrets Management**: Use Secret Manager for sensitive data like GitHub tokens
3. **VPC**: Consider VPC connector for private networking
4. **IAM**: Restrict access using IAM policies
5. **HTTPS**: Cloud Run provides HTTPS by default

## Next Steps

- Set up monitoring and alerts in Cloud Console
- Configure custom domain (optional)
- Set up CI/CD pipeline
- Add authentication if needed
- Configure rate limiting


