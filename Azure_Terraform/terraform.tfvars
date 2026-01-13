default_loc = "centralindia"

rg_name = "Project_ShopSphere"

sa_name = "shopsphereappsa123"

sa_account_tier = "Standard"

sa_replication_type = "LRS"

sa_access_tier = "Hot"

sa_allow_public_access = false

vnet_name = "ss_main_vnet"

vnet_cidr = "10.0.0.0/16"

vm_un = "prajwalsm"

vm_pwd = "P@$$w0rd1234"

subnet_details = {
  "public-fe" = {
    access              = "public"
    cidr                = "10.0.1.0/24"
    role                = "frontend"
    contains_vmss       = true
    sub_nsg_priority    = 100
    sub_nsg_source_cidr = "Internet"
    vm_nsg_priority     = 100
    vm_nsg_source_cidr  = "AzureLoadBalancer"
  }
  "private-be" = {
    access              = "private"
    cidr                = "10.0.2.0/24"
    role                = "backend"
    contains_vmss       = true
    sub_nsg_priority    = 100
    sub_nsg_source_cidr = "VirtualNetwork"
    vm_nsg_priority     = 100
    vm_nsg_source_cidr  = "10.0.1.0/24"
  }
  "private-db" = {
    access              = "private"
    cidr                = "10.0.3.0/24"
    role                = "db-endpoint"
    contains_vmss       = false
    sub_nsg_priority    = 100
    sub_nsg_source_cidr = "VirtualNetwork"
    vm_nsg_priority     = 100
    vm_nsg_source_cidr  = "10.0.2.0/24"
  }
}

