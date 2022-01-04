FROM nginx:1.19.0-alpine

RUN sudo service nginx restart
RUN -s reload

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d