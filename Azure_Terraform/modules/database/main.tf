resource "azurerm_mssql_server" "sql" {
  name                = var.sql_server_name
  resource_group_name = var.default_rg
  location            = var.default_loc
  version             = var.sql_version

  administrator_login          = var.db_un
  administrator_login_password = var.db_pwd

  public_network_access_enabled = false
}

resource "azurerm_mssql_database" "db" {
  name        = var.sql_db_name
  server_id   = azurerm_mssql_server.sql.id
  sku_name    = var.db_sku_name
  max_size_gb = var.db_max_size_gb
}

resource "azurerm_private_dns_zone" "db-dns-zone" {
  name                = "privatelink.database.windows.net"
  resource_group_name = var.default_rg
}

resource "azurerm_private_dns_zone_virtual_network_link" "dns-zone-vnet-link" {
  name                  = "dns-vnet-link"
  resource_group_name   = var.default_rg
  private_dns_zone_name = azurerm_private_dns_zone.db-dns-zone.name
  virtual_network_id    = var.vnet_id
}

resource "azurerm_private_endpoint" "db-endpoint" {
  name                = "db-endpoint"
  location            = var.default_loc
  resource_group_name = var.default_rg
  subnet_id           = var.subnet_ids["private-db"]

  private_service_connection {
    name                           = "sql-connection"
    private_connection_resource_id = azurerm_mssql_server.sql.id
    subresource_names              = ["sqlServer"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [azurerm_private_dns_zone.db-dns-zone.id]
  }
}
