resource "azurerm_public_ip" "fe_lb_public_ip" {
  name                = "public-subnet-lb-pip"
  resource_group_name = var.default_rg
  location            = var.default_loc
  allocation_method   = "Static"
  sku = "Standard"
}

resource "azurerm_lb" "vmss_lb" {
  for_each = {
    for k, v in var.subnet_details: k => v if v.contains_vmss
  }

  name = "${each.key}-lb"
  location = var.default_loc
  resource_group_name = var.default_rg
  sku = "Standard"

  frontend_ip_configuration {
    name = "${each.key}-fe-ip"
    public_ip_address_id = each.value.access == "public" ? azurerm_public_ip.fe_lb_public_ip.id : null
    subnet_id = each.value.access == "private" ? var.subnet_ids[each.key] : null
    private_ip_address_allocation = each.value.access == "private" ? "Dynamic" : null
  }
}

resource "azurerm_lb_backend_address_pool" "lb_bap" {
  for_each = azurerm_lb.vmss_lb

  name = "${each.key}-bap"
  loadbalancer_id = each.value.id
}

resource "azurerm_lb_probe" "lb_probe" {
  for_each = azurerm_lb.vmss_lb

  name = "${each.key}-lb-probe"
  loadbalancer_id = each.value.id
  protocol = "Tcp"
  port = 8000
}

resource "azurerm_lb_rule" "lb_rule" {
  for_each = azurerm_lb.vmss_lb

  name = "${each.key}-lb-rule"
  loadbalancer_id = each.value.id
  protocol = "Tcp"
  frontend_port = 80
  backend_port = 8000
  frontend_ip_configuration_name = "${each.key}-fe-ip"
  backend_address_pool_ids = [ azurerm_lb_backend_address_pool.lb_bap[each.key].id ]
  probe_id = azurerm_lb_probe.lb_probe[each.key].id
}