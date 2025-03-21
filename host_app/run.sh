#!/bin/sh
docker run --rm --privileged \
       -v dind-cache:/var/lib/docker \
       -v "$(pwd)"/config.json:/app/config.json \
       -p 8080:8080 \
       -p 8081:5000 \
       ispirtraian/test-did-host-app


    