FROM golang:1.17.1-alpine as build
WORKDIR /usr/local/app
COPY go-mdot go-mdot
RUN cd go-mdot && CGO_ENABLED=0 GOOS=linux go build -o ../mdot-server cmd/mdot-server.go

FROM alpine:latest
WORKDIR /usr/local/app
COPY --from=build /usr/local/app/mdot-server mdot-server
ENTRYPOINT [ "./mdot-server" ]