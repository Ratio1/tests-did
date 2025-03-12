#!/bin/sh
set -e

# Function to wait for the Docker daemon to be ready
wait_for_dockerd() {
    echo "Waiting for Docker daemon to start..."
    while ! docker info > /dev/null 2>&1; do
        sleep 1
    done
    echo "Docker daemon is ready!"
}

dockerd-entrypoint.sh &

# Wait until dockerd is fully initialized
wait_for_dockerd

exec "$@"