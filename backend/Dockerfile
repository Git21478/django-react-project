FROM python:3.13.5-alpine3.22 AS builder

RUN apk add --no-cache curl

ENV DJANGO_ENV=development

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput



FROM python:3.13.5-alpine3.22 AS production

RUN apk add --no-cache curl

ENV DJANGO_ENV=development

WORKDIR /app

COPY --from=builder /app /app
COPY --from=builder /app/staticfiles /app/staticfiles

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn -c gunicorn.py --bind 0.0.0.0:8000 backend.wsgi:application"]