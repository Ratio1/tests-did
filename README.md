# Simple Docker-in-Docker project


- `some_app` arbitrary app image that just prints some text (Dockerfile included)
- a host containerized app that rung `some_app` in a container and prints the output - this app runs in a docker-in-docker setup