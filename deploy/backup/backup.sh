#!/bin/bash

# Загрузка переменных из файла .env
set -o allexport
source .pg-env
set +o allexport

POSTGRES_HOST="postgresql-db"
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_FILE="$BACKUP_DIR/$POSTGRES_DB-$TIMESTAMP.sql"

# Создание директории для бэкапов, если её нет
mkdir -p $BACKUP_DIR

# Установка переменной окружения для пароля
export PGPASSWORD=$POSTGRES_PASSWORD

# Создание резервной копии
pg_dump -U $POSTGRES_USER -h $POSTGRES_HOST -F c $POSTGRES_DB > $BACKUP_FILE

# Удаление бэкапов старше 5 дней
cd backups
sudo find . -type f -name "*.sql" -mtime +3 -exec rm {} \;
