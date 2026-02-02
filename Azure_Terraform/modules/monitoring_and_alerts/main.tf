resource "azurerm_log_analytics_workspace" "ss_la_workspace" {
  name                = var.la_workspace_name
  location            = var.default_loc
  resource_group_name = var.default_rg

  sku               = var.la_sku
  retention_in_days = var.la_retention
}

resource "azurerm_application_insights" "ss_appinsights" {
  name                = var.app_insights_name
  location            = var.default_loc
  resource_group_name = var.default_rg

  application_type = "web"
  workspace_id     = azurerm_log_analytics_workspace.ss_la_workspace.id
}

resource "azurerm_monitor_action_group" "ss_ma_group" {
  name                = var.alert_action_group_name
  resource_group_name = var.default_rg
  short_name          = "app-alerts"

  email_receiver {
    name          = "admin"
    email_address = var.alert_email
  }
}

resource "azurerm_monitor_metric_alert" "ss_mm_alert" {
  for_each = var.vmss_ids

  name                = "ss-${each.key}-vmss-mm-alert"
  resource_group_name = var.default_rg
  scopes              = [each.value]

  description = "CPU usage too high on ${each.key} VMSS"
  severity    = 3
  frequency   = "PT1M"
  window_size = "PT5M"

  criteria {
    metric_namespace = "Microsoft.Compute/virtualMachineScaleSets"
    metric_name      = "Percentage CPU"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 70
  }

  action {
    action_group_id = azurerm_monitor_action_group.ss_ma_group.id
  }
}
