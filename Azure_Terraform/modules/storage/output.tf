output "storage_account" {
  value = {
    name   = azurerm_storage_account.main_sa.name
    pa_key = azurerm_storage_account.main_sa.primary_access_key
  }
  sensitive = true
}

output "frontend_code_blob_url" {
  value = azurerm_storage_blob.frontend_zip.url
}

output "backend_code_blob_url" {
  value = azurerm_storage_blob.backend_zip.url
}