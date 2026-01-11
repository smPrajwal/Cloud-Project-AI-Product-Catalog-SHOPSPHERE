variable "default_loc" {}
variable "default_rg" {}
variable "vnet_name" {}
variable "vnet_cidr" {}
variable "subnet_details" {
  type = map(object({
    access = string
    cidr = string
    role = string
    contains_vmss = bool
    sub_nsg_priority = number
    sub_nsg_source_cidr = string
    vm_nsg_priority    = number
    vm_nsg_source_cidr = string
  }))
}