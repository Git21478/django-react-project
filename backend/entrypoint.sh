#!/bin/bash
set -e

python manage.py migrate --noinput

USER_COUNT=$(python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.count())" 2>/dev/null || echo 0)

# Загрузка дампа БД
if [ -f db_dumps/dump_for_quickstart.sql ] && [ "$USER_COUNT" -eq 0 ]: then
    psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < db_dumps/dump_for_quickstart.sql 
fi

# Загрузка изображений
# if [ -f media_dumps/media_backup.tar.gz ]; then
#     tar -xzf media_dumps/media_backup.tar.gz -C /app/media
# fi

gunicorn -c gunicorn.py --bind 0.0.0.0:8000 backend.wsgi:application