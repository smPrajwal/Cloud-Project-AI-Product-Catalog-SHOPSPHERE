variable "default_loc" {}
variable "default_rg" {}
variable "la_workspace_name" {}
variable "la_sku" {}
variable "la_retention" {}
variable "app_insights_name" {}
variable "alert_action_group_name" {}
variable "alert_email" {}
variable "vmss_ids" {
  description = "This represents the VMSS IDs"
  type        = map(string)
}
