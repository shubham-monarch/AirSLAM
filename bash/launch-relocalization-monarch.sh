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
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 --svo-file <path_to_svo_file>"
            exit 1
            ;;
    esac
done

# Check if SVO_FILE is provided
if [[ -z "$SVO_FILE" ]]; then
    echo "Error: --svo-file is required"
    echo "Usage: $0 --svo-file <path_to_svo_file>"
    exit 1
fi



# Step 1: Prepare SVO data
echo "=== [launch-relocalization-monarch.sh] Step 1: calling prepare-svo-data.sh ==="

./bash/prepare-svo-data.sh \
    --svo-file "$SVO_FILE" \
    --frame-step "$FRAME_STEP"

# Step 2: Determine the dataroot args for monarch.launch
echo "=== [launch-relocalization-monarch.sh] Step 2: Determining dataroot args for monarch.launch ==="

# Calculate relative path of SVO_FILE w.r.t. UNCROPPED_INPUT_BASE_DIR
# Remove UNCROPPED_INPUT_BASE_DIR prefix from SVO_FILE path
RELATIVE_PATH=${SVO_FILE#$UNCROPPED_INPUT_BASE_DIR/}

# Append relative path to CROPPED_OUTPUT_BASE_DIR and workspace/src/AirSLAM
DATAROOT="/workspace/src/AirSLAM/$CROPPED_OUTPUT_BASE_DIR/$RELATIVE_PATH/cam0/data"



# Step 3: Launch monarch relocalization
echo "=== [launch-relocalization-monarch.sh] Step 3: Launching monarch relocalization ==="

source /opt/ros/noetic/setup.bash
source ../../devel/setup.bash

# Launch the monarch relocalization with the correct dataroot
echo "Launching monarch.launch with dataroot: $DATAROOT"

roslaunch /workspace/src/AirSLAM/launch/relocalization/monarch.launch \
    dataroot:="$DATAROOT"

echo ""
echo "✅ Relocalization launch completed!"
