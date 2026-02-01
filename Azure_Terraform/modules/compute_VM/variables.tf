variable "default_loc" {}
variable "default_rg" {}
variable "vm_un" {}
variable "azure_sql_conn" {}
variable "app_admin_un" {}
variable "frontend_code_blob_url" {}
variable "backend_code_blob_url" {}
variable "vision_endpoint" {}
variable "backend_lb_private_ip" {}
variable "vision_key" {
  sensitive = true
}
variable "vm_pwd" {
  sensitive = true
}
variable "app_admin_pwd" {
  sensitive = true
}
variable "subnet_ids" {
  description = "This holds all the subnet IDs"
  type        = map(string)
}
variable "lb_backend_pool_ids" {
  description = "This holds all the backend pool IDs"
  type        = map(string)
}
variable "storage_account" {
  type = object({
    name              = string
    pa_key            = string
    connection_string = string
  })
  sensitive = true
}
variable "sas_token" {
  sensitive = true
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