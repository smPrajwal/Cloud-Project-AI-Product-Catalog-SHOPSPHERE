output "subnet_ids" {
  description = "This holds all the subnet IDs"
  value = {
    for k, v in azurerm_subnet.subnet : k => v.id
  }
}

output "vnet_id" {
  description = "This will hold the VNet ID"
  value       = azurerm_virtual_network.vnet.id
}