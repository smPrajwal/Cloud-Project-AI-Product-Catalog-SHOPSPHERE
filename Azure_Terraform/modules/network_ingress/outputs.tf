output "lb_backend_pool_ids" {
  description = "This holds all the backend pool IDs"
  value = {
    for k, v in azurerm_lb_backend_address_pool.lb_bap : k => v.id
  }
}

output "application_public_ip" {
  description = "This represents the Public IP of the frontend Load Balancer"
  value = azurerm_public_ip.fe_lb_public_ip.ip_address
}

output "backend_lb_private_ip" {
  description = "This represents the Private IP of the backend Load Balancer"
  value = azurerm_lb.vmss_lb["private-be"].frontend_ip_configuration[0].private_ip_address
}
