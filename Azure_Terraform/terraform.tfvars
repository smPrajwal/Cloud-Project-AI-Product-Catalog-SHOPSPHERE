default_loc = "South India"

rg_name = "Project_ShopSphere"

sa_name = "shopsphereappsa"

sa_account_tier = "Standard"

sa_replication_type = "LRS"

sa_access_tier = "Hot"

sa_allow_public_access = false

vnet_name = "ss_main_vnet"

vnet_cidr = "10.0.0.0/16"

subnet_details = {
  "public-fe" = {
    access          = "public"
    cidr            = "10.0.1.0/24"
    role            = "frontend"
    contains_vmss   = true
    nsg_priority    = 100
    nsg_port        = "8000"
    nsg_source_cidr = "*"
  }
  "private-be" = {
    access          = "private"
    cidr            = "10.0.2.0/24"
    role            = "backend"
    contains_vmss   = true
    nsg_priority    = 100
    nsg_port        = "8000"
    nsg_source_cidr = "10.0.1.0/24"
  }
  "private-db" = {
    access          = "private"
    cidr            = "10.0.3.0/24"
    role            = "db-endpoint"
    contains_vmss   = false
    nsg_priority    = 100
    nsg_port        = "1433"
    nsg_source_cidr = "10.0.2.0/24"
  }
}

