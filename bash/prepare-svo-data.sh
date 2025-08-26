#!/bin/bash

# Prepare SVO Data Script
# This script takes an SVO file as input, extracts frames using extract_svo_frames.py,
# and then crops the images using crop_airslam_data.py

set -e  # Exit on any error

# Function to print usage
usage() {
    echo "Usage: $0 --svo-file <path_to_svo_file> [OPTIONS]"
    echo ""
    echo "Required arguments:"
    echo "  --svo-file PATH      Path to the input SVO file (should be in format: data/svo-files/...)"
    echo ""
    echo "Optional arguments:"
    echo "  --output-dir DIR     Base output directory (default: data)"
    echo "  --frame-step N       Extract every Nth frame (default: 10)"
    echo "  --crop-percentage P  Crop percentage for cropping script (default: 55.0)"
    echo "  --resolution W,H     Image resolution (default: 640,480)"
    echo "  --help               Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 --svo-file data/svo-files/test.svo --frame-step 5 --crop-percentage 50.0"
    exit 1
}

# Default values
SVO_FILE=""
OUTPUT_DIR="data"
FRAME_STEP=10
CROP_PERCENTAGE=55.0
RESOLUTION="640,480"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --svo-file)
            SVO_FILE="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --frame-step)
            FRAME_STEP="$2"
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

# Check if SVO file exists
if [[ ! -f "$SVO_FILE" ]]; then
    echo "Error: SVO file does not exist: $SVO_FILE"
    exit 1
fi

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Prepare SVO Data Script ==="
echo "SVO File: $SVO_FILE"
echo "Output Directory: $OUTPUT_DIR"
echo "Frame Step: $FRAME_STEP"
echo "Crop Percentage: $CROP_PERCENTAGE"
echo "Resolution: $RESOLUTION"
echo ""

# Step 1: Extract frames from SVO file
echo "=== Step 1: Extracting frames from SVO file ==="
cd "$PROJECT_ROOT"

if [[ -f ".venv/bin/activate" ]]; then
    source .venv/bin/activate
    echo "Activated virtual environment"
else
    echo "Warning: Virtual environment not found at .venv/bin/activate"
    echo "Continuing with system Python..."
fi

echo "Running extract_svo_frames.py..."
python -m scripts.extract_svo_frames \
    --input-file "$SVO_FILE" \
    --output-dir "$OUTPUT_DIR/uncropped" \
    --svo-files-base "data/svo-files" \
    --frame-step "$FRAME_STEP" \
    --resolution "$RESOLUTION"

echo "Frame extraction completed successfully!"
echo ""

# Step 2: Crop the extracted frames
echo "=== Step 2: Cropping extracted frames ==="

# Find the extracted folder (it should be under uncropped with the SVO file's relative path)
SVO_BASENAME=$(basename "$SVO_FILE" .svo)

# Try to find the extracted folder
EXTRACTED_DIR=""
if [[ -d "$OUTPUT_DIR/uncropped/$SVO_BASENAME" ]]; then
    EXTRACTED_DIR="$OUTPUT_DIR/uncropped/$SVO_BASENAME"
else
    # Try to find any directory under uncropped that might contain our frames
    UNCROPPED_CONTENTS=$(find "$OUTPUT_DIR/uncropped" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | head -1)
    if [[ -n "$UNCROPPED_CONTENTS" ]]; then
        EXTRACTED_DIR="$UNCROPPED_CONTENTS"
    fi
fi

if [[ -z "$EXTRACTED_DIR" ]]; then
    echo "Error: Could not find extracted frames directory"
    echo "Looking for directories in: $OUTPUT_DIR/uncropped"
    ls -la "$OUTPUT_DIR/uncropped" 2>/dev/null || echo "Directory not found or empty"
    exit 1
fi

echo "Found extracted frames in: $EXTRACTED_DIR"
echo "Running crop_airslam_data.py..."

python -m scripts.crop_airslam_data \
    --input-dir "$EXTRACTED_DIR" \
    --output-dir "$OUTPUT_DIR/cropped" \
    --crop-percentage "$CROP_PERCENTAGE"

echo "Cropping completed successfully!"
echo ""

# Summary
echo "=== Processing Complete ==="
echo "Input SVO: $SVO_FILE"
echo "Uncropped frames: $EXTRACTED_DIR"
echo "Cropped frames: $OUTPUT_DIR/cropped"

# Count the number of frames
UNCROPPED_COUNT=$(find "$EXTRACTED_DIR" -name "*.png" 2>/dev/null | wc -l)
CROPPED_COUNT=$(find "$OUTPUT_DIR/cropped" -name "*.png" 2>/dev/null | wc -l)

echo "Uncropped images: $UNCROPPED_COUNT"
echo "Cropped images: $CROPPED_COUNT"
echo ""
echo "✅ SVO data preparation completed successfully!"
