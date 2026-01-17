output "vision_endpoint" {
  value = azurerm_cognitive_account.azure_ai.endpoint
}

output "vision_key" {
  value     = azurerm_cognitive_account.azure_ai.primary_access_key
  sensitive = true
}