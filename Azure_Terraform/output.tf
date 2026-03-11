output "application_public_ip" {
  description = "This represents the Public IP of the Frontend Load Balancer (Application URL)"
  value = module.network_ingress.application_public_ip
}