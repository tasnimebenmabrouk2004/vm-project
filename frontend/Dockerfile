FROM node:20 AS builder

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80
