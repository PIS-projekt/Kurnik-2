output "ci_cd_vm_public_ip" {
    description = "The public IP address of the CI/CD VM."
    value       = azurerm_public_ip.ci_cd_ip.ip_address
}

output "deployment_vm_public_ip" {
    description = "The public IP address of the deployment VM."
    value       = azurerm_public_ip.deployment_ip.ip_address
}
