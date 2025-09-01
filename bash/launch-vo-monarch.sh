#!/bin/bash



# Default values
SVO_FILE=""
FRAME_STEP=1

UNCROPPED_INPUT_BASE_DIR="data/svo-files"
UNCROPPED_OUTPUT_BASE_DIR="data/uncropped"

CROPPED_OUTPUT_BASE_DIR="data/cropped"
CROP_PERCENTAGE=55.0
RESOLUTION="640,480"
OVERWRITE=0

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
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done



# Step 1: Prepare SVO data
echo "=== [launch-vo-monarch.sh] Step 1: calling prepare-svo-data.sh ==="
echo "OVERWRITE variable value: $OVERWRITE"

./bash/prepare-svo-data.sh \
    --svo-file "$SVO_FILE" \
    --frame-step "$FRAME_STEP" \
    $( [[ "$OVERWRITE" -eq 1 ]] && echo "--overwrite" )

# Step 2: Determine the dataroot args for monarch.launch
echo "=== [launch-vo-monarch.sh] Step 2: Determining dataroot args for monarch.launch ==="

# Calculate relative path of SVO_FILE w.r.t. UNCROPPED_INPUT_BASE_DIR
# Remove UNCROPPED_INPUT_BASE_DIR prefix from SVO_FILE path
RELATIVE_PATH=${SVO_FILE#$UNCROPPED_INPUT_BASE_DIR/}

# Append relative path to CROPPED_OUTPUT_BASE_DIR and workspace/src/AirSLAM
DATAROOT="/workspace/src/AirSLAM/$CROPPED_OUTPUT_BASE_DIR/$RELATIVE_PATH"



# Step 3: Launch monarch visual odometry
echo "=== [launch-vo-monarch.sh] Step 3: Launching monarch visual odometry ==="

source /opt/ros/noetic/setup.bash
source ../../devel/setup.bash

# Launch the monarch visual odometry with the correct dataroot
echo "Launching monarch.launch with dataroot: $DATAROOT"

roslaunch /workspace/src/AirSLAM/launch/visual_odometry/monarch.launch \
    dataroot:="$DATAROOT"

echo ""
echo "✅ Visual odometry launch completed!"
