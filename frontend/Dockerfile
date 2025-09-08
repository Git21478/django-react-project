FROM node:22.17.1-alpine3.21 AS builder

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN npm run build



FROM nginx:1.29.1-alpine AS production

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]