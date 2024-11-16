#!/bin/bash

REMOTE_HOST="ci-cd-vm.mgarbowski.pl"
BACKUP_DIR="/tmp/docker_volume_backups"
LOCAL_BACKUP_DIR="./docker_volume_backups"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Create backup directory on remote machine
ssh ${REMOTE_HOST} "mkdir -p ${BACKUP_DIR}"

# Get list of Docker volumes
VOLUMES=$(ssh ${REMOTE_HOST} "docker volume ls -q")

# Backup each volume
for VOLUME in ${VOLUMES}; do
  ssh ${REMOTE_HOST} "docker run --rm -v ${VOLUME}:/volume -v ${BACKUP_DIR}:/backup alpine tar czvf /backup/${VOLUME}_${TIMESTAMP}.tar.gz -C /volume ."
done

# Create local backup directory
mkdir -p ${LOCAL_BACKUP_DIR}

# Download backups to local machine
scp ${REMOTE_HOST}:${BACKUP_DIR}/*.tar.gz ${LOCAL_BACKUP_DIR}/

# Clean up remote backup directory
ssh ${REMOTE_HOST} "rm -rf ${BACKUP_DIR}"

echo "Backup completed and downloaded to ${LOCAL_BACKUP_DIR}"