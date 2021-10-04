#!/bin/sh

IP="${1:-0.0.0.0}"
PORT="21236"

curl \
    -X POST \
    --url "http://$IP:$PORT/api/check/" \
    --header "Content-Type: application/json" \
    --data @solution.json
