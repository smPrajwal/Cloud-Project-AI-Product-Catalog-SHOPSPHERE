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
variable "func_plan_name" {}
variable "func_plan_sku" {}
variable "func_service_plan_id" {}
variable "func_python_version" {}
variable "storage_account" {
  type = object({
    name              = string
    pa_key            = string
    connection_string = string
  })
  sensitive = true
}

variable "app_insights_connection_string" {
  sensitive = true
}
