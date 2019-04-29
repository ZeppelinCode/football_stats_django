FROM nginx:latest

COPY start-nginx.sh /start-nginx.sh
COPY nginx.conf /etc/nginx/nginx.conf

COPY football_stats.conf /etc/nginx/conf.d/default.conf

RUN chmod +x /start-nginx.sh

RUN mkdir -p /logs/nginx

CMD ["/start-nginx.sh"]
