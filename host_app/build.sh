#!/bin/sh
docker build -t ispirtraian/test-did-host-app -f Dockerfile.cpu .
docker push ispirtraian/test-did-host-app
