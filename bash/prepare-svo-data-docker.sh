#!/bin/bash

# Run SVO data preparation inside Docker container
# Supports all flags from prepare-svo-data.sh:
#   --svo-file <file>                    # Required: Path to SVO file
#   --uncropped-input-base-dir <dir>     # Default: data/svo-files
#   --uncropped-output-base-dir <dir>    # Default: data/uncropped
#   --cropped-output-base-dir <dir>      # Default: data/cropped
#   --frame-step <num>                   # Default: 10
#   --crop-percentage <pct>              # Default: 55.0
#   --resolution <w,h>                   # Default: 640,480
#   --overwrite                          # Overwrite existing output
#   --help                               # Show usage
#
# Examples:
#   # Basic usage with default settings
#   bash/prepare-svo-data-docker.sh --svo-file data/svo-files/open_sky/2024_08_19/front_2024-08-19-20-02-29.svo
#
#   # Custom frame extraction and cropping
#   bash/prepare-svo-data-docker.sh --svo-file data/svo-files/open_sky/2024_08_19/front_2024-08-19-20-02-29.svo --frame-step 5 --crop-percentage 60.0
#
#   # High resolution with overwrite
#   bash/prepare-svo-data-docker.sh --svo-file data/svo-files/open_sky/2024_08_19/front_2024-08-19-20-02-29.svo --resolution 1280,720 --overwrite
#
#   # Custom output directories
#   bash/prepare-svo-data-docker.sh --svo-file data/svo-files/test/test.svo --uncropped-output-base-dir data/test_uncropped --cropped-output-base-dir data/test_cropped

sudo docker exec -it air_slam_modified bash -c "cd /workspace/src/AirSLAM && bash bash/prepare-svo-data.sh $@"

echo "✅ Docker SVO data preparation completed successfully!"
