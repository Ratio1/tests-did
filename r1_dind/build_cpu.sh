#!/bin/sh
docker build -t aidamian/base_edge_node:x86_64-py3.10.12-th2.4.0.cpu-tr4.43.3-d . -f Dockerfile.cpu
docker push aidamian/base_edge_node:x86_64-py3.10.12-th2.4.0.cpu-tr4.43.3-d