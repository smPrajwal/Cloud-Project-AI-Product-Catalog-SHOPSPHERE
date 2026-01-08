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
    nsg_priority = number
    nsg_port = string
    nsg_source_cidr = string
  }))
}
locals {
  default_vnet = resource.azurerm_virtual_network.vnet.name
}
