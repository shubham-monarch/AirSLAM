#!/bin/bash

# Script to kill active ROS nodes in the Docker container
# Usage: ./kill-ros-nodes.sh [container_name] [node_names...]
# If no container_name provided, defaults to "air_slam"
# If no node_names provided, attempts to kill common AirSLAM nodes

CONTAINER_NAME="${1:-air_slam}"
shift  # Remove first argument, rest are node names

echo "==============================================="
echo "🧹 Killing ROS Nodes in Container: $CONTAINER_NAME"
echo "==============================================="

# Check if container is running
if ! sudo docker ps --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Container '$CONTAINER_NAME' is not running."
    exit 1
fi

# Source ROS and check if master is running
ROS_CHECK=$(sudo docker exec "$CONTAINER_NAME" bash -c "source /opt/ros/noetic/setup.bash && rosnode list 2>/dev/null || echo 'NO_MASTER'")

if [[ "$ROS_CHECK" == "NO_MASTER" ]]; then
    echo "ℹ️  No ROS master running in container '$CONTAINER_NAME'"
    exit 0
fi

# Get list of running nodes
NODE_LIST=$(sudo docker exec "$CONTAINER_NAME" bash -c "source /opt/ros/noetic/setup.bash && rosnode list | grep -v '/rosout'")

if [[ -z "$NODE_LIST" ]]; then
    echo "ℹ️  No ROS nodes running (excluding /rosout)"
    exit 0
fi

echo "📋 Found ROS nodes:"
echo "$NODE_LIST"
echo ""

# If specific nodes provided, kill only those
if [[ $# -gt 0 ]]; then
    echo "🎯 Killing specified nodes: $@"
    for node in "$@"; do
        if echo "$NODE_LIST" | grep -q "$node"; then
            echo "Killing node: $node"
            sudo docker exec "$CONTAINER_NAME" bash -c "source /opt/ros/noetic/setup.bash && rosnode kill $node" 2>/dev/null || true
        else
            echo "⚠️  Node '$node' not found"
        fi
    done
else
    # Kill common AirSLAM nodes
    echo "🎯 Killing common AirSLAM nodes..."
    COMMON_NODES=("visual_odometry" "map_refinement" "relocalization" "rviz")

    for node in "${COMMON_NODES[@]}"; do
        if echo "$NODE_LIST" | grep -q "$node"; then
            echo "Killing node: $node"
            sudo docker exec "$CONTAINER_NAME" bash -c "source /opt/ros/noetic/setup.bash && rosnode kill /$node" 2>/dev/null || true
        fi
    done

    # Kill any remaining nodes (except rosout)
    REMAINING_NODES=$(sudo docker exec "$CONTAINER_NAME" bash -c "source /opt/ros/noetic/setup.bash && rosnode list 2>/dev/null | grep -v '/rosout'" 2>/dev/null || true)

    if [[ -n "$REMAINING_NODES" ]]; then
        echo ""
        echo "🎯 Killing remaining nodes..."
        echo "$REMAINING_NODES" | while read -r node; do
            if [[ -n "$node" ]]; then
                echo "Killing node: $node"
                sudo docker exec "$CONTAINER_NAME" bash -c "source /opt/ros/noetic/setup.bash && rosnode kill $node" 2>/dev/null || true
            fi
        done
    fi
fi

echo ""
echo "✅ ROS nodes cleanup completed!"

# Final check
FINAL_CHECK=$(sudo docker exec "$CONTAINER_NAME" bash -c "source /opt/ros/noetic/setup.bash && rosnode list 2>/dev/null | grep -v '/rosout'" 2>/dev/null || echo "NO_MASTER")

if [[ "$FINAL_CHECK" == "NO_MASTER" ]]; then
    echo "ℹ️  ROS master is no longer running"
elif [[ -z "$FINAL_CHECK" ]]; then
    echo "✅ All ROS nodes successfully killed"
else
    echo "⚠️  Some nodes may still be running:"
    echo "$FINAL_CHECK"
fi
