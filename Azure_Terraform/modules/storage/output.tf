output "sas_token" {
  description = "This represents the SAS Token of the Application code Blob container"
  value     = data.azurerm_storage_account_blob_container_sas.code_sas.sas
  sensitive = true
}
output "storage_account" {
  description = "This holds some of the useful attribute values of the Storage Account"
  value = {
    name              = azurerm_storage_account.main_sa.name
    pa_key            = azurerm_storage_account.main_sa.primary_access_key
    connection_string = azurerm_storage_account.main_sa.primary_connection_string
  }
  sensitive = true
}