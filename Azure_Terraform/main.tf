terraform {
  required_version = "~> 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.57.0, < 5.0.0"
    }
  }
  cloud {
    organization = "Practice_and_Project"
    workspaces {
      name = "Azure_Cloud_Project"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

resource "azurerm_resource_group" "main_rg" {
  name     = var.rg_name
  location = var.default_loc
  tags = {
    Project = "ShopSphere"
  }
}

module "network_core" {
  source = "./modules/network_core"

  default_loc    = var.default_loc
  default_rg     = azurerm_resource_group.main_rg.name
  vnet_name      = var.vnet_name
  vnet_cidr      = var.vnet_cidr
  subnet_details = var.subnet_details
}

module "compute_VM" {
  source = "./modules/compute_VM"

  default_loc            = var.default_loc
  default_rg             = azurerm_resource_group.main_rg.name
  vm_un                  = var.vm_un
  vm_pwd                 = var.vm_pwd
  subnet_ids             = module.network_core.subnet_ids
  lb_backend_pool_ids    = module.network_ingress.lb_backend_pool_ids
  subnet_details         = var.subnet_details
  app_admin_un           = var.app_admin_un
  app_admin_pwd          = var.app_admin_pwd
  azure_sql_conn         = module.database.azure_sql_conn
  frontend_code_blob_url = var.frontend_code_blob_url
  backend_code_blob_url  = var.backend_code_blob_url
  vision_endpoint        = module.azure_ai.vision_endpoint
  vision_key             = module.azure_ai.vision_key
  storage_account        = module.storage.storage_account
  sas_token              = module.storage.sas_token
  backend_lb_private_ip  = module.network_ingress.backend_lb_private_ip
  vm_sku                 = var.vm_sku
  vm_os_publisher        = var.vm_os_publisher
  vm_os_offer            = var.vm_os_offer
  vm_os_sku              = var.vm_os_sku
  vm_os_version          = var.vm_os_version
  vmss_min_capacity      = var.vmss_min_capacity
  vmss_max_capacity      = var.vmss_max_capacity
  vmss_default_capacity  = var.vmss_default_capacity

  depends_on = [module.network_core]
}

module "database" {
  source = "./modules/database"

  default_loc     = var.default_loc
  default_rg      = azurerm_resource_group.main_rg.name
  db_un           = var.db_un
  db_pwd          = var.db_pwd
  vnet_id         = module.network_core.vnet_id
  subnet_ids      = module.network_core.subnet_ids
  sql_server_name = var.sql_server_name
  sql_db_name     = var.sql_db_name
  sql_version     = var.sql_version
  db_sku_name     = var.db_sku_name
  db_max_size_gb  = var.db_max_size_gb
}

module "storage" {
  source = "./modules/storage"

  default_loc            = var.default_loc
  default_rg             = azurerm_resource_group.main_rg.name
  sa_name                = var.sa_name
  sa_account_tier        = var.sa_account_tier
  sa_replication_type    = var.sa_replication_type
  sa_access_tier         = var.sa_access_tier
  sa_allow_public_access = var.sa_allow_public_access
}

module "azure_ai" {
  source = "./modules/azure_ai"

  default_loc = var.default_loc
  default_rg  = azurerm_resource_group.main_rg.name
  ai_name     = var.ai_name
  ai_sku      = var.ai_sku
}

module "azure_functions" {
  source = "./modules/azure_functions"

  default_loc                    = var.default_loc
  default_rg                     = azurerm_resource_group.main_rg.name
  azure_sql_conn                 = module.database.azure_sql_conn
  vision_endpoint                = module.azure_ai.vision_endpoint
  vision_key                     = module.azure_ai.vision_key
  storage_account                = module.storage.storage_account
  function_app_name              = var.function_app_name
  subnet_ids                     = module.network_core.subnet_ids
  func_plan_name                 = var.func_plan_name
  func_plan_sku                  = var.func_plan_sku
  func_python_version            = var.func_python_version
  app_insights_connection_string = module.monitoring_and_alerts.app_insights_connection_string
  func_service_plan_id           = var.func_service_plan_id
}

module "network_ingress" {
  source = "./modules/network_ingress"

  default_loc    = var.default_loc
  default_rg     = azurerm_resource_group.main_rg.name
  subnet_details = var.subnet_details
  subnet_ids     = module.network_core.subnet_ids
  lb_pip_name    = var.lb_pip_name
  lb_pip_sku     = var.lb_pip_sku
}

module "monitoring_and_alerts" {
  source = "./modules/monitoring_and_alerts"

  default_loc             = var.default_loc
  default_rg              = azurerm_resource_group.main_rg.name
  vmss_ids                = module.compute_VM.vmss_ids
  la_workspace_name       = var.la_workspace_name
  la_sku                  = var.la_sku
  la_retention            = var.la_retention
  app_insights_name       = var.app_insights_name
  alert_action_group_name = var.alert_action_group_name
  alert_email             = var.alert_email
}
