output "vmss_ids" {
  value = {
    for k, v in azurerm_linux_virtual_machine_scale_set.vmss : k => v.id
  }
}