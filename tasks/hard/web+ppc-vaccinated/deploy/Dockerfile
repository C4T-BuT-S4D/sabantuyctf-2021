FROM python:alpine as dbbuilder
WORKDIR /build
COPY prepare_db.py .
RUN python prepare_db.py


FROM node:14-alpine

WORKDIR /usr/src/app

COPY src/package*.json ./

RUN npm install

COPY src .

COPY --from=dbbuilder /build/storage.db /storage.db

CMD [ "node", "app.js" ]