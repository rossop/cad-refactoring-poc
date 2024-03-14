#!/bin/bash

# Function to cleanup resources
cleanup() {
    echo "Cleaning up resources..."
    # Stop the container (container is automatically removed due to --rm flag)
    docker stop my_jupyter_cadquery_test 2>/dev/null
    # docker rm my_jupyter_cadquery_test 2>/dev/null
    docker rmi my_jupyter_cadquery 2>/dev/null
    echo "Cleanup complete."
}

# Ensure cleanup runs on script exit, including when exiting with an error code
trap cleanup EXIT

# Ensure the script is run from the project root directory
if [ ! -f Dockerfile ]; then
    echo "Error: Dockerfile not found. This script must be run from the project root directory."
    exit 1
fi

# Build the Docker image
# docker build -t my_jupyter_cadquery .
docker build --no-cache --progress=plain -t my_jupyter_cadquery .


# Run the Docker container in detached mode, mounting the project directory
docker run -d --rm -p 8888:8888 -v "$(pwd)":/home/cq --name my_jupyter_cadquery_test my_jupyter_cadquery

# Wait for the container to start properly
sleep 10

# Attempt to run the test command with a timeout
timeout=30 # 30 seconds timeout
while ! docker exec my_jupyter_cadquery_test ls /home/cq | grep -q notebooks
do
    if [ $timeout -le 0 ]; then
        docker logs my_jupyter_cadquery_test
        echo "Container did not become ready in time."
        exit 1
    fi
    sleep 1
    ((timeout--))
done
echo "Notebooks folder test passed."

cleanup
echo "All tests completed successfully."
