FROM nginx:1.29.0-alpine

COPY nuxtapp/.output/public /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d

CMD ["nginx", "-g", "daemon off;"]
