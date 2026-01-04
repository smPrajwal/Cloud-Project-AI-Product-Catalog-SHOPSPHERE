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

  }
}

locals {
  default_rg = resource.azurerm_resource_group.main_rg.name
}

resource "azurerm_resource_group" "main_rg" {
  name     = var.rg_name
  location = var.default_loc
  tags = {
    Project = "ShopSphere"
  }
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