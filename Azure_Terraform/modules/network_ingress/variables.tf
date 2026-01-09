variable "default_loc" {}
variable "default_rg" {}
variable "subnet_ids" {
  description = "This holds all the subnet IDs"
  type = map(string)
}
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