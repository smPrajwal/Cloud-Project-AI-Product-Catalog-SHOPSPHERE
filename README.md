# ShopSphere - Azure 3-Tier Cloud Project

A product catalog web app deployed on Azure using a 3-tier architecture with CI/CD automation.

## What This Project Demonstrates

- **3-Tier Architecture** on Azure (Frontend VMs, Backend VMs, SQL Database)
- **Infrastructure as Code** using Terraform with modular design
- **CI/CD Pipeline** using Jenkins with multiple deployment modes
- **AI Integration** via Azure Functions + Computer Vision for auto image tagging
- **Monitoring & Alerts** using Log Analytics and Application Insights

## Architecture Overview

```
                    ┌─────────────────┐
                    │   Public Load   │
                    │    Balancer     │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
     ┌────────▼────────┐           ┌────────▼────────┐
     │  Frontend VMSS  │           │  Frontend VMSS  │
     │   (Flask App)   │           │   (Flask App)   │
     └────────┬────────┘           └────────┬────────┘
              │                             │
              └──────────────┬──────────────┘
                             │
                    ┌────────▼────────┐
                    │  Internal Load  │
                    │    Balancer     │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
     ┌────────▼────────┐           ┌────────▼────────┐
     │  Backend VMSS   │           │  Backend VMSS   │
     │   (Flask API)   │           │   (Flask API)   │
     └────────┬────────┘           └────────┬────────┘
              │                             │
              └──────────────┬──────────────┘
                             │
                    ┌────────▼────────┐
                    │   Azure SQL     │
                    │    Database     │
                    └─────────────────┘
```

## Project Structure

```
├── Azure_Terraform/          # Infrastructure as Code
│   ├── main.tf               # Main config with 8 modules
│   ├── variables.tf          # All configurable parameters
│   ├── terraform.tfvars      # Variable values
│   └── modules/
│       ├── network_core/     # VNet, Subnets, NSGs
│       ├── compute_VM/       # VM Scale Sets + Autoscaling
│       ├── database/         # Azure SQL Server + DB
│       ├── storage/          # Blob Storage
│       ├── azure_ai/         # Computer Vision service
│       ├── azure_functions/  # Serverless function
│       ├── network_ingress/  # Load Balancers
│       └── monitoring_and_alerts/  # Log Analytics, App Insights
│
├── Azure_Function/           # Serverless AI tagging function
│   └── image_tags_fn/        # Blob-triggered function
│
├── Jenkinsfile               # CI/CD Pipeline (12 stages)
│
├── backend/                  # Backend Flask API
├── frontend/                 # Frontend Flask App
├── database/                 # DB initialization scripts
└── common/                   # Shared utilities
```

## CI/CD Pipeline

The Jenkins pipeline has 4 modes:

| Mode | What It Does |
|------|--------------|
| Clone and Package (CI) | Validates code, creates zip artifacts |
| Deploy Infrastructure (CD) | Provisions Azure resources, deploys app |
| Full Pipeline (CICD) | Complete end-to-end deployment |
| De-provision | Tears down all infrastructure |

**Pipeline Stages:**
1. Pre-build Validation
2. Packaging
3. Push to Artifacts
4. Manual Approval
5. Terraform Apply
6. Azure Authentication
7. Blob Upload
8. Azure Function Deployment
9. Smoke Testing
10. Email Notification

## Azure Resources Created

- Resource Group
- Virtual Network with Subnets
- 2x VM Scale Sets (Frontend + Backend) with Autoscaling
- Public Load Balancer + Internal Load Balancer
- Azure SQL Database
- Storage Account (for code + images)
- Azure Function App (Blob trigger)
- Azure AI Vision
- Log Analytics Workspace
- Application Insights
- Alert Action Group

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AZURE_SQL_CONN` | ODBC connection string for Azure SQL |
| `AZURE_STORAGE_CONNECTION_STRING` | Blob storage connection |
| `VISION_KEY` | Azure Computer Vision key |
| `VISION_ENDPOINT` | Azure Computer Vision endpoint |
| `ADMIN_USERNAME` | App admin username |
| `ADMIN_PASSWORD` | App admin password |

## How to Deploy

1. **Setup Jenkins** with required credentials (Azure SP, Terraform Cloud token)
2. **Configure Terraform Cloud** workspace for remote state
3. **Run the Pipeline** - Select "Full Pipeline (CICD)" mode
4. **Access the App** - Use the public IP from Terraform output

## Quick Test

After deployment:
1. Open the public load balancer IP in browser
2. Browse products on homepage
3. Login at `/admin-auth` (admin credentials)
4. Upload a product image → AI tags are auto-generated

## Tech Stack

- **Cloud**: Azure (IaaS)
- **IaC**: Terraform + Terraform Cloud
- **CI/CD**: Jenkins
- **App**: Python Flask
- **Database**: Azure SQL
- **AI**: Azure Computer Vision
- **Monitoring**: Log Analytics, Application Insights
