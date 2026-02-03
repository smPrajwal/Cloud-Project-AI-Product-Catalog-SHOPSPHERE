output "azure_sql_conn" {
  value     = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.sql.fully_qualified_domain_name},1433;Database=${azurerm_mssql_database.db.name};Uid=${var.db_un};Pwd=${var.db_pwd};Encrypt=yes;"
  sensitive = true
}
