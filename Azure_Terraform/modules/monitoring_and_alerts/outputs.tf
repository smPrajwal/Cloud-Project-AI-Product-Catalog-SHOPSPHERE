output "app_insights_connection_string" {
  description = "This represents the Application Insights Connection String"
  value       = azurerm_application_insights.ss_appinsights.connection_string
  sensitive   = true
}
