#!/bin/bash

# Script to create a symlink from a source folder to a specified destination directory
# Usage: ./add_data_folder.sh --src /absolute/path/to/source/folder [--dest relative/path/in/data/folder]
#        ./add_data_folder.sh /absolute/path/to/source/folder  # for backward compatibility

# Function to display usage information
show_usage() {
    echo "Usage: $0 --src /absolute/path/to/source/folder [--dest relative/path/in/data/folder]"
    echo "       $0 [OPTIONS] /absolute/path/to/source/folder"
    echo ""
    echo "Options:"
    echo "  --src PATH     Absolute path to the source folder (required)"
    echo "  --dest DIR     Relative path within AirSLAM data folder (default: data folder root)"
    echo "  --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --src /home/user/data/dataset1"
    echo "  $0 --src /home/user/data/dataset1 --dest unmasked"
    echo "  $0 --src /home/user/data/dataset1 --dest processed/raw"
    echo "  $0 /home/user/data/dataset1  # Positional argument for backward compatibility"
}

# Parse command line arguments
SRC_PATH=""
DEST_DIR=""
USE_FLAG=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --src)
            if [ -z "$2" ] || [[ "$2" == --* ]]; then
                echo "Error: --src requires a value"
                show_usage
                exit 1
            fi
            SRC_PATH="$2"
            USE_FLAG=true
            shift 2
            ;;
        --dest)
            if [ -z "$2" ] || [[ "$2" == --* ]]; then
                echo "Error: --dest requires a value"
                show_usage
                exit 1
            fi
            DEST_DIR="$2"
            shift 2
            ;;
        --path)
            echo "Warning: --path is deprecated, use --src instead"
            if [ -z "$2" ] || [[ "$2" == --* ]]; then
                echo "Error: --path requires a value"
                show_usage
                exit 1
            fi
            SRC_PATH="$2"
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
            # If we already have a path from --src or --path flag, this is an extra argument
            if [ -n "$SRC_PATH" ]; then
                echo "Error: Too many arguments"
                show_usage
                exit 1
            fi
            SRC_PATH="$1"
            shift
            ;;
    esac
done

# Validate that we have a source path
if [ -z "$SRC_PATH" ]; then
    echo "Error: No source path provided"
    show_usage
    exit 1
fi

# Set default destination directory
DEFAULT_DATA_DIR="/media/skumar/External/catkin_ws/src/AirSLAM/data"

# Handle destination directory
if [ -z "$DEST_DIR" ]; then
    DEST_DIR="$DEFAULT_DATA_DIR"
else
    # If DEST_DIR is provided, treat it as relative to the default data directory
    DEST_DIR="$DEFAULT_DATA_DIR/$DEST_DIR"
fi

# Check if the source path exists and is a directory
if [ ! -d "$SRC_PATH" ]; then
    echo "Error: Source path '$SRC_PATH' does not exist or is not a directory"
    exit 1
fi

# Check if the destination directory exists
if [ ! -d "$DEST_DIR" ]; then
    echo "Error: Destination directory '$DEST_DIR' does not exist"
    exit 1
fi

# Get the basename of the source folder for the symlink name
FOLDER_NAME=$(basename "$SRC_PATH")

# Create the symlink
SYMLINK_PATH="$DEST_DIR/$FOLDER_NAME"

if [ -e "$SYMLINK_PATH" ]; then
    echo "Warning: '$SYMLINK_PATH' already exists. Removing it first."
    rm -rf "$SYMLINK_PATH"
fi

ln -s "$SRC_PATH" "$SYMLINK_PATH"

if [ $? -eq 0 ]; then
    echo "Success: Created symlink '$SYMLINK_PATH' -> '$SRC_PATH'"
else
    echo "Error: Failed to create symlink"
    exit 1
fi
