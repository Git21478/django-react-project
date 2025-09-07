FROM nginx:1.29.1-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /app/backend/media

RUN chown -R nginx:nginx /app

EXPOSE 80 443