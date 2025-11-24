FROM nginx:1.29-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx-main.conf /etc/nginx/nginx.conf

COPY reverse-proxy.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /app/staticfiles /app/media && \
    chmod -R 755 /app

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]