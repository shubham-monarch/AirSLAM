#!/bin/bash

# Run launch-vo-monarch.sh inside Docker container
# Supports all flags from launch-vo-monarch.sh:
#   --svo-file <file>                    # Required: Path to SVO file
#   --frame-step <num>                   # Default: 1
#   --uncropped-input-base-dir <dir>     # Default: data/svo-files
#   --uncropped-output-base-dir <dir>    # Default: data/uncropped
#   --cropped-output-base-dir <dir>      # Default: data/cropped
#   --crop-percentage <pct>              # Default: 55.0
#   --resolution <w,h>                   # Default: 640,480
#   --overwrite                          # Overwrite existing output
#   --help                               # Show usage
#
# Examples:
#   # Basic usage with default settings
#   bash/launch-docker-container-docker.sh --svo-file data/svo-files/chino_valley/2024_02_13/front/front_2024-02-13-09-47-14.svo
#
#   # Custom frame extraction and cropping
#   bash/launch-docker-container-docker.sh --svo-file data/svo-files/chino_valley/2024_02_13/front/front_2024-02-13-09-47-14.svo --frame-step 10 --crop-percentage 60.0
#
#   # High resolution with overwrite
#   bash/launch-docker-container-docker.sh --svo-file data/svo-files/chino_valley/2024_02_13/front/front_2024-02-13-09-47-14.svo --resolution 1280,720 --overwrite
#
#   # Custom output directories
#   bash/launch-docker-container-docker.sh --svo-file data/svo-files/test/test.svo --uncropped-output-base-dir data/test_uncropped --cropped-output-base-dir data/test_cropped

sudo docker exec -it air_slam bash -c "cd /workspace/src/AirSLAM && bash bash/launch-vo-monarch.sh $@"

echo "✅ Docker visual odometry launch completed successfully!"
