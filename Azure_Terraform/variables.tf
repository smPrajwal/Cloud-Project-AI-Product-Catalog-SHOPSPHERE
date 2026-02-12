variable "default_loc" {
  description = "This represents the default location"
  default     = "centralindia"
  type        = string
}

variable "rg_name" {
  description = "This represents the default resource group name"
  default     = "Project_ShopSphere"
  type        = string
}

variable "sa_name" {
  description = "This represents the default storage account name"
  default     = "shopspheresa"
  type        = string
}

variable "sa_account_tier" {
  description = "This represents the storage account tier"
  default     = "Standard"
  type        = string
}

variable "sa_replication_type" {
  description = "This represents the storage account replication type"
  default     = "LRS"
  type        = string
}

variable "sa_access_tier" {
  description = "This represents the storage account access tier"
  default     = "Hot"
  type        = string
}

variable "sa_allow_public_access" {
  description = "This represents the storage account parameter to allow the nested items to be public or not"
  default     = false
  type        = bool
}

variable "vnet_name" {
  description = "This represents the VNet name"
  default     = "ss_main_vnet"
  type        = string
}

variable "vnet_cidr" {
  description = "This represents the VNet CIDR"
  default     = "10.0.0.0/16"
  type        = string
}

variable "vm_un" {
  description = "This will hold the username of VMs"
  type        = string
}

variable "vm_pwd" {
  description = "This will hold the password of VMs"
  type        = string
  sensitive   = true
}

variable "db_un" {
  description = "This will hold the username of SQL Server"
  type        = string
}

variable "db_pwd" {
  description = "This will hold the password of SQL Server"
  type        = string
  sensitive   = true
}

variable "function_app_name" {
  description = "This represents the default Azure Function App name"
  default     = "azure-ai-function-app"
  type        = string
}

variable "app_admin_un" {
  description = "This will hold the username of ShopSphere Application Admin"
  type        = string
}

variable "app_admin_pwd" {
  description = "This will hold the password of ShopSphere Application Admin"
  type        = string
  sensitive   = true
}

variable "frontend_code_blob_url" {
  description = "This represents the Frontend Code Blob URL"
  default     = "https://shopsphereappsa.blob.core.windows.net/application-code/frontend/project1_shopsphere_frontend.zip"
  type        = string
}

variable "backend_code_blob_url" {
  description = "This represents the Backend Code Blob URL"
  default     = "https://shopsphereappsa.blob.core.windows.net/application-code/backend/project1_shopsphere_backend.zip"
  type        = string
}

variable "subnet_details" {
  description = "This contains all the necessary details related to the subnet and all are mandatory fields"
  type = map(object({
    access              = string
    cidr                = string
    role                = string
    contains_vmss       = bool
    sub_nsg_priority    = number
    sub_nsg_source_cidr = string
    vm_nsg_priority     = number
    vm_nsg_source_cidr  = string
  }))
}

variable "vm_sku" {
  description = "The SKU (Size) of the Virtual Machines"
  default     = "Standard_B2pls_v2"
  type        = string
}

variable "vm_os_publisher" {
  description = "The Publisher of the OS Image"
  default     = "Canonical"
  type        = string
}

variable "vm_os_offer" {
  description = "The Offer of the OS Image"
  default     = "0001-com-ubuntu-server-jammy"
  type        = string
}

variable "vm_os_sku" {
  description = "The SKU of the OS Image"
  default     = "Standard_B2ts_v2"
  type        = string
}

variable "vm_os_version" {
  description = "The Version of the OS Image"
  default     = "latest"
  type        = string
}

variable "vmss_min_capacity" {
  description = "Minimum number of instances in VMSS"
  default     = 1
  type        = number
}

variable "vmss_max_capacity" {
  description = "Maximum number of instances in VMSS"
  default     = 3
  type        = number
}

variable "vmss_default_capacity" {
  description = "Default number of instances in VMSS"
  default     = 1
  type        = number
}

variable "sql_server_name" {
  description = "Name of the Azure SQL Server"
  default     = "shopsphere-sql-db"
  type        = string
}

variable "sql_db_name" {
  description = "Name of the Azure SQL Database"
  default     = "sql-db"
  type        = string
}

variable "db_sku_name" {
  description = "SKU Name for the SQL Database"
  default     = "Basic"
  type        = string
}

variable "db_max_size_gb" {
  description = "Max Size in GB for the SQL Database"
  default     = 2
  type        = number
}

variable "ai_name" {
  description = "Name of the Azure AI Service"
  default     = "azure-ai"
  type        = string
}

variable "ai_sku" {
  description = "SKU for the Azure AI Service"
  default     = "S0"
  type        = string
}

variable "func_plan_name" {
  description = "Name of the App Service Plan for Azure Functions"
  default     = "azure-function-service-plan"
  type        = string
}

variable "func_plan_sku" {
  description = "SKU for the Function App Service Plan"
  default     = "B1"
  type        = string
}

variable "func_python_version" {
  description = "Python Version for the Function App"
  default     = "3.12"
  type        = string
}

variable "func_service_plan_id" {
  description = "App Service Plan ID for Azure Function"
  type        = string
}

variable "lb_pip_name" {
  description = "Name of the Public IP for Load Balancer"
  default     = "public-subnet-lb-pip"
  type        = string
}

variable "lb_pip_sku" {
  description = "SKU for the Load Balancer Public IP"
  default     = "Standard"
  type        = string
}

variable "la_workspace_name" {
  description = "Name of the Log Analytics Workspace"
  default     = "ss-la-workspace"
  type        = string
}

variable "la_sku" {
  description = "SKU for Log Analytics Workspace"
  default     = "PerGB2018"
  type        = string
}

variable "la_retention" {
  description = "Retention in days for Log Analytics"
  default     = 30
  type        = number
}

variable "app_insights_name" {
  description = "Name of the Application Insights resource"
  default     = "ss-appinsights"
  type        = string
}

variable "alert_action_group_name" {
  description = "Name of the Monitor Action Group"
  default     = "ss-ma-group"
  type        = string
}

variable "alert_email" {
  description = "Email address for Alerts"
  default     = "prajwalprajwal1999@gmail.com"
  type        = string
}
