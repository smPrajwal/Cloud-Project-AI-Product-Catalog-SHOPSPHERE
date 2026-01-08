resource "azurerm_virtual_network" "vnet" {
  name = var.vnet_name
  address_space = [var.vnet_cidr]
  location = var.default_loc
  resource_group_name = var.default_rg
}

resource "azurerm_subnet" "subnet" {
  for_each = var.subnet_details

  name = "subnet-${each.key}"
  resource_group_name = var.default_rg
  virtual_network_name = local.default_vnet
  address_prefixes = [each.value.cidr]
}

resource "azurerm_network_security_group" "nsg" {
  for_each = var.subnet_details
  name = "${each.key}-nsg"
  location = var.default_loc
  resource_group_name = var.default_rg
}

resource "azurerm_network_security_rule" "inbound" {
  for_each = var.subnet_details

  name = "${each.key}-nsg-rule"
  priority = each.value.nsg_priority
  direction = "Inbound"
  access = "Allow"
  protocol = "Tcp"
  source_port_range = "*"
  destination_port_range = each.value.nsg_port
  source_address_prefix = each.value.nsg_source_cidr
  destination_address_prefix = "*"
  resource_group_name = var.default_rg
  network_security_group_name = azurerm_network_security_group.nsg[each.key].name
}

resource "azurerm_subnet_network_security_group_association" "subnet-nsg-assoc" {
  for_each = var.subnet_details
  subnet_id = azurerm_subnet.subnet[each.key].id
  network_security_group_id = azurerm_network_security_group.nsg[each.key].id
}