variable "default_loc" {}
variable "default_rg" {}
variable "db_un" {}
variable "db_pwd" {}
variable "vnet_id" {
  description = "This will hold the VNet ID"
  type        = string
}
variable "subnet_ids" {
  description = "This holds all the subnet IDs"
  type        = map(string)
}
variable "subnet_details" {
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