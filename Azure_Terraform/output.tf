output "application_public_ip" {
  value = module.network_ingress.application_public_ip
}

output "application_port" {
  value = module.network_ingress.application_port
}