#!/bin/bash

# Docker version of the complete AirSLAM pipeline script
# Runs all three monarch scripts inside the air_slam Docker container

# Default values (matching launch-vo-monarch.sh defaults)
SVO_FILE=""
FRAME_STEP=1
UNCROPPED_INPUT_BASE_DIR="data/svo-files"
UNCROPPED_OUTPUT_BASE_DIR="data/uncropped"
CROPPED_OUTPUT_BASE_DIR="data/cropped"
CROP_PERCENTAGE=55.0
RESOLUTION="640,480"
OVERWRITE=0
CONTAINER_NAME="air_slam"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --svo-file)
            SVO_FILE="$2"
            shift 2
            ;;
        --frame-step)
            FRAME_STEP="$2"
            shift 2
            ;;
        --uncropped-input-base-dir)
            UNCROPPED_INPUT_BASE_DIR="$2"
            shift 2
            ;;
        --uncropped-output-base-dir)
            UNCROPPED_OUTPUT_BASE_DIR="$2"
            shift 2
            ;;
        --cropped-output-base-dir)
            CROPPED_OUTPUT_BASE_DIR="$2"
            shift 2
            ;;
        --crop-percentage)
            CROP_PERCENTAGE="$2"
            shift 2
            ;;
        --resolution)
            RESOLUTION="$2"
            shift 2
            ;;
        --overwrite)
            OVERWRITE=1
            shift 1
            ;;
        --container)
            CONTAINER_NAME="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 --svo-file <path_to_svo_file> [other options]"
            echo "Options:"
            echo "  --svo-file <file>              # Required: Path to SVO file"
            echo "  --frame-step <num>             # Default: 1"
            echo "  --container <name>             # Default: air_slam"
            echo "  --overwrite                    # Overwrite existing output"
            exit 1
            ;;
    esac
done

# Validate required parameter
if [[ -z "$SVO_FILE" ]]; then
    echo "Error: --svo-file is required"
    echo "Usage: $0 --svo-file <path_to_svo_file> [other options]"
    exit 1
fi

echo "==============================================="
echo "🐳 Docker AirSLAM Pipeline Starting"
echo "==============================================="
echo "SVO File: $SVO_FILE"
echo "Container: $CONTAINER_NAME"
echo "Frame Step: $FRAME_STEP"
echo "Overwrite: $OVERWRITE"
echo "==============================================="

# Check if container is running
if ! sudo docker ps --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Container '$CONTAINER_NAME' is not running."
    echo "Starting container..."
    sudo docker start "$CONTAINER_NAME"
    if [[ $? -ne 0 ]]; then
        echo "❌ Failed to start container '$CONTAINER_NAME'"
        exit 1
    fi
    echo "✅ Container '$CONTAINER_NAME' started successfully"
    # Give container time to fully start
    sleep 2
fi

# Build the command string for visual odometry
VO_CMD="cd /workspace/src/AirSLAM && bash bash/launch-vo-monarch.sh"
VO_CMD="$VO_CMD --svo-file \"$SVO_FILE\""
VO_CMD="$VO_CMD --frame-step $FRAME_STEP"
VO_CMD="$VO_CMD --uncropped-input-base-dir \"$UNCROPPED_INPUT_BASE_DIR\""
VO_CMD="$VO_CMD --uncropped-output-base-dir \"$UNCROPPED_OUTPUT_BASE_DIR\""
VO_CMD="$VO_CMD --cropped-output-base-dir \"$CROPPED_OUTPUT_BASE_DIR\""
VO_CMD="$VO_CMD --crop-percentage $CROP_PERCENTAGE"
VO_CMD="$VO_CMD --resolution \"$RESOLUTION\""
if [[ "$OVERWRITE" -eq 1 ]]; then
    VO_CMD="$VO_CMD --overwrite"
fi

# Step 1: Visual Odometry
echo ""
echo "==============================================="
echo "📹 Step 1: Running Visual Odometry in Docker"
echo "==============================================="

sudo docker exec "$CONTAINER_NAME" bash -c "$VO_CMD"
VO_EXIT_CODE=$?

# Check if visual odometry completed successfully
if [[ $VO_EXIT_CODE -ne 0 ]]; then
    echo "❌ Visual Odometry failed with exit code $VO_EXIT_CODE. Stopping pipeline."
    exit 1
fi

echo ""
echo "✅ Visual Odometry completed successfully!"

# Step 2: Map Refinement
echo ""
echo "==============================================="
echo "🔧 Step 2: Running Map Refinement in Docker"
echo "==============================================="

sudo docker exec "$CONTAINER_NAME" bash -c "cd /workspace/src/AirSLAM && bash bash/launch-map-refinement-monarch.sh"
MR_EXIT_CODE=$?

# Check if map refinement completed successfully
if [[ $MR_EXIT_CODE -ne 0 ]]; then
    echo "❌ Map Refinement failed with exit code $MR_EXIT_CODE. Stopping pipeline."
    exit 1
fi

echo ""
echo "✅ Map Refinement completed successfully!"

# Step 3: Relocalization
echo ""
echo "==============================================="
echo "📍 Step 3: Running Relocalization in Docker"
echo "==============================================="

sudo docker exec "$CONTAINER_NAME" bash -c "cd /workspace/src/AirSLAM && bash bash/launch-relocalization-monarch.sh --svo-file \"$SVO_FILE\""
RELOC_EXIT_CODE=$?

# Check if relocalization completed successfully
if [[ $RELOC_EXIT_CODE -ne 0 ]]; then
    echo "❌ Relocalization failed with exit code $RELOC_EXIT_CODE."
    exit 1
fi

echo ""
echo "✅ Relocalization completed successfully!"

echo ""
echo "==============================================="
echo "🎉 Complete AirSLAM Pipeline in Docker finished successfully!"
echo "==============================================="
