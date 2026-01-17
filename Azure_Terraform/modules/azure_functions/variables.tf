variable "default_loc" {}
variable "default_rg" {}
variable "azure_sql_conn" {}
variable "vision_endpoint" {}
variable "vision_key" {}
variable "storage_account" {
  type = object({
    name   = string
    pa_key = string
  })
}