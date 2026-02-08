# ShopSphere - Azure 3-Tier Cloud Project

A fully automated, end-to-end cloud deployment of a product catalog web application on Microsoft Azure. Features a 3-tier architecture (Frontend VMs, Backend VMs, SQL Database), Infrastructure as Code with Terraform, Jenkins CI/CD pipeline, AI-powered image tagging and sentiment analysis, autoscaling, and comprehensive monitoring.

## What This Project Demonstrates

- **3-Tier Architecture** on Azure (Frontend VMs, Backend VMs, SQL Database)
- **Infrastructure as Code** using Terraform with 8 modular components
- **Remote State Management** using Terraform Cloud
- **CI/CD Pipeline** using Jenkins with 4 deployment modes (CI, CD, CICD, De-provision)
- **Networking & Security** - VNet, Subnets, NSGs, NAT Gateway, Private Endpoints
- **Load Balancing** - Public and Internal Load Balancers with health probes
- **Autoscaling** - CPU-based scaling for VM Scale Sets
- **Serverless Computing** - Azure Functions with Blob trigger and VNet Integration
- **AI Integration** - Computer Vision for image tagging + Text Analytics for sentiment analysis
- **Monitoring & Alerts** - Log Analytics, Application Insights, CPU alerts with email notifications
- **Secure Credential Management** - Jenkins credentials, SAS tokens, Service Principal authentication

## Architecture Overview

The diagram below shows the main traffic flow and compute layer. Additional components like Blob Storage, Azure Functions, and monitoring are described in the sections above.

```
                        INTERNET
                            │
                    ┌───────▼───────┐
                    │  Public Load  │
                    │   Balancer    │
                    │   (Port 80)   │
                    └───────┬───────┘
                            │
         ┌──────────────────┴──────────────────┐
         │              VNet                   │
         │  ┌───────────────────────────────┐  │
         │  │       Frontend Subnet         │  │
         │  │  ┌─────────┐    ┌─────────┐   │  │
         │  │  │ VMSS    │    │ VMSS    │   │  │
         │  │  │(Flask)  │    │(Flask)  │   │  │
         │  │  └────┬────┘    └────┬────┘   │  │
         │  │       │              │        │  │
         │  └───────┼──────────────┼────────┘  │
         │          └──────┬───────┘           │
         │                 │                   │
         │         ┌───────▼───────┐           │
         │         │ Internal Load │           │
         │         │   Balancer    │           │
         │         └───────┬───────┘           │
         │                 │                   │
         │  ┌──────────────┼───────────────┐   │
         │  │       Backend Subnet         │   │
         │  │  ┌─────────┐    ┌─────────┐  │   │
         │  │  │ VMSS    │    │ VMSS    │  │   │
         │  │  │(API)    │    │(API)    │  │   │
         │  │  └────┬────┘    └────┬────┘  │   │
         │  │       │    NAT GW    │       │   │
         │  └───────┼──────────────┼───────┘   │
         │          └──────┬───────┘           │
         │                 │                   │
         │  ┌──────────────┼───────────────┐   │
         │  │       Database Subnet        │   │
         │  │  ┌─────────────────────────┐ │   │
         │  │  │  Private Endpoint       │ │   │
         │  │  │  (Azure SQL Database)   │ │   │
         │  │  └─────────────────────────┘ │   │
         │  └──────────────────────────────┘   │
         │                                     │
         │  ┌──────────────────────────────┐   │
         │  │       Function Subnet        │   │
         │  │  ┌─────────────────────────┐ │   │
         │  │  │  Azure Function (AI)    │ │   │
         │  │  │  + VNet Integration     │ │   │
         │  │  └───────────┬─────────────┘ │   │
         │  └──────────────┼───────────────┘   │
         │                 │                   │
         └─────────────────┼───────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
     ┌────────▼────────┐      ┌─────────▼─────────┐
     │  Blob Storage   │      │  Azure Computer   │
     │ (Images + Code) │      │     Vision        │
     └─────────────────┘      └───────────────────┘
```

**Additional Components (not shown above):**
- Log Analytics Workspace for centralized logging
- Application Insights connected to the Function App
- Monitor Metric Alerts for CPU usage on VMSS
- Alert Action Group for email notifications
- Private DNS Zone for database name resolution
- Azure Text Analytics for review sentiment analysis

## Detailed Description

This project is a complete end-to-end cloud deployment that brings together multiple Azure services, infrastructure automation, and a working web application. The main goal was to build something that mimics real-world production setups, not just a toy project.

### Infrastructure (Terraform)

All the Azure resources are provisioned using Terraform with a modular approach. Instead of putting everything in one giant file, the infrastructure code is split into 8 separate modules for things like networking, compute, database, storage, and so on. This makes it easier to maintain and reuse. The Terraform state is stored remotely in Terraform Cloud, so there's no risk of local state file issues when working from different machines.

The infrastructure includes:
- A Virtual Network with multiple subnets (frontend, backend, database, and function subnets), each with its own purpose and security rules
- Network Security Groups (NSGs) at both subnet and VM levels to control traffic flow
- A NAT Gateway attached to the backend subnet so those VMs can reach the internet for package updates and external API calls
- Private Endpoints for the database, meaning the SQL Server is not exposed to the public internet at all
- Private DNS Zone linked to the VNet for internal name resolution

### Compute and Autoscaling

The application runs on two VM Scale Sets. One for the frontend (serves the UI) and one for the backend (handles API requests). Both scale sets run Ubuntu 22.04 LTS and are configured with autoscaling rules based on CPU usage. If CPU goes above 80%, a new instance spins up. If it drops below 30%, an instance gets removed. This keeps costs in check while handling traffic spikes.

Each VM is provisioned using cloud-init scripts that do a lot of heavy lifting—install Python, set up a virtual environment, install the ODBC Driver 18 for SQL Server connectivity, download the zipped application code from Blob Storage using a SAS token, and configure the Flask app as a SystemD service. The app runs under Gunicorn (a production WSGI server) with 4 workers. SystemD handles restarts if the process crashes. All of this happens automatically, no SSH required after deployment.

### Networking and Load Balancing

Traffic flows through two load balancers. The public-facing load balancer sits in front of the frontend VMs and accepts requests on port 80. It forwards traffic to the Flask apps running on port 8000. The frontend then talks to the backend through an internal load balancer, which is not exposed to the internet. This separation keeps the backend layer protected.

Health probes are configured on both load balancers to check if the Flask apps are responding. If a VM becomes unhealthy, it stops receiving traffic until it recovers.

### Database

The project uses Azure SQL Database. The SQL Server has public network access disabled, so the only way to reach it is through a Private Endpoint. The VMs connect to the database using a private IP address within the VNet, and DNS resolution is handled by a Private DNS Zone. This is a common pattern for securing databases in production.

### Storage

An Azure Storage Account is used for two things. First, there's a container called `application-code` that holds the zipped application code (uploaded by the CI/CD pipeline). The VMs download this code during startup using a SAS token. Second, there's a `product-images` container that stores product images uploaded through the app. This container is publicly accessible so images can be displayed on the frontend.

### Azure Functions and AI Integration

This is where it gets interesting. The project uses Azure Cognitive Services in two ways:

**1. Image Tagging (via Azure Function):** Whenever a new product image is uploaded to the Blob container, it triggers an Azure Function. The function reads the image, sends it to Azure Computer Vision API, and gets back a list of tags describing what's in the image (up to 8 tags). These tags are saved to the database automatically and used for product recommendations.

**2. Sentiment Analysis (via Backend API):** When users submit product reviews, the backend calls Azure Text Analytics API to analyze the sentiment. Each review gets a sentiment label (Positive, Neutral, Negative) and a score. This is stored alongside the review in the database.

The Azure Function runs on a Linux-based App Service Plan and is integrated into the VNet through VNet Integration. It also connects to Application Insights for logging and monitoring. The function code is deployed separately using Azure CLI during the pipeline run. There's retry logic built in—if the database hasn't been updated with the new product yet (race condition), the function retries automatically.

### Monitoring and Alerts

A Log Analytics Workspace collects logs from the various resources. Application Insights is attached to the Function App to track invocations, errors, and performance. There's also an Alert Action Group configured to send email notifications if CPU usage on any VMSS exceeds 70%. This gives visibility into what's happening without needing to constantly check the portal.

### CI/CD Pipeline (Jenkins)

The Jenkinsfile defines a multi-stage pipeline that handles everything from code validation to deployment and teardown. Depending on the selected mode, the pipeline can:
- Just validate and package the code (CI only)
- Deploy infrastructure and application (CD only)
- Do both end-to-end (Full CICD)
- Tear down everything (De-provision)

The pipeline uses a Service Principal for Azure authentication. Credentials like Terraform Cloud tokens, Azure client secrets, and app passwords are stored securely in Jenkins and injected as environment variables during the run. There's also a manual approval stage before any infrastructure changes are applied, so nothing gets deployed by accident.

After deployment, a smoke test runs to verify the application is actually responding. If everything looks good, a notification email is sent out.

### The Application (Brief Overview)

The application itself is a product catalog called ShopSphere. Users can browse products by category, view product details with AI-generated tags, read sentiment-analyzed reviews, and search. There's also a tag-based recommendation system that suggests similar products. Admins can log in to add, edit, or delete products. When a product image is uploaded, the AI tagging kicks in automatically.

It's built with Flask on both frontend and backend. The frontend renders pages using Jinja2 templates and proxies API calls to the backend. The backend exposes REST APIs for products, reviews, advertisements, and recommendations. There's also a `/health` endpoint used by the load balancer probes and the Jenkins smoke test.

The database has 5 tables: `products`, `reviews`, `product_tags`, `advertisements`, and `site_settings`. The app seeds sample data on first run if the tables are empty.

## Project Structure

```
├── Azure_Terraform/          # Infrastructure as Code
│   ├── main.tf               # Main config with 8 modules
│   ├── variables.tf          # All configurable parameters
│   ├── terraform.tfvars      # Variable values
│   ├── output.tf             # Terraform outputs (public IP)
│   └── modules/
│       ├── network_core/     # VNet, Subnets, NSGs, NAT Gateway
│       ├── compute_VM/       # VM Scale Sets + Autoscaling + cloud-init
│       ├── database/         # Azure SQL Server + Private Endpoint
│       ├── storage/          # Blob Storage + SAS tokens
│       ├── azure_ai/         # Cognitive Services
│       ├── azure_functions/  # Serverless function + VNet Integration
│       ├── network_ingress/  # Load Balancers (Public + Internal)
│       └── monitoring_and_alerts/  # Log Analytics, App Insights, Alerts
│
├── Azure_Function/           # Serverless AI tagging function
│   ├── host.json             # Function app configuration
│   ├── requirements.txt      # Python dependencies
│   └── image_tags_fn/        # Blob-triggered function code
│
├── backend/                  # Backend Flask API
│   ├── routes_api.py         # Public API endpoints
│   └── routes_admin.py       # Admin API endpoints
│
├── frontend/                 # Frontend Flask App
│   ├── routes_ui.py          # UI routes
│   ├── static/               # CSS, JS, images
│   └── templates/            # Jinja2 HTML templates
│
├── database/                 # Database layer
│   ├── db.py                 # Connection + helpers
│   └── seed_data.py          # Sample data seeding
│
├── common/                   # Shared utilities
│   └── utils.py              # AI helpers, image upload, formatters
│
├── Jenkinsfile               # CI/CD Pipeline (12 stages)
├── app.py                    # Flask application entry point
├── startup.sh                # Azure App Service startup script
├── requirements_frontend.txt # Frontend Python dependencies
├── requirements_backend.txt  # Backend Python dependencies
└── .gitignore                # Git ignore rules
```

## CI/CD Pipeline

The Jenkins pipeline has 4 modes:

| Mode | What It Does |
|------|--------------|
| Clone and Package (CI) | Validates code, creates zip artifacts |
| Deploy Infrastructure (CD) | Provisions Azure resources, deploys app |
| Full Pipeline (CICD) | Complete end-to-end deployment |
| De-provision | Tears down all infrastructure |

**Pre-build Action (All modes):**
- Clone code from SCM (Git repository)

---

### Clone and Package (CI)
1. Pre-build Validation (checks all required files exist)
2. Packaging (creates frontend and backend zip files)
3. Push to Artifacts (archives zips in Jenkins)

---

### Deploy Infrastructure and Application (CD)
1. Pull from Artifacts (retrieves zips from Jenkins)
2. Manual Approval (human gate before infra changes)
3. Creating Resources using Terraform (init, validate, plan, apply)
4. Azure Authentication using Service Principal
5. Uploading files to Azure Blob Container (code + product images)
6. Configuration and Deployment to Azure Function
7. Logout from Service Principal
8. Smoke Testing (health check + page content verification)

---

### Full Pipeline (CICD)
1. Pre-build Validation (checks all required files exist)
2. Packaging (creates frontend and backend zip files)
3. Push to Artifacts (archives zips in Jenkins)
4. Manual Approval (human gate before infra changes)
5. Creating Resources using Terraform (init, validate, plan, apply)
6. Azure Authentication using Service Principal
7. Uploading files to Azure Blob Container (code + product images)
8. Configuration and Deployment to Azure Function
9. Logout from Service Principal
10. Smoke Testing (health check + page content verification)

---

### De-provision Infrastructure and Application
1. Manual Approval
2. Removing the complete Infrastructure, Resources and Application (terraform destroy)

---

**Post-build Actions (All modes):**
- Email notification with build status and direct app link
- Workspace cleanup

## Azure Resources Created

- Resource Group
- Virtual Network with 4 Subnets (frontend, backend, database, function)
- Network Security Groups (subnet-level and VM-level)
- NAT Gateway + Public IP (for backend internet access)
- 2x VM Scale Sets (Frontend + Backend) with Autoscaling rules
- Public IP for Load Balancer (application entry point)
- Public Load Balancer with health probes and rules
- Internal Load Balancer with health probes and rules
- Azure SQL Server + Database
- Private Endpoint for SQL Server
- Private DNS Zone + VNet Link (database name resolution)
- Storage Account with 2 Blob containers (application-code, product-images)
- SAS Token for secure code download
- App Service Plan (Linux)
- Azure Function App (Blob trigger + VNet Integration)
- Azure Cognitive Services (Computer Vision + Text Analytics)
- Log Analytics Workspace
- Application Insights
- Monitor Metric Alerts (CPU threshold alerts)
- Alert Action Group (email notifications)

## Environment Variables

These are injected into VMs via cloud-init and written to `/etc/environment`.

**Common (Both Tiers):**

| Variable | Description |
|----------|-------------|
| `FLASK_SECRET` | Secret key for Flask session management |
| `AZURE_SQL_CONN` | ODBC connection string for Azure SQL |

**Frontend VMSS Only:**

| Variable | Description |
|----------|-------------|
| `ADMIN_USERNAME` | App admin login username |
| `ADMIN_PASSWORD` | App admin login password |
| `BACKEND_API_URL` | Internal load balancer URL to reach backend |

**Backend VMSS Only:**

| Variable | Description |
|----------|-------------|
| `AZURE_AI_ENDPOINT` | Azure Cognitive Services endpoint |
| `AZURE_AI_KEY` | Azure Cognitive Services API key |
| `AZURE_STORAGE_CONNECTION_STRING` | Blob storage connection string |
| `STORAGE_ACCOUNT_NAME` | Storage account name for image uploads |

## How to Deploy

### Prerequisites
1. **Azure Subscription** with permissions to create resources
2. **Azure Service Principal** with Contributor role
3. **Terraform Cloud Account** with a workspace configured
4. **Jenkins Server** with required plugins (Pipeline, Git, Credentials)

### Jenkins Credentials Setup
Add the following credentials in Jenkins (Manage Jenkins → Credentials):

| Credential ID | Type | Description |
|---------------|------|-------------|
| `tfc-token` | Secret text | Terraform Cloud API token |
| `AZURE_CLIENT_ID` | Secret text | Service Principal App ID |
| `AZURE_CLIENT_SECRET` | Secret text | Service Principal password |
| `AZURE_TENANT_ID` | Secret text | Azure AD Tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Secret text | Azure Subscription ID |
| `vm_password` | Secret text | Password for VM admin user |
| `db_password` | Secret text | Password for Azure SQL admin |
| `ShopSphere_App_Admin_Password` | Secret text | App admin panel password |

### Deployment Steps
1. **Fork/Clone the repository** to your Git server
2. **Configure Terraform Cloud** - Create workspace, link to VCS, set execution mode to "Local"
3. **Update `terraform.tfvars`** - Modify resource names, location, and other parameters as needed
4. **Create Jenkins Pipeline** - Point to your repository's Jenkinsfile
5. **Run the Pipeline** - Select "Full Pipeline (CICD)" mode
6. **Approve the deployment** - Click "Proceed" at the manual approval stage
7. **Access the App** - Use the public IP shown in Terraform output or email notification

## Quick Test

After deployment:
1. Open the public load balancer IP in browser
2. Browse products on homepage (filter by category ads)
3. Search for products using the search bar
4. Click on a product to view details and AI-generated tags
5. Check the "You might also like" section (tag-based recommendations)
6. Submit a review → Sentiment analysis labels it as Positive/Neutral/Negative
7. Login at `/admin-auth` with admin credentials
8. Add a new product with an image → AI tags are auto-generated within seconds
9. Edit or delete existing products from admin panel
10. Verify health endpoint: `http://<public-ip>/health` returns "OK"

## Tech Stack

| Category | Technology |
|----------|------------|
| **Cloud Platform** | Microsoft Azure |
| **Infrastructure as Code** | Terraform + Terraform Cloud |
| **CI/CD** | Jenkins |
| **Compute** | Azure VM Scale Sets (Ubuntu 22.04) |
| **Database** | Azure SQL Database |
| **Storage** | Azure Blob Storage |
| **Serverless** | Azure Functions (Python) |
| **AI Services** | Azure Computer Vision, Azure Text Analytics |
| **Monitoring** | Log Analytics, Application Insights |
| **Backend** | Python Flask + Gunicorn |
| **Frontend** | Jinja2 Templates, Bootstrap, JavaScript |
| **Networking** | VNet, NSG, NAT Gateway, Load Balancers, Private Endpoints |

## Author

| **Name** | Prajwal SM |
| **LinkedIn** | https://www.linkedin.com/in/prajwal-sm/ |
| **Email** | prajwalprajwal1999@gmail.com |
