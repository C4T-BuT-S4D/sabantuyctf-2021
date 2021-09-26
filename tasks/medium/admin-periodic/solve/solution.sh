#!/bin/sh

IP="${1:-0.0.0.0}"
PORT="25687"

echo "Input the password: challenge"

ssh -p $PORT challenge@$IP '
date
directory="/var/tmp/data"
while true; do
    for file in $(ls "${directory}"); do
        path="${directory}/${file}"
        echo "Found file: $path"
        cat "$path"
        exit
    done
    sleep 0.5
done
'
