output "app_insights_connection_string" {
  value     = azurerm_application_insights.ss_appinsights.connection_string
  sensitive = true
}
