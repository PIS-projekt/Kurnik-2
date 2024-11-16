#!/bin/bash

# Create public IP for ci cd vm
az network public-ip create \
    --resource-group "pis-rg" \
    --name "ci-cd-ip"

# Create public IP for deployment vm
az network public-ip create \
    --resource-group "pis-rg" \
    --name "deployment-ip"

# Create virtual network
az network vnet create \
    --resource-group "pis-rg" \
    --name "pis-vnet" \
    --address-prefix 10.0.0.0/16

# Create network security group
az network nsg create \
    --resource-group "pis-rg" \
    --name "pis-nsg"

# Add network security group rule
az network nsg rule create \
    --resource-group "pis-rg" \
    --nsg-name "pis-nsg" \
    --name "pis-nsg-rule-ssh" \
    --protocol tcp \
    --priority 1000 \
    --destination-port-range 22 \
    --access allow

## Add network security group rule to allow HTTP traffic to nginx
az network nsg rule create \
    --resource-group "pis-rg" \
    --nsg-name "pis-nsg" \
    --name "pis-nsg-rule-http" \
    --protocol tcp \
    --priority 1020 \
    --destination-port-range 80 \
    --access allow

## Add network security group rule to allow HTTPS traffic to nginx
az network nsg rule create \
    --resource-group "pis-rg" \
    --nsg-name "pis-nsg" \
    --name "pis-nsg-rule-http3" \
    --protocol tcp \
    --priority 1030 \
    --destination-port-range 443 \
    --access allow

# Create subnet
az network vnet subnet create \
        --resource-group "pis-rg" \
        --vnet-name "pis-vnet" \
        --name "pis-subnet" \
        --address-prefix 10.0.1.0/24 \
        --network-security-group "pis-nsg"

# Create ci cd vm network interface
az network nic create \
    --resource-group "pis-rg" \
    --name "ci-cd-nic" \
    --vnet-name "pis-vnet" \
    --subnet "pis-subnet" \
    --network-security-group "pis-nsg" \
    --private-ip-address "10.0.1.4" \
    --public-ip-address "ci-cd-ip"

# Create deployment vm network interface
az network nic create \
    --resource-group "pis-rg" \
    --name "deployment-nic" \
    --vnet-name "pis-vnet" \
    --subnet "pis-subnet" \
    --network-security-group "pis-nsg" \
    --private-ip-address "10.0.1.5" \
    --public-ip-address "deployment-ip"


# Create ci cd vm
az vm create \
    --resource-group "pis-rg" \
    --name "ci-cd-vm" \
    --location "westeurope" \
    --image "Ubuntu2404" \
    --nics "ci-cd-nic" \
    --admin-username "azureuser" \
    --ssh-key-values "./ssh-keys"

# Auto-shutdown ci cd vm
az vm auto-shutdown \
    --resource-group "pis-rg" \
    --name "ci-cd-vm" \
    --time 2300

# Create deployment vm
az vm create \
    --resource-group "pis-rg" \
    --name "deployment-vm" \
    --location "westeurope" \
    --image "Ubuntu2404" \
    --nics "deployment-nic" \
    --admin-username "azureuser" \
    --ssh-key-values "./ssh-keys"

# Auto-shutdown ci cd vm
az vm auto-shutdown \
    --resource-group "pis-rg" \
    --name "deployment-vm" \
    --time 2300
