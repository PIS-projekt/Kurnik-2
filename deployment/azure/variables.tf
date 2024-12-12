variable "rg_name" {
  description = "The name of the resource group in which to create the resources."
  type        = string
  default     = "pis-rg-2"
}

variable "location" {
  description = "The location/region where the resources will be created."
  type        = string
  default     = "westeurope"
}

variable "ci_cd_vm_public_ip_name" {
  description = "The name of the public IP address for the CI/CD VM."
  type        = string
  default     = "ci-cd-ip"
}

variable "deployment_vm_public_ip_name" {
  description = "The name of the public IP address for the deployment VM."
  type        = string
  default     = "deployment-ip"
}

variable "vnet_name" {
  description = "The name of the virtual network."
  type        = string
  default     = "pis-vnet"
}

variable "vnet_address_space" {
  description = "The address space that is used by the virtual network."
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "nsg_name" {
  description = "The name of the network security group."
  type        = string
  default     = "pis-nsg"
}

variable "nsg_rules" {
  description = "A list of network security rules."
  type = list(object({
    name                       = string
    priority                   = number
    direction                  = string
    access                     = string
    protocol                   = string
    source_port_range          = string
    destination_port_range     = string
    source_address_prefix      = string
    destination_address_prefix = string
  }))
  default = [
    {
      name                       = "pis-nsg-rule-ssh"
      priority                   = 1000
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "22"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    },
    {
      name                       = "pis-nsg-rule-http"
      priority                   = 1020
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "80"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    },
    {
      name                       = "pis-nsg-rule-https"
      priority                   = 1030
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "443"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    }
  ]
}

variable "subnet_name" {
  description = "The name of the subnet."
  type        = string
  default     = "pis-subnet"
}

variable "subnet_address_prefixes" {
  description = "A list of address prefixes that are used by the subnet."
  type        = list(string)
  default     = ["10.0.1.0/24"]
}

variable "ci_cd_vm_nic_name" {
  description = "The name of the network interface for the CI/CD VM."
  type        = string
  default     = "ci-cd-nic"
}

variable "ci_cd_vm_nic_ip_conf_name" {
  description = "The name of the IP configuration for the network interface for the CI/CD VM."
  type        = string
  default     = "ci-cd-ip-config"
}

variable "ci_cd_vm_nic_ip_conf_address" {
  description = "The private IP address that is used by the network interface for the CI/CD VM."
  type        = string
  default     = "10.0.1.4"
}

variable "deployment_vm_nic_name" {
  description = "The name of the network interface for the deployment VM."
  type        = string
  default     = "deployment-nic"
}

variable "deployment_vm_nic_ip_conf_name" {
  description = "The name of the IP configuration for the network interface for the deployment VM."
  type        = string
  default     = "deployment-ip-config"
}

variable "deployment_vm_nic_ip_conf_address" {
  description = "The private IP address that is used by the network interface for the deployment VM."
  type        = string
  default     = "10.0.1.5"
}

variable "ci_cd_vm_name" {
  description = "The name of the CI/CD VM."
  type        = string
  default     = "ci-cd-vm"
}

variable "ci_cd_vm_size" {
  description = "The size of the CI/CD VM."
  type        = string
  default     = "Standard_B1s"
}

variable "deployment_vm_name" {
  description = "The name of the deployment VM."
  type        = string
  default     = "deployment-vm"
}

variable "deployment_vm_size" {
  description = "The size of the deployment VM."
  type        = string
  default     = "Standard_B1s"
}

variable "vms_admin_username" {
  description = "The username of created user."
  type        = string
  default     = "azureuser"
}

variable "vms_ssh_keys" {
  description = "The public SSH keys that are used to authenticate to VMs."
  type        = string
  default     = file("./ssh-keys")
}

variable "vms_auto_shutdown_time" {
  description = "Time string in format HHMM."
  type        = string
  default     = "1500"
}

variable "vms_auto_shutdown_timezone" {
  description = "Timezone string."
  type        = string
  default     = "Pacific Standard Time"
}
