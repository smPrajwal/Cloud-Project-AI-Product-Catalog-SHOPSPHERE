resource "azurerm_log_analytics_workspace" "ss_la_workspace" {
  name                = "ss-la-workspace"
  location            = var.default_loc
  resource_group_name = var.default_rg

  sku               = "PerGB2018"
  retention_in_days = 30
}

resource "azurerm_application_insights" "ss_appinsights" {
  name                = "ss-appinsights"
  location            = var.default_loc
  resource_group_name = var.default_rg

  application_type = "web"
  workspace_id     = azurerm_log_analytics_workspace.ss_la_workspace.id
}

resource "azurerm_monitor_action_group" "ss_ma_group" {
  name                = "ss-ma-group"
  resource_group_name = var.default_rg
  short_name          = "app-alerts"

  email_receiver {
    name          = "admin"
    email_address = "prajwalprajwal1999@gmail.com"
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