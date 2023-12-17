#!/bin/sh

docker run --rm -p 8090:8080 \
    -e DYNAMIC_CONFIG_ENABLED=true \
    --name kafka-ui \
    --add-host=primary:192.168.205.3 \
    provectuslabs/kafka-ui

