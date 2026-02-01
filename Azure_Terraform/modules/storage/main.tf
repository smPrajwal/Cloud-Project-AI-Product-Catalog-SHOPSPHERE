resource "azurerm_storage_account" "main_sa" {
  name                            = var.sa_name
  resource_group_name             = var.default_rg
  location                        = var.default_loc
  account_tier                    = var.sa_account_tier
  account_replication_type        = var.sa_replication_type
  access_tier                     = var.sa_access_tier
  allow_nested_items_to_be_public = var.sa_allow_public_access
}

resource "azurerm_storage_container" "product_images" {
  name                  = "product-images"
  storage_account_id    = azurerm_storage_account.main_sa.id
  container_access_type = "blob"
}

resource "azurerm_storage_container" "application_code" {
  name                  = var.code_blob_container_name
  storage_account_id    = azurerm_storage_account.main_sa.id
  container_access_type = "private"
}

data "azurerm_storage_account_blob_container_sas" "code_sas" {
  connection_string = azurerm_storage_account.main_sa.primary_connection_string
  container_name    = azurerm_storage_container.application_code.name
  https_only        = true

  start  = "2024-01-01"
  expiry = "2030-01-01"

  permissions {
    read   = true
    add    = false
    create = false
    write  = false
    delete = false
    list   = false
  }
}