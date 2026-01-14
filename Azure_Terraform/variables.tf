variable "default_loc" {
  description = "This represents the default location"
  default     = "South India"
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
}

variable "db_un" {
  description = "This will hold the username of SQL Server"
  type        = string
}

variable "db_pwd" {
  description = "This will hold the password of SQL Server"
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