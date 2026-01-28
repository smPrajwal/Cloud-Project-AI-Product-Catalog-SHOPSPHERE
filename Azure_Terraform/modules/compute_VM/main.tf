resource "azurerm_network_security_group" "vm-nsg" {
  for_each = {
    for k, v in var.subnet_details : k => v if v.contains_vmss
  }

  name                = "${each.key}-vm-nsg"
  location            = var.default_loc
  resource_group_name = var.default_rg
}

resource "azurerm_network_security_rule" "vm-nsg-rule" {
  for_each = {
    for k, v in var.subnet_details : k => v if v.contains_vmss
  }

  name                        = "${each.key}-vm-nsg-rule"
  priority                    = each.value.vm_nsg_priority
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "8000"
  source_address_prefix       = each.value.vm_nsg_source_cidr
  destination_address_prefix  = "*"
  resource_group_name         = var.default_rg
  network_security_group_name = azurerm_network_security_group.vm-nsg[each.key].name
}

resource "random_password" "flask_secret" {
  length  = 64
  special = true
}

resource "azurerm_linux_virtual_machine_scale_set" "vmss" {
  for_each = {
    for k, v in var.subnet_details : k => v if v.contains_vmss
  }

  name                = "${each.key}-vmss"
  location            = var.default_loc
  resource_group_name = var.default_rg
  sku                 = "Standard_B2s_v2"
  instances           = 1
  upgrade_mode        = "Automatic"

  admin_username                  = var.vm_un
  admin_password                  = var.vm_pwd
  disable_password_authentication = false

  custom_data = base64encode(
    each.value.role == "frontend" ?
    templatefile("${path.module}/frontend-cloud-init.yaml", {
      flask_secret      = random_password.flask_secret.result
      admin_username    = var.app_admin_un
      admin_password    = var.app_admin_pwd
      azure_sql_conn    = var.azure_sql_conn
      frontend_blob_url = var.frontend_code_blob_url
      vm_user           = var.vm_un
      backend_lb_ip     = var.backend_lb_private_ip
    }) :
    templatefile("${path.module}/backend-cloud-init.yaml", {
      flask_secret        = random_password.flask_secret.result
      azure_sql_conn      = var.azure_sql_conn
      azure_ai_endpoint   = var.vision_endpoint
      azure_ai_key        = var.vision_key
      storage_conn_string  = var.storage_account.pa_key
      storage_account_name = var.storage_account.name
      backend_blob_url     = var.backend_code_blob_url
      vm_user              = var.vm_un
    })
  )

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  os_disk {
    storage_account_type = "Standard_LRS"
    caching              = "ReadWrite"
  }

  network_interface {
    name    = "nic"
    primary = true

    network_security_group_id = azurerm_network_security_group.vm-nsg[each.key].id

    ip_configuration {
      name      = "ipconfig"
      subnet_id = var.subnet_ids[each.key]

      load_balancer_backend_address_pool_ids = [
        var.lb_backend_pool_ids[each.key]
      ]
    }
  }
}

resource "azurerm_monitor_autoscale_setting" "vmss_autoscale" {
  for_each = azurerm_linux_virtual_machine_scale_set.vmss

  name                = "${each.key}-vmss-autoscale"
  location            = var.default_loc
  resource_group_name = var.default_rg
  target_resource_id  = each.value.id

  profile {
    name = "default"

    capacity {
      minimum = 1
      maximum = 3
      default = 1
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_resource_id = each.value.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 30
      }
      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_resource_id = each.value.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 30
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT5M"
      }
    }
  }
}
