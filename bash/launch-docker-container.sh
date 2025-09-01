#!/bin/bash

# AirSLAM Docker Container Launcher
# This script launches the AirSLAM development environment with GPU support
# and mounts the external SSD to make SVO data accessible

echo "Launching AirSLAM Docker container..."
echo "============================================"
echo "Container will have access to:"
echo "  - NVIDIA GPU (RTX 3070)"
echo "  - Host display for GUI applications"
echo "  - External SSD workspace at /workspace"
echo "  - External SSD data at /home/skumar/ext_ssd"
echo "============================================"

# Check if container already exists
if sudo docker ps -a --format 'table {{.Names}}' | grep -q "^air_slam$"; then
    echo "Stopping existing air_slam container..."
    sudo docker stop air_slam >/dev/null 2>&1
    echo "Removing existing air_slam container..."
    sudo docker rm air_slam >/dev/null 2>&1
fi

echo "Starting new air_slam container..."

# Change to the external SSD workspace directory
cd /home/skumar/ext_ssd/catkin_ws

# Launch the container with all necessary mounts and configurations
sudo docker run -it \
    --env DISPLAY=$DISPLAY \
    --env NVIDIA_DRIVER_CAPABILITIES=all \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --privileged \
    --runtime nvidia \
    --gpus all \
    --volume /home/skumar/ext_ssd/catkin_ws:/workspace \
    --volume /home/skumar/ext_ssd:/home/skumar/ext_ssd \
    --workdir /workspace \
    --name air_slam \
    xukuanhit/air_slam:v4 \
    /bin/bash

echo "AirSLAM container stopped."
