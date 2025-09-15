FROM nginx:1.29.1-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx-main.conf /etc/nginx/nginx.conf

COPY reverse-proxy.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /app/staticfiles /app/media && \
    chmod -R 755 /app/staticfiles /app/media

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]