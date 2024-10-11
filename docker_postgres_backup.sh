#!/bin/bash
# based on https://www.postgresqltutorial.com/postgresql-administration/postgresql-backup-database/

CONTAINER_NAME="github-pi-db-1"
BACKUP_DIR="/data_backups"

datestamp=$(date +'%Y-%m-%d')
timestamp=$(date +'%H%M')

BACKUP_FILENAME="data_db_${datestamp}_${timestamp}.sql"

docker exec -u root -t "$CONTAINER_NAME" mkdir -p "$BACKUP_DIR"
docker exec -u root -t "$CONTAINER_NAME" sh -c "pg_dump -d data_db > $BACKUP_DIR/$BACKUP_FILENAME"


echo "Backup completed: $BACKUP_DIR/$BACKUP_FILENAME"

read -p "Extract the backup out of docker container? (y/n): " extract_choice
if [[ $extract_choice == "y" || $extract_choice == "Y" ]]; then
    EXTRACT_DIR="./backups"
    mkdir -p "$EXTRACT_DIR"
    
    docker cp "$CONTAINER_NAME:$BACKUP_DIR/$BACKUP_FILENAME" "$EXTRACT_DIR/$BACKUP_FILENAME"
    
    echo "Backup extracted to: $EXTRACT_DIR/$BACKUP_FILENAME"
else
    echo "Backup remains in the Docker container."
fi

echo "Backups done ✅"
