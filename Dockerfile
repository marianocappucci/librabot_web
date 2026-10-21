# La misma base que la imagen libra-nginx-web del kit (nginx:1.27-alpine), sin el bloque
# de /docs/ y su auth, como librasuite_web: ver nginx.conf.
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY public/ /usr/share/nginx/html/
EXPOSE 80
