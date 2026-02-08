default_loc = "centralindia"
rg_name     = "Project_ShopSphere"

sa_name                = "shopsphereapplicationsa"
sa_account_tier        = "Standard"
sa_replication_type    = "LRS"
sa_access_tier         = "Hot"
sa_allow_public_access = true

vnet_name = "ss_main_vnet"
vnet_cidr = "10.0.0.0/16"

lb_pip_name = "public-subnet-lb-pip"
lb_pip_sku  = "Standard"

vm_un                 = "prajwalsm"
vm_sku                = "Standard_B2s_v2"
vm_os_publisher       = "Canonical"
vm_os_offer           = "0001-com-ubuntu-server-jammy"
vm_os_sku             = "22_04-lts"
vm_os_version         = "latest"
vmss_min_capacity     = 1
vmss_max_capacity     = 3
vmss_default_capacity = 1

db_un           = "prajwalsm"
sql_server_name = "shopsphereapp-sql-db"
sql_db_name     = "sql-db"
sql_version     = "12.0"
db_sku_name     = "Basic"
db_max_size_gb  = 2

app_admin_un        = "admin"
function_app_name   = "azure-ai-function-app-ss"
func_plan_name      = "azure-function-service-plan"
func_plan_sku       = "B1"
func_python_version = "3.12"

ai_name = "azure-ai-ss"
ai_sku  = "S0"

la_workspace_name       = "ss-la-workspace"
la_sku                  = "PerGB2018"
la_retention            = 30
app_insights_name       = "ss-appinsights"
alert_action_group_name = "ss-ma-group"
alert_email             = "prajwalprajwal1999@gmail.com"

subnet_details = {
  "public-fe" = {
    access              = "public"
    cidr                = "10.0.1.0/24"
    role                = "frontend"
    contains_vmss       = true
    sub_nsg_priority    = 100
    sub_nsg_source_cidr = "Internet"
    vm_nsg_priority     = 100
    vm_nsg_source_cidr  = "Internet"
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
    vm_nsg_priority     = null
    vm_nsg_source_cidr  = null
  }
  "private-func" = {
    access              = "private"
    cidr                = "10.0.4.0/24"
    role                = "function"
    contains_vmss       = false
    sub_nsg_priority    = 100
    sub_nsg_source_cidr = "*"
    vm_nsg_priority     = null
    vm_nsg_source_cidr  = null
  }
}
