FROM node:22.17.1-alpine3.21 AS builder

WORKDIR /app

COPY frontend/package.json .

RUN npm install

COPY frontend .

RUN npm run build



FROM nginx:1.29.1-alpine AS production

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]