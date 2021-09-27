FROM python:alpine as dbbuilder
WORKDIR /build
COPY prepare_db.py .
RUN python prepare_db.py


FROM openresty/openresty:1.19.9.1-1-alpine-fat

RUN /usr/local/openresty/luajit/bin/luarocks install --global lsqlite3complete
RUN /usr/local/openresty/luajit/bin/luarocks install --global lua-resty-session
RUN /usr/local/openresty/luajit/bin/luarocks install --global lua-cjson

COPY resty.conf /etc/nginx/conf.d/default.conf

RUN mkdir /storage
RUN chmod -R 777 /storage
COPY --from=dbbuilder /build/storage.db /storage/storage.db

