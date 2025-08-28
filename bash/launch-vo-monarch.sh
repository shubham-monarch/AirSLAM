#!/bin/bash

# Launch Visual Odometry Monarch Script
# This script prepares SVO data and launches the monarch visual odometry node
#
# STEPS SUMMARY:
# 1. Parse command line arguments (--svo-file, --frame-step)
# 2. Validate SVO file existence and resolve absolute paths
# 3. Prepare SVO data using prepare-svo-data.sh script
# 4. Determine dataroot from cropped data directory
# 5. Source ROS and catkin workspace environments
# 6. Launch monarch visual odometry with roslaunch

set -e  # Exit on any error

# Function to print usage
usage() {
    echo "Usage: $0 --svo-file <path_to_svo_file> [OPTIONS]"
    echo ""
    echo "Required arguments:"
    echo "  --svo-file PATH      Path to the input SVO file (should be in data/svo-files/...)"
    echo ""
    echo "Optional arguments:"
    echo "  --frame-step N       Extract every Nth frame (default: 1)"
    echo "  --help               Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 --svo-file data/svo-files/test.svo --frame-step 5"
    exit 1
}

# Default values
SVO_FILE=""
FRAME_STEP=1

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
        --help)
            usage
            ;;
        *)
            echo "Unknown argument: $1"
            usage
            ;;
    esac
done

# Check if SVO file is provided
if [[ -z "$SVO_FILE" ]]; then
    echo "Error: --svo-file is required"
    usage
fi

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Resolve the SVO file path relative to the project root
if [[ "$SVO_FILE" == /* ]]; then
    # Absolute path
    SVO_FILE_ABS="$SVO_FILE"
else
    # Relative path - resolve from project root
    SVO_FILE_ABS="$PROJECT_ROOT/$SVO_FILE"
fi

# Check if SVO file exists
if [[ ! -f "$SVO_FILE_ABS" ]]; then
    echo "Error: SVO file does not exist: $SVO_FILE_ABS"
    exit 1
fi

echo "=== Launch VO Monarch Script ==="
echo "SVO File: $SVO_FILE"
echo "Frame Step: $FRAME_STEP"
echo ""

# Step 1: Prepare SVO data
echo "=== Step 1: Preparing SVO data ==="
cd "$SCRIPT_DIR"

./prepare-svo-data.sh \
    --svo-file "$SVO_FILE_ABS" \
    --frame-step "$FRAME_STEP"

echo "Data preparation completed successfully!"
echo ""



# Step 2: Determine the dataroot
echo "=== Step 2: Determining dataroot ==="

# Get the basename of the SVO file (without .svo extension)
SVO_BASENAME=$(basename "$SVO_FILE" .svo)

# The cropped data should be in data/cropped/{SVO_BASENAME}
DATAROOT="$PROJECT_ROOT/data/cropped/$SVO_BASENAME"

if [[ ! -d "$DATAROOT" ]]; then
    echo "Error: Cropped data directory not found: $DATAROOT"
    echo "Please check if the data preparation completed successfully."
    exit 1
fi

echo "Using dataroot: $DATAROOT"
echo ""

# Step 3: Launch monarch visual odometry
echo "=== Step 3: Launching monarch visual odometry ==="

# Source ROS setup if available
if [[ -f "/opt/ros/noetic/setup.bash" ]]; then
    source /opt/ros/noetic/setup.bash
    echo "Sourced ROS Noetic setup"
elif [[ -f "/opt/ros/melodic/setup.bash" ]]; then
    source /opt/ros/melodic/setup.bash
    echo "Sourced ROS Melodic setup"
else
    echo "Warning: Could not find ROS setup.bash. Make sure ROS is properly installed and sourced."
fi

# Source the catkin workspace setup
if [[ -f "$PROJECT_ROOT/../../../devel/setup.bash" ]]; then
    source "$PROJECT_ROOT/../../../devel/setup.bash"
    echo "Sourced catkin workspace setup"
else
    echo "Warning: Could not find catkin workspace setup.bash"
fi

# Launch the monarch visual odometry with the correct dataroot
echo "Launching monarch.launch with dataroot: $DATAROOT"

roslaunch air_slam monarch.launch \
    dataroot:="$DATAROOT"

echo ""
echo "✅ Visual odometry launch completed!"
