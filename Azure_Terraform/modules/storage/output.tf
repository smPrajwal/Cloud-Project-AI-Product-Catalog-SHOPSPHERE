output "storage_account" {
  value = {
    name   = azurerm_storage_account.main_sa.name
    pa_key = azurerm_storage_account.main_sa.primary_access_key
  }
}