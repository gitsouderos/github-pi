#!/bin/bash

CONTAINER_NAME="github-pi-db-1"
BACKUP_DIR="/data_backups"
FILE="data_db_FULL.sql"

docker exec -u root -t "$CONTAINER_NAME" sh -c "mkdir -p $BACKUP_DIR"
docker cp ./backups/$FILE $CONTAINER_NAME:$BACKUP_DIR/
docker exec -u root -t "$CONTAINER_NAME" sh -c "psql -d data_db -f $BACKUP_DIR/$FILE"

echo "DB restored ✅"
