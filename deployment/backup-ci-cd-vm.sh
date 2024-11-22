#!/bin/bash

# Default username to the current user
USERNAME=$(whoami)

# Parse optional arguments
while getopts "u:" opt; do
  case ${opt} in
    u )
      USERNAME=${OPTARG}
      ;;
    \? )
      echo "Usage: cmd [-u username]"
      exit 1
      ;;
  esac
done

REMOTE_HOST="ci-cd-vm.mgarbowski.pl"
BACKUP_DIR="/tmp/docker_volume_backups"
LOCAL_BACKUP_DIR="./docker_volume_backups"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Create backup directory on remote machine
ssh ${USERNAME}@${REMOTE_HOST} "mkdir -p ${BACKUP_DIR}"

# Get list of Docker volumes
VOLUMES=$(ssh ${USERNAME}@${REMOTE_HOST} "docker volume ls -q")

# Backup each volume
for VOLUME in ${VOLUMES}; do
  ssh ${USERNAME}@${REMOTE_HOST} "docker run --rm -v ${VOLUME}:/volume -v ${BACKUP_DIR}:/backup alpine tar czvf /backup/${VOLUME}_${TIMESTAMP}.tar.gz -C /volume ."
done

# Create local backup directory
mkdir -p ${LOCAL_BACKUP_DIR}

# Download backups to local machine
scp ${USERNAME}@${REMOTE_HOST}:${BACKUP_DIR}/*.tar.gz ${LOCAL_BACKUP_DIR}/

# Clean up remote backup directory
ssh ${USERNAME}@${REMOTE_HOST} "rm -rf ${BACKUP_DIR}"

echo "Backup completed and downloaded to ${LOCAL_BACKUP_DIR}"