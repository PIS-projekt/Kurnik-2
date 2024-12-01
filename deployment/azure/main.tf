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
  name = "pis-rg-2"
  location = "westeurope"
}

resource "azurerm_public_ip" "ci_cd_ip" {
  name                = "ci-cd-ip"
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
  allocation_method   = "Dynamic"
}

resource "azurerm_public_ip" "deployment_ip" {
  name                = "deployment-ip"
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
  allocation_method   = "Dynamic"
}

resource "azurerm_virtual_network" "pis_vnet" {
  name                = "pis-vnet"
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_network_security_group" "pis_nsg" {
  name                = "pis-nsg"
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
}

resource "azurerm_network_security_rule" "ssh_rule" {
  name                        = "pis-nsg-rule-ssh"
  priority                    = 1000
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  network_security_group_name = azurerm_network_security_group.pis_nsg.name
  resource_group_name         = azurerm_resource_group.pis_rg.name
}

resource "azurerm_network_security_rule" "http_rule" {
  name                        = "pis-nsg-rule-http"
  priority                    = 1020
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "80"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  network_security_group_name = azurerm_network_security_group.pis_nsg.name
  resource_group_name         = azurerm_resource_group.pis_rg.name
}

resource "azurerm_network_security_rule" "https_rule" {
  name                        = "pis-nsg-rule-https"
  priority                    = 1030
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  network_security_group_name = azurerm_network_security_group.pis_nsg.name
  resource_group_name         = azurerm_resource_group.pis_rg.name
}

resource "azurerm_subnet" "pis_subnet" {
  name                 = "pis-subnet"
  resource_group_name  = azurerm_resource_group.pis_rg.name
  virtual_network_name = azurerm_virtual_network.pis_vnet.name
  address_prefixes     = ["10.0.1.0/24"]
#   network_security_group_id = azurerm_network_security_group.pis_nsg.id
}

resource "azurerm_network_interface" "ci_cd_nic" {
  name                = "ci-cd-nic"
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name

  ip_configuration {
    name                          = "ci-cd-ip-config"
    subnet_id                     = azurerm_subnet.pis_subnet.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "10.0.1.4"
    public_ip_address_id          = azurerm_public_ip.ci_cd_ip.id
  }
}

resource "azurerm_network_interface" "deployment_nic" {
  name                = "deployment-nic"
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name

  ip_configuration {
    name                          = "deployment-ip-config"
    subnet_id                     = azurerm_subnet.pis_subnet.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "10.0.1.5"
    public_ip_address_id          = azurerm_public_ip.deployment_ip.id
  }
}

resource "azurerm_linux_virtual_machine" "ci_cd_vm" {
  name                = "ci-cd-vm"
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
  size                = "Standard_B1s"
  admin_username      = "azureuser"
  network_interface_ids = [azurerm_network_interface.ci_cd_nic.id]
  disable_password_authentication = true

  admin_ssh_key {
    username   = "azureuser"
    public_key = file("./ssh-keys")
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
  name                = "deployment-vm"
  location            = azurerm_resource_group.pis_rg.location
  resource_group_name = azurerm_resource_group.pis_rg.name
  size                = "Standard_B1s"
  admin_username      = "azureuser"
  network_interface_ids = [azurerm_network_interface.deployment_nic.id]
  disable_password_authentication = true

  admin_ssh_key {
    username   = "azureuser"
    public_key = file("./ssh-keys")
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

resource "azurerm_dev_test_global_vm_shutdown_schedule" "ci_cd_shuitdown" {
  virtual_machine_id = azurerm_linux_virtual_machine.ci_cd_vm.id
  location           = azurerm_resource_group.pis_rg.location
  enabled            = true

  daily_recurrence_time = "1500"
  timezone              = "Pacific Standard Time"

  notification_settings {
    enabled = false
  }
}

resource "azurerm_dev_test_global_vm_shutdown_schedule" "deployment_shuitdown" {
  virtual_machine_id = azurerm_linux_virtual_machine.deployment_vm.id
  location           = azurerm_resource_group.pis_rg.location
  enabled            = true

  daily_recurrence_time = "1500"
  timezone              = "Pacific Standard Time"

  notification_settings {
    enabled = false
  }
}
