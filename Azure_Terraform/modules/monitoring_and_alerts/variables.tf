variable "default_loc" {}
variable "default_rg" {}
variable "vmss_ids" {
  description = "This represents the VMSS IDs"
  type        = map(string)
}