FROM nginx:alpine

# Install certbot
RUN apk add --no-cache certbot certbot-nginx

COPY ./nginx.conf /etc/nginx/nginx.conf