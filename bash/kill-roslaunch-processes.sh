#!/bin/bash

# Script to kill roslaunch processes in the Docker container
# Usage: ./kill-roslaunch-processes.sh [container_name]
# If no container_name provided, defaults to "air_slam"

CONTAINER_NAME="${1:-air_slam}"

echo "==============================================="
echo "🔪 Killing ROS Launch Processes in Container: $CONTAINER_NAME"
echo "==============================================="

# Check if container is running
if ! sudo docker ps --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Container '$CONTAINER_NAME' is not running."
    exit 1
fi

# Find roslaunch processes
echo "🔍 Searching for roslaunch processes..."
LAUNCH_PROCESSES=$(sudo docker exec "$CONTAINER_NAME" ps aux | grep -E "roslaunch|rosmaster" | grep -v grep)

if [[ -z "$LAUNCH_PROCESSES" ]]; then
    echo "ℹ️  No roslaunch or rosmaster processes found"
    exit 0
fi

echo "📋 Found processes:"
echo "$LAUNCH_PROCESSES"
echo ""

# Kill roslaunch processes
echo "🎯 Killing roslaunch processes..."
sudo docker exec "$CONTAINER_NAME" pkill -f "roslaunch" 2>/dev/null || true

# Kill rosmaster if it's running
echo "🎯 Killing rosmaster process..."
sudo docker exec "$CONTAINER_NAME" pkill -f "rosmaster" 2>/dev/null || true

# Wait a moment for processes to terminate
sleep 2

# Check if processes are still running
REMAINING_PROCESSES=$(sudo docker exec "$CONTAINER_NAME" ps aux | grep -E "roslaunch|rosmaster" | grep -v grep)

if [[ -z "$REMAINING_PROCESSES" ]]; then
    echo "✅ All roslaunch and rosmaster processes killed successfully"
else
    echo "⚠️  Some processes may still be running:"
    echo "$REMAINING_PROCESSES"
    echo ""
    echo "🔄 Force killing remaining processes..."
    sudo docker exec "$CONTAINER_NAME" pkill -9 -f "roslaunch" 2>/dev/null || true
    sudo docker exec "$CONTAINER_NAME" pkill -9 -f "rosmaster" 2>/dev/null || true
fi

echo ""
echo "✅ ROS launch processes cleanup completed!"

# Final verification
FINAL_CHECK=$(sudo docker exec "$CONTAINER_NAME" ps aux | grep -E "roslaunch|rosmaster" | grep -v grep)

if [[ -z "$FINAL_CHECK" ]]; then
    echo "✅ All processes successfully terminated"
else
    echo "⚠️  Some processes may still be running:"
    echo "$FINAL_CHECK"
    echo ""
    echo "💡 You may need to restart the container or manually kill remaining processes"
fi
