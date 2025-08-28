#!/bin/bash

# Prepare SVO Data Script
# This script takes an SVO file as input, extracts frames using extract_svo_frames.py,
# and then crops the images using crop_airslam_data.py
#
# IMPORTANT NOTES:
# - This script MUST be run from the src/AirSLAM directory
# - The script will automatically verify it's in the correct location
# - Variable names have been updated for clarity:
#   * SVO_FILES_BASE_DIR → UNCROPPED_INPUT_BASE_DIR
#   * UNCROPPED_BASE_DIR → UNCROPPED_OUTPUT_BASE_DIR
#   * CROPPED_BASE_DIR → CROPPED_OUTPUT_BASE_DIR
#   * OUTPUT_DIR argument has been removed (use specific base dir arguments instead)

set -e  # Exit on any error

# Early directory check and virtual environment setup
# Get the absolute path of the script directory and ensure we're in src/AirSLAM
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AIRSLAM_DIR="$(dirname "$SCRIPT_DIR")"

# Ensure we're running from the src/AirSLAM directory
cd "$AIRSLAM_DIR"

# Verify we're in the correct directory
if [[ ! -f "CMakeLists.txt" ]] || [[ ! -d "scripts" ]] || [[ ! -d "bash" ]]; then
    echo "Error: Script must be run from the src/AirSLAM directory"
    echo "Expected to find CMakeLists.txt, scripts/, and bash/ directories"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Set up virtual environment early
if [[ -f ".venv/bin/activate" ]]; then
    source .venv/bin/activate
    echo "Activated virtual environment"
else
    echo "Warning: Virtual environment not found at .venv/bin/activate"
    echo "Continuing with system Python..."
fi

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
    echo "  --overwrite          If set, overwrite existing extracted directory for this sequence"
    echo "  --help               Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 --svo-file data/svo-files/test.svo --frame-step 5 --crop-percentage 50.0"
    exit 1
}

# Default values
SVO_FILE=""
FRAME_STEP=10

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
        --overwrite)
            OVERWRITE=1
            shift 1
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



echo "===[prepare-svo-data.sh] Prepare SVO Data Script ==="
echo "Running from: $(pwd)"

# Step 1: Extract frames from SVO file
echo "===[prepare-svo-data.sh] Step 1: Extracting frames from SVO file ==="

echo "Running scripts/generate_uncropped_svo_frames.py..."
echo "--input-file: $SVO_FILE"
echo "--base-input-dir: $UNCROPPED_INPUT_BASE_DIR"
echo "--base-output-dir: $UNCROPPED_OUTPUT_BASE_DIR"
echo "--frame-step: $FRAME_STEP"
echo "--crop-percentage: $CROP_PERCENTAGE"
echo "--resolution: $RESOLUTION"
echo ""

# Use a temp file to receive the output dir from the extractor
OUTFILE="$(mktemp)"

python -m scripts.generate_uncropped_svo_frames \
    --input-file "$SVO_FILE" \
    --frame-step "$FRAME_STEP" \
    --resolution "$RESOLUTION" \
    --base-input-dir "$UNCROPPED_INPUT_BASE_DIR" \
    --base-output-dir "$UNCROPPED_OUTPUT_BASE_DIR" \
    --output-dir-outfile "$OUTFILE" \
    $( [[ "$OVERWRITE" -eq 1 ]] && echo "--overwrite" )

# Read back the directory
UNCROPPED_OUTPUT_DIR="$(cat "$OUTFILE")"
rm -f "$OUTFILE"

echo "Generated uncropped frames in: $UNCROPPED_OUTPUT_DIR"

# Verify the output directory was created successfully
if [[ -z "$UNCROPPED_OUTPUT_DIR" ]] || [[ ! -d "$UNCROPPED_OUTPUT_DIR" ]]; then
    echo "Error: Failed to generate uncropped frames or directory not found"
    exit 1
fi



# Step 2: Crop the extracted frames
echo "===[prepare-svo-data.sh] Step 2: Cropping extracted frames ==="

# Use a temp file to receive the cropped output dir from the cropping script
CROPPED_OUTFILE="$(mktemp)"

echo "Running scripts/generate_cropped_svo_frames.py..."
echo "--input-dir: $UNCROPPED_OUTPUT_DIR"
echo "--base-input-dir: $UNCROPPED_OUTPUT_BASE_DIR"
echo "--base-output-dir: $CROPPED_OUTPUT_BASE_DIR"
echo "--crop-percentage: $CROP_PERCENTAGE"
echo ""

python -m scripts.generate_cropped_svo_frames \
    --input-dir "$UNCROPPED_OUTPUT_DIR" \
    --base-input-dir "$UNCROPPED_OUTPUT_BASE_DIR" \
    --base-output-dir "$CROPPED_OUTPUT_BASE_DIR" \
    --output-dir-outfile "$CROPPED_OUTFILE" \
    $( [[ "$OVERWRITE" -eq 1 ]] && echo "--overwrite" )

# Read back the cropped directory
CROPPED_OUTPUT_DIR="$(cat "$CROPPED_OUTFILE")"
rm -f "$CROPPED_OUTFILE"

echo "Generated cropped frames in: $CROPPED_OUTPUT_DIR"

# Verify the cropped output directory was created successfully
if [[ -z "$CROPPED_OUTPUT_DIR" ]] || [[ ! -d "$CROPPED_OUTPUT_DIR" ]]; then
    echo "Error: Failed to generate cropped frames or directory not found: $CROPPED_OUTPUT_DIR"
    exit 1
fi

echo "Cropping completed successfully!"
echo ""

# Count images in both directories
UNCROPPED_COUNT=$(find "$UNCROPPED_OUTPUT_DIR" -name "*.png" 2>/dev/null | wc -l)
CROPPED_COUNT=$(find "$CROPPED_OUTPUT_DIR" -name "*.png" 2>/dev/null | wc -l)

# Display results in a table
echo ""
echo "+------------------+-------+"
echo "| Type             | Count |"
echo "+------------------+-------+"
printf "| Uncroped Images  | %-5d |\n" "$UNCROPPED_COUNT"
printf "| Cropped Images   | %-5d |\n" "$CROPPED_COUNT"
echo "+------------------+-------+"

# Verify counts match
if [[ "$UNCROPPED_COUNT" -ne "$CROPPED_COUNT" ]]; then
    echo ""
    echo "❌ ERROR: Image counts do not match!"
    echo "Expected: $UNCROPPED_COUNT cropped images, found: $CROPPED_COUNT"
    exit 1
fi

echo ""
echo "✅ SVO data preparation completed successfully!"
