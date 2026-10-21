# etapa 1: se compila angular, aqui si hace falta node
FROM node:24-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
# npm ci instala justo las versiones de package-lock.json
RUN npm ci

COPY . .
RUN npm run build

# etapa 2: nginx solo entrega los archivos ya compilados, node ya no se necesita
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html

EXPOSE 80
