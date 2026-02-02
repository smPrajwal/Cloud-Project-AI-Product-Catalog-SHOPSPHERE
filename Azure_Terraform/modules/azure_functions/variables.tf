variable "default_loc" {}
variable "default_rg" {}
variable "subnet_ids" {
  type = map(string)
}
variable "azure_sql_conn" {}
variable "vision_endpoint" {}
variable "vision_key" {
  sensitive = true
}
variable "function_app_name" {}

variable "storage_account" {
  type = object({
    name              = string
    pa_key            = string
    connection_string = string
  })
  sensitive = true
}