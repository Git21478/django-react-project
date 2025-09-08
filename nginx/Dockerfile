FROM nginx:1.29.1-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx-main.conf /etc/nginx/nginx.conf

COPY reverse-proxy.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
# EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]