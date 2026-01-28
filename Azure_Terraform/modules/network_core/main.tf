resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  address_space       = [var.vnet_cidr]
  location            = var.default_loc
  resource_group_name = var.default_rg
}

resource "azurerm_subnet" "subnet" {
  for_each = var.subnet_details

  name                 = "subnet-${each.key}"
  resource_group_name  = var.default_rg
  virtual_network_name = local.default_vnet
  address_prefixes     = [each.value.cidr]
}

resource "azurerm_network_security_group" "subnet-nsg" {
  for_each            = var.subnet_details

  name                = "${each.key}-subnet-nsg"
  location            = var.default_loc
  resource_group_name = var.default_rg
}

resource "azurerm_network_security_rule" "subnet-nsg-rule" {
  for_each = var.subnet_details

  name                        = "${each.key}-subnet-nsg-rule"
  priority                    = each.value.sub_nsg_priority
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefixes     = [each.value.sub_nsg_source_cidr, "AzureLoadBalancer"]
  destination_address_prefix  = "*"
  resource_group_name         = var.default_rg
  network_security_group_name = azurerm_network_security_group.subnet-nsg[each.key].name
}


resource "azurerm_subnet_network_security_group_association" "subnet-nsg-assoc" {
  for_each                  = var.subnet_details
  subnet_id                 = azurerm_subnet.subnet[each.key].id
  network_security_group_id = azurerm_network_security_group.subnet-nsg[each.key].id
}

# --- Simple NAT Gateway for Internet Access ---
resource "azurerm_public_ip" "nat_gw_pip" {
  name                = "nat-gateway-public-ip"
  location            = var.default_loc
  resource_group_name = var.default_rg
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_nat_gateway" "nat_gw" {
  name                = "main-nat-gateway"
  location            = var.default_loc
  resource_group_name = var.default_rg
  sku_name            = "Standard"
}

resource "azurerm_nat_gateway_public_ip_association" "nat_gw_ip_assoc" {
  nat_gateway_id       = azurerm_nat_gateway.nat_gw.id
  public_ip_address_id = azurerm_public_ip.nat_gw_pip.id
}

resource "azurerm_subnet_nat_gateway_association" "subnet_nat_assoc" {
  for_each       = {
    for k, v in var.subnet_details : k => v if v.role == "backend"
  }
  subnet_id      = azurerm_subnet.subnet[each.key].id
  nat_gateway_id = azurerm_nat_gateway.nat_gw.id
}
