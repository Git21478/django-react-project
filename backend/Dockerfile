FROM python:3.13.5-alpine3.22

RUN apk add --no-cache curl

ENV DJANGO_ENV=development

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles /app/media && \
    chmod -R 755 /app/staticfiles /app/media

EXPOSE 8000

CMD ["sh", "-c", " python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn -c gunicorn.py --bind 0.0.0.0:8000 backend.wsgi:application"]