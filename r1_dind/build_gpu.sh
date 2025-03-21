#!/bin/sh
docker build -t aidamian/base_edge_node:x86_64-py3.10.12-th2.3.1.cu121-tr4.43.3-d . -f Dockerfile.gpu
docker push aidamian/base_edge_node:x86_64-py3.10.12-th2.3.1.cu121-tr4.43.3-d