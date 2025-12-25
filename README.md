# Product Catalog Web App

A minimalist product catalog web application built for Azure 3-tier architecture demonstrations.

## Overview
This application provides a clean, responsive UI for browsing products, submitting reviews, and managing inventory. It includes stubs for Azure AI and Storage services to demonstrate cloud integration patterns without incurring costs during development.

## How to Run Locally

```bash
# Windows
run

# Linux / Mac
./run.sh
```

Access at: http://localhost:5000

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FLASK_SECRET` | Secret key for session management (default: dev-key). |
| `FLASK_DEBUG` | Set to `true` for debug mode. |
| `ADMIN_USERNAME` | Admin username (default: admin). |
| `ADMIN_PASSWORD` | Admin password (default: admin). |
| `USE_AZURE_BLOB` | Set to `true` to enable Azure Blob Storage. |
| `AZURE_STORAGE_CONNECTION_STRING` | Connection string for Azure Blob Storage. |
| `AZURE_SQL_CONN` | ODBC Connection string for Azure SQL (Overrides SQLite). |
| `TEXT_ANALYTICS_KEY` | Key for Azure AI Language Service (Sentiment stub). |
| `TEXT_ANALYTICS_ENDPOINT` | Endpoint for Azure AI Language Service. |
| `VISION_KEY` | Key for Azure Computer Vision (Tagging stub). |
| `VISION_ENDPOINT` | Endpoint for Azure Computer Vision. |

> **Note:** Cloud integrations are optional. Without Azure config, the app uses local SQLite and local file storage.
> **Note:** Azure Functions integration is planned for Phase-2 (not included).

## Smoke Test Checklist (5-Step)

1. **Start App**: Run `python app.py` -> Verify running on `0.0.0.0:5000`.
2. **Public View**: Open `http://localhost:5000` -> Verify products load.
3. **Admin Login**: Go to `/admin-auth` -> Log in with credentials (admin/admin).
4. **Ops Check**: Add a new product -> Upload an image -> Verify image appears.
5. **Clean Up**: Delete the test product -> Verify it disappears from list.


