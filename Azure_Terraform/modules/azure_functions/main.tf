data "azurerm_service_plan" "existing" {
  name                = var.func_plan_name
  resource_group_name = var.static_resource_rg
}

resource "azurerm_linux_function_app" "azure_ai_function_app" {
  name                = var.function_app_name
  location            = var.default_loc
  resource_group_name = var.default_rg

  service_plan_id = data.azurerm_service_plan.existing.id

  storage_account_name       = var.storage_account.name
  storage_account_access_key = var.storage_account.pa_key

  site_config {
    application_stack {
      python_version = var.func_python_version
    }
    always_on = true
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME              = "python"
    APPLICATIONINSIGHTS_CONNECTION_STRING = var.app_insights_connection_string
    ENABLE_ORYX_BUILD                     = "true"
    SCM_DO_BUILD_DURING_DEPLOYMENT        = "true"

    AZURE_SQL_CONN  = var.azure_sql_conn
    VISION_ENDPOINT = var.vision_endpoint
    VISION_KEY      = var.vision_key
  }
}

resource "azurerm_app_service_virtual_network_swift_connection" "func_vnet_integration" {
  app_service_id = azurerm_linux_function_app.azure_ai_function_app.id
  subnet_id      = var.subnet_ids["private-func"]
}
