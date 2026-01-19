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

module "network_ingress" {
  source = "./modules/network_ingress"

  default_loc    = var.default_loc
  default_rg     = azurerm_resource_group.main_rg.name
  subnet_details = var.subnet_details
  subnet_ids     = module.network_core.subnet_ids
}

module "compute_VM" {
  source = "./modules/compute_VM"

  default_loc         = var.default_loc
  default_rg          = azurerm_resource_group.main_rg.name
  vm_un               = var.vm_un
  vm_pwd              = var.vm_pwd
  subnet_ids          = module.network_core.subnet_ids
  lb_backend_pool_ids = module.network_ingress.lb_backend_pool_ids
  subnet_details      = var.subnet_details
}

module "database" {
  source = "./modules/database"

  default_loc    = var.default_loc
  default_rg     = azurerm_resource_group.main_rg.name
  db_un          = var.db_un
  db_pwd         = var.db_pwd
  vnet_id        = module.network_core.vnet_id
  subnet_ids     = module.network_core.subnet_ids
  subnet_details = var.subnet_details
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
}

module "azure_functions" {
  source = "./modules/azure_functions"

  default_loc                            = var.default_loc
  default_rg                             = azurerm_resource_group.main_rg.name
  azure_sql_conn                         = module.database.azure_sql_conn
  vision_endpoint                        = module.azure_ai.vision_endpoint
  vision_key                             = module.azure_ai.vision_key
  storage_account                        = module.storage.storage_account
  application_insights_connection_string = module.monitoring_and_alerts.application_insights_connection_string
}

module "monitoring_and_alerts" {
  source = "./modules/monitoring_and_alerts"

  default_loc = var.default_loc
  default_rg  = azurerm_resource_group.main_rg.name
  vmss_ids    = module.compute_VM.vmss_ids
}