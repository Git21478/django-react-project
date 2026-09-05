#!/bin/bash
set -e

python manage.py collectstatic --noinput

ls -la db_dumps || echo "Папка db_dumps не найдена!"

TABLE_COUNT=$(psql -h database -U ${POSTGRES_USER} -d ${POSTGRES_DB} -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';")
TABLE_COUNT=$(echo $TABLE_COUNT | tr -d '[:space:]')

echo "Результат TABLE_COUNT: '$TABLE_COUNT'"

# Загрузка дампа БД
if [ -f db_dumps/db_dump_for_quickstart.sql ] && [ "$TABLE_COUNT" -eq 0 ]; then
    psql -h database -U ${POSTGRES_USER} -d ${POSTGRES_DB} < db_dumps/db_dump_for_quickstart.sql

    # Загрузка дампа media
    if [ -f media_dumps/media_dump_for_quickstart.tar.gz ]; then
        tar -xzf media_dumps/media_dump_for_quickstart.tar.gz -C /app/
    fi
fi

python manage.py migrate --noinput
gunicorn -c gunicorn.py --bind 0.0.0.0:8000 backend.wsgi:application