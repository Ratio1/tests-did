# Simple Docker-in-Docker Project

Ratio1 | [Website](https://ratio1.ai) | [Blog](https://ratio1.com/blog)

This development repository demonstrates a simple setup where one Docker container (the **host_app**) runs Docker itself (Docker-in-Docker) and launches another container (the **external_app**). In other words, it shows how a container can orchestrate another container and capture its output. This pattern is sometimes useful for CI/CD pipelines or isolated test environments, but **should be used carefully**, since Docker-in-Docker comes with particular security considerations.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Directory Structure](#directory-structure)
- [Building and Pushing Images](#building-and-pushing-images)
    - [1. external_app (some_app)](#1-external_app-some_app)
    - [2. host_app (Docker-in-Docker)](#2-host_app-docker-in-docker)
- [Running the Host App](#running-the-host-app)
- [Technical Details](#technical-details)
- [Security Considerations](#security-considerations)

---

## Overview

1. **external_app** (“some_app”):  
   A simple Python-based Docker image that prints out some text (or does some trivial task).  

2. **host_app**:  
   A Docker-in-Docker (DinD) container that launches **external_app** as a separate container. It then captures the output of **external_app** and prints it to stdout.  

**High-Level Flow**:  
```
HOST_CONTAINER (DinD) -> runs docker commands -> external_app container
```

---

## Prerequisites

- Docker installed locally.  
- Docker Hub (or another image registry) credentials, if you plan to push these images.  
- Sufficient privileges to run Docker in privileged mode.  

---

## Directory Structure

```
project-root/
  ├─ external_app/
  │    ├─ Dockerfile
  │    └─ main.py        # Simple script that prints text
  └─ host_app/
       ├─ Dockerfile
       └─ main.py        # Python script that runs "docker run <external_app>"
```

---

## Building and Pushing Images

Below are example commands to build and optionally push these images to a Docker registry (e.g., Docker Hub). Adjust tag names (including the namespace/username) to your own preference.

### 1. external_app (some_app)

```bash
cd external_app
docker build -t aidamian/test-did-external-app .
docker push aidamian/test-did-external-app
```

**What it does**:  
- Builds an image from the `Dockerfile` in `external_app`.  
- Publishes it to the Docker registry under the tag `aidamian/test-did-external-app`.  

### 2. host_app (Docker-in-Docker)

```bash
cd ../host_app
docker build -t aidamian/test-did-host-app .
docker push aidamian/test-did-host-app
```

**What it does**:  
- Builds the Docker-in-Docker based image that includes a Python script to orchestrate the **external_app** container.  
- Publishes it under the tag `aidamian/test-did-host-app`.  

---

## Running the Host App

Once both images are built and pushed (or built locally), you can run the **host_app** container. Note that it needs to run in privileged mode to properly enable Docker-in-Docker:

```bash
docker run --rm --privileged aidamian/test-did-host-app
```

**What to Expect**:  
- The host container starts the Docker daemon inside itself (DinD).  
- It then attempts to pull/run the `aidamian/test-did-external-app` container.  
- Finally, it captures and prints the output from that container.  

Sample output might look like:
```
Host container started. Attempting to run external_app container...
Successfully ran external_app container!
Output from container: Hello from the naive Python container!
```

---

## Technical Details

1. **external_app/main.py**:  
   A trivial Python script that prints a greeting.  
   ```python
   print("Hello from the naive Python container!")
   ```

2. **host_app/Dockerfile**:  
   - Based on the official `docker:dind` image.  
   - Installs Python so that we can run a Python script.  
   - Copies `main.py` (host-side logic) into the container.  

3. **host_app/main.py**:  
   - Uses `subprocess.run(["docker", "run", "..."])` to orchestrate running the **external_app**.  
   - Captures stdout and stderr.  
   - Checks the return code to provide a basic success/failure message.  

---

## Security Considerations

- **Docker-in-Docker** requires `--privileged` mode (or a comparable set of extended capabilities). In many environments, this level of access might be disallowed due to security policies.  
- Because the DinD container can effectively run Docker commands, it can create and manipulate containers and images at will so the DinD container cand run only as the Ratio1 Edge Node.
- If you want to store Docker artifacts persistently in the **host_app** container, mount a volume to `/var/lib/docker`. This is optional but might be useful for caching or debugging.  

---

If you have any questions or issues, please feel free to open an issue or contact the maintainer. Happy coding!