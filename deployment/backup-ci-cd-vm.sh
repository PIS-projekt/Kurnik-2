#!/bin/bash

# Default username to the current user
USERNAME=$(whoami)
KEY_FILE=""

# Parse optional arguments
while getopts "u:k:" opt; do
  case ${opt} in
    u )
      USERNAME=${OPTARG}
      ;;
    k )
      KEY_FILE=${OPTARG}
      ;;
    \? )
      echo "Usage: cmd [-u username] [-k key_file]"
      exit 1
      ;;
  esac
done

if [ -z "${KEY_FILE}" ]; then
  echo "Key file must be specified with -k option"
  exit 1
fi

REMOTE_HOST="ci-cd-vm.mgarbowski.pl"
BACKUP_DIR="~/docker_volume_backups"
LOCAL_BACKUP_DIR="./docker_volume_backups"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Create backup directory on remote machine
ssh -i ${KEY_FILE} ${USERNAME}@${REMOTE_HOST} "mkdir -p ${BACKUP_DIR}"

# Backup only the volumes we care about
VOLUMES=("certs" "jenkins-data" "jenkins-docker-certs" "nexus-data")

# Backup each volume
for VOLUME in "${VOLUMES[@]}"; do
  ssh -i ${KEY_FILE} ${USERNAME}@${REMOTE_HOST} "docker run --rm -v ${VOLUME}:/volume -v ${BACKUP_DIR}:/backup alpine tar czvf /backup/${VOLUME}_${TIMESTAMP}.tar.gz -C /volume ."
done

# Create local backup directory
mkdir -p ${LOCAL_BACKUP_DIR}

# Download backups to local machine
scp -i ${KEY_FILE} ${USERNAME}@${REMOTE_HOST}:${BACKUP_DIR}/*.tar.gz ${LOCAL_BACKUP_DIR}/

# Clean up remote backup directory
ssh -i ${KEY_FILE} ${USERNAME}@${REMOTE_HOST} "rm -rf ${BACKUP_DIR}"

echo "Backup completed and downloaded to ${LOCAL_BACKUP_DIR}"