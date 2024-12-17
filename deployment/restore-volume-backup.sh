#!/bin/bash

# Default username to the current user
USERNAME=$(whoami)
KEY_FILE=""

# Parse optional arguments
while getopts "u:f:k:" opt; do
  case ${opt} in
    u )
      USERNAME=${OPTARG}
      ;;
    f )
      BACKUP_FILE=${OPTARG}
      ;;
    k )
      KEY_FILE=${OPTARG}
      ;;
    \? )
      echo "Usage: cmd [-u username] -f backup_file -k key_file"
      exit 1
      ;;
  esac
done

if [ -z "${BACKUP_FILE}" ]; then
  echo "Backup file must be specified with -f option"
  exit 1
fi

if [ -z "${KEY_FILE}" ]; then
  echo "Key file must be specified with -k option"
  exit 1
fi

REMOTE_HOST="ci-cd-vm.mgarbowski.pl"
BACKUP_DIR="~/docker_volume_backups"
VOLUME_NAME=$(basename ${BACKUP_FILE} | cut -d'_' -f1)

echo "Restoring backup file ${BACKUP_FILE} for volume ${VOLUME_NAME}"
echo "Using key file ${KEY_FILE}"
echo "Using username ${USERNAME}"
echo "Using remote host ${REMOTE_HOST}"
echo "Using backup directory ${BACKUP_DIR}"
echo "Using volume name ${VOLUME_NAME}"

# Ensure backup directory exists on remote machine
ssh -i ${KEY_FILE} ${USERNAME}@${REMOTE_HOST} "mkdir -p ${BACKUP_DIR}"

# Upload backup file to remote machine
scp -i ${KEY_FILE} ${BACKUP_FILE} ${USERNAME}@${REMOTE_HOST}:${BACKUP_DIR}/

# Restore the Docker volume from the backup file
ssh -i ${KEY_FILE} ${USERNAME}@${REMOTE_HOST} "docker run --rm -v ${VOLUME_NAME}:/volume -v ${BACKUP_DIR}:/backup alpine sh -c 'cd /volume && tar xzvf /backup/$(basename ${BACKUP_FILE})'"

# Clean up remote backup file
ssh -i ${KEY_FILE} ${USERNAME}@${REMOTE_HOST} "rm -f ${BACKUP_DIR}/$(basename ${BACKUP_FILE})"

echo "Restore completed for volume ${VOLUME_NAME}"