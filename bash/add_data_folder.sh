#!/bin/bash

# Script to create a symlink from a data folder to the AirSLAM data directory
# Usage: ./add_data_folder.sh /absolute/path/to/source/folder
#        ./add_data_folder.sh --path /absolute/path/to/source/folder

# Function to display usage information
show_usage() {
    echo "Usage: $0 [OPTIONS] /absolute/path/to/source/folder"
    echo "       $0 --path /absolute/path/to/source/folder"
    echo ""
    echo "Options:"
    echo "  --path PATH    Absolute path to the source folder"
    echo "  --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 /home/user/data/dataset1"
    echo "  $0 --path /home/user/data/dataset1"
}

# Parse command line arguments
SOURCE_PATH=""
USE_FLAG=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --path)
            if [ -z "$2" ] || [[ "$2" == --* ]]; then
                echo "Error: --path requires a value"
                show_usage
                exit 1
            fi
            SOURCE_PATH="$2"
            USE_FLAG=true
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        -*)
            echo "Error: Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            # If we already have a path from --path flag, this is an extra argument
            if [ -n "$SOURCE_PATH" ]; then
                echo "Error: Too many arguments"
                show_usage
                exit 1
            fi
            SOURCE_PATH="$1"
            shift
            ;;
    esac
done

# Validate that we have exactly one path
if [ -z "$SOURCE_PATH" ]; then
    echo "Error: No source path provided"
    show_usage
    exit 1
fi
DATA_DIR="/media/skumar/External/catkin_ws/src/AirSLAM/data"

# Check if the source path exists and is a directory
if [ ! -d "$SOURCE_PATH" ]; then
    echo "Error: Source path '$SOURCE_PATH' does not exist or is not a directory"
    exit 1
fi

# Check if the data directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "Error: Data directory '$DATA_DIR' does not exist"
    exit 1
fi

# Get the basename of the source folder for the symlink name
FOLDER_NAME=$(basename "$SOURCE_PATH")

# Create the symlink
SYMLINK_PATH="$DATA_DIR/$FOLDER_NAME"

if [ -e "$SYMLINK_PATH" ]; then
    echo "Warning: '$SYMLINK_PATH' already exists. Removing it first."
    rm -rf "$SYMLINK_PATH"
fi

ln -s "$SOURCE_PATH" "$SYMLINK_PATH"

if [ $? -eq 0 ]; then
    echo "Success: Created symlink '$SYMLINK_PATH' -> '$SOURCE_PATH'"
else
    echo "Error: Failed to create symlink"
    exit 1
fi
