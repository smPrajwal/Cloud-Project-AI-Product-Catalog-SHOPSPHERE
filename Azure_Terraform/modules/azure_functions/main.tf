resource "azurerm_service_plan" "azure_function_service_plan" {
  name                = "azure-function-service-plan"
  location            = var.default_loc
  resource_group_name = var.default_rg

  os_type  = "Linux"
  sku_name = "Y1"
}

resource "azurerm_linux_function_app" "azure_ai_function_app" {
  name                = "azure-ai-function-app"
  location            = var.default_loc
  resource_group_name = var.default_rg

  service_plan_id = azurerm_service_plan.azure_function_service_plan.id

  storage_account_name       = var.storage_account.name
  storage_account_access_key = var.storage_account.pa_key

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"

    APPLICATIONINSIGHTS_CONNECTION_STRING = var.application_insights_connection_string
    AZURE_SQL_CONN                        = var.azure_sql_conn
    VISION_ENDPOINT                       = var.vision_endpoint
    VISION_KEY                            = var.vision_key
  }
}