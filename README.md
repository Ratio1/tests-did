# Simple Docker-in-Docker project


- `some_app` arbitrary app image that just prints some text (Dockerfile included)
- a host containerized app that rung `some_app` in a container and prints the output - this app runs in a docker-in-docker setup



```bash
cd external_app
docker build -t aidamian/test-did-external-app .
docker push aidamian/test-did-external-app
```

```bash
cd host_app
docker build -t aidamian/test-did-host-app .
docker push aidamian/test-did-host-app
```

```bash
docker run --rm --privileged aidamian/test-did-host-app
```
