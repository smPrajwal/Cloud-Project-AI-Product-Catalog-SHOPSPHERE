variable "default_loc" {}
variable "default_rg" {}
variable "azure_sql_conn" {}
variable "vision_endpoint" {}
variable "vision_key" {}
variable "function_app_name" {}
variable "application_insights_connection_string" {
  description = "This represents the Application Insights Connection string"
  type        = string
}
variable "storage_account" {
  type = object({
    name   = string
    pa_key = string
  })
}