# Product Catalog Web App

A minimalist product catalog web application built for Azure 3-tier architecture demonstrations.

## Overview
This application provides a clean, responsive UI for browsing products, submitting reviews, and managing inventory. It includes stubs for Azure AI and Storage services to demonstrate cloud integration patterns without incurring costs during development.

## How to Deploy to Azure
This application is designed to run on Azure App Service with Azure SQL Database.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FLASK_SECRET` | Secret key for session management. |
| `AZURE_SQL_CONN` | **Required.** ODBC Connection string for Azure SQL. |
| `USE_AZURE_BLOB` | Set to `true` to enable Azure Blob Storage. |
| `AZURE_STORAGE_CONNECTION_STRING` | Connection string for Azure Blob Storage. |
| `TEXT_ANALYTICS_KEY` | Key for Azure AI Language Service (Sentiment stub). |
| `TEXT_ANALYTICS_ENDPOINT` | Endpoint for Azure AI Language Service. |
| `VISION_KEY` | Key for Azure Computer Vision (Tagging stub). |
| `VISION_ENDPOINT` | Endpoint for Azure Computer Vision. |
| `ADMIN_USERNAME` | Admin username (default: admin). |
| `ADMIN_PASSWORD` | Admin password (default: admin). |

> **Note:** This application requires Azure Services (SQL, Blob Storage) to function. Local SQLite fallbacks have been removed.

## Smoke Test Checklist (Azure)

1. **Deploy**: Push changes to Azure Repos / GitHub.
2. **Public View**: Open your Azure Web App URL -> Verify products load from Azure SQL.
3. **Admin Login**: Go to `/admin-auth` -> Log in.
4. **Ops Check**: Add a new product -> Upload an image -> Verify image appears (via Blob Storage).


