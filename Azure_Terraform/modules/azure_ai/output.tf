output "vision_endpoint" {
  description = "This represents the Azure AI Vision Endpoint"
  value       = azurerm_cognitive_account.azure_ai.endpoint
}

output "vision_key" {
  description = "This represents the Azure AI Vision Key"
  value       = azurerm_cognitive_account.azure_ai.primary_access_key
  sensitive   = true
}