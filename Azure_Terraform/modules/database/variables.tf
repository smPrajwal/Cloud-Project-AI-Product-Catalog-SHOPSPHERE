variable "default_loc" {}
variable "default_rg" {}
variable "db_un" {}
variable "db_pwd" {
  sensitive = true
}
variable "vnet_id" {
  description = "This will hold the VNet ID"
  type        = string
}
variable "subnet_ids" {
  description = "This holds all the subnet IDs"
  type        = map(string)
}