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

locals {
  default_rg = azurerm_resource_group.main_rg.name
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
  default_rg     = local.default_rg
  vnet_name      = var.vnet_name
  vnet_cidr      = var.vnet_cidr
  subnet_details = var.subnet_details

  depends_on = [azurerm_resource_group.main_rg]
}

module "network_ingress" {
  source = "./modules/network_ingress"

  default_loc    = var.default_loc
  default_rg     = local.default_rg
  subnet_details = var.subnet_details
  subnet_ids     = module.network_core.subnet_ids

  depends_on = [
    azurerm_resource_group.main_rg,
    module.network_core
  ]
}

module "compute_VM" {
  source = "./modules/compute_VM"

  default_loc         = var.default_loc
  default_rg          = local.default_rg
  vm_un               = var.vm_un
  vm_pwd              = var.vm_pwd
  subnet_ids          = module.network_core.subnet_ids
  lb_backend_pool_ids = module.network_ingress.lb_backend_pool_ids
  subnet_details      = var.subnet_details

  depends_on = [
    module.network_core,
    module.network_ingress
  ]
}

resource "azurerm_storage_account" "main_sa" {
  name                            = var.sa_name
  resource_group_name             = local.default_rg
  location                        = var.default_loc
  account_tier                    = var.sa_account_tier
  account_replication_type        = var.sa_replication_type
  access_tier                     = var.sa_access_tier
  allow_nested_items_to_be_public = var.sa_allow_public_access
  tags = {
    project    = "ShopSphere"
    managed_by = "terraform"
  }
}