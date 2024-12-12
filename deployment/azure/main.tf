terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "pis_rg" {
  name     = var.rg_name
  location = "westeurope"
}

resource "azurerm_public_ip" "ci_cd_ip" {
  name                = var.ci_cd_vm_public_ip_name
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
  allocation_method   = "Static"
}

resource "azurerm_public_ip" "deployment_ip" {
  name                = var.deployment_vm_public_ip_name
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
  allocation_method   = "Static"
}

resource "azurerm_virtual_network" "pis_vnet" {
  name                = var.vnet_name
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
  address_space       = var.vnet_address_space
}

resource "azurerm_network_security_group" "pis_nsg" {
  name                = var.nsg_name
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
}

resource "azurerm_network_security_rule" "name" {
  for_each = { for rule in var.nsg_rules : rule.name => rule }

  name                        = each.value.name
  priority                    = each.value.priority
  direction                   = each.value.direction
  access                      = each.value.access
  protocol                    = each.value.protocol
  source_port_range           = each.value.source_port_range
  destination_port_range      = each.value.destination_port_range
  source_address_prefix       = each.value.source_address_prefix
  destination_address_prefix  = each.value.destination_address_prefix
  network_security_group_name = azurerm_network_security_group.pis_nsg.name
  resource_group_name         = azurerm_resource_group.pis_rg.name
}

resource "azurerm_subnet" "pis_subnet" {
  name                 = var.subnet_name
  resource_group_name  = azurerm_resource_group.pis_rg.name
  virtual_network_name = azurerm_virtual_network.pis_vnet.name
  address_prefixes     = var.vnet_address_space
}

resource "azurerm_network_interface" "ci_cd_nic" {
  name                = var.ci_cd_vm_nic_name
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name

  ip_configuration {
    name                          = var.ci_cd_vm_nic_ip_conf_name
    subnet_id                     = azurerm_subnet.pis_subnet.id
    private_ip_address_allocation = "Static"
    private_ip_address            = var.ci_cd_vm_nic_ip_conf_address
    public_ip_address_id          = azurerm_public_ip.ci_cd_ip.id
  }
}

resource "azurerm_network_interface" "deployment_nic" {
  name                = var.deployment_vm_nic_name
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name

  ip_configuration {
    name                          = var.deployment_vm_nic_ip_conf_name
    subnet_id                     = azurerm_subnet.pis_subnet.id
    private_ip_address_allocation = "Static"
    private_ip_address            = var.deployment_vm_nic_ip_conf_address
    public_ip_address_id          = azurerm_public_ip.deployment_ip.id
  }
}

resource "azurerm_linux_virtual_machine" "ci_cd_vm" {
  name                            = var.ci_cd_vm_name
  location                        = azurerm_resource_group.pis_rg.location
  resource_group_name             = azurerm_resource_group.pis_rg.name
  size                            = var.ci_cd_vm_size
  admin_username                  = var.vms_admin_username
  network_interface_ids           = [azurerm_network_interface.ci_cd_nic.id]
  disable_password_authentication = true

  admin_ssh_key {
    username   = var.vms_admin_username
    public_key = var.vms_ssh_keys
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts"
    version   = "latest"
  }
}

resource "azurerm_linux_virtual_machine" "deployment_vm" {
  name                            = var.deployment_vm_name
  location                        = azurerm_resource_group.pis_rg.location
  resource_group_name             = azurerm_resource_group.pis_rg.name
  size                            = var.deployment_vm_size
  admin_username                  = var.vms_admin_username
  network_interface_ids           = [azurerm_network_interface.deployment_nic.id]
  disable_password_authentication = true

  admin_ssh_key {
    username   = var.vms_admin_username
    public_key = var.vms_ssh_keys
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts"
    version   = "latest"
  }
}

resource "azurerm_network_interface_security_group_association" "ci_cd_nic_nsg" {
  network_interface_id      = azurerm_network_interface.ci_cd_nic.id
  network_security_group_id = azurerm_network_security_group.pis_nsg.id
}

resource "azurerm_network_interface_security_group_association" "deployment_nic_nsg" {
  network_interface_id      = azurerm_network_interface.deployment_nic.id
  network_security_group_id = azurerm_network_security_group.pis_nsg.id
}

resource "azurerm_dev_test_global_vm_shutdown_schedule" "ci_cd_shutdown" {
  virtual_machine_id = azurerm_linux_virtual_machine.ci_cd_vm.id
  location           = azurerm_resource_group.pis_rg.location
  enabled            = true

  daily_recurrence_time = var.vms_auto_shutdown_time
  timezone              = var.vms_auto_shutdown_timezone

  notification_settings {
    enabled = false
  }
}

resource "azurerm_dev_test_global_vm_shutdown_schedule" "deployment_shutdown" {
  virtual_machine_id = azurerm_linux_virtual_machine.deployment_vm.id
  location           = azurerm_resource_group.pis_rg.location
  enabled            = true

  daily_recurrence_time = var.vms_auto_shutdown_time
  timezone              = var.vms_auto_shutdown_timezone

  notification_settings {
    enabled = false
  }
}
