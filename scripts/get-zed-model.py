#!/usr/bin/env python3
"""
Script to print the ZED camera model information from an SVO file.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

import pyzed.sl as sl

from .logger import LOGGER


def parse_args(argv: Optional[List[str]] = None):
    """Parse command line arguments."""
    p = argparse.ArgumentParser(description="Print ZED camera model information from SVO file")
    p.add_argument(
        "--input-file",
        required=True,
        type=Path,
        help="Path to the SVO file to read camera model from \
            e.g. data/svo-files/2025-08-29-10-00-00.svo",
    )
    return p.parse_args(argv)


def print_camera_model(svo_file_path: Path):
    """Print the camera model information from the SVO file."""

    if not svo_file_path.exists():
        LOGGER.error(f"SVO file does not exist: {svo_file_path}")
        return False

    # Create camera object
    zed = sl.Camera()

    # Set up initialization parameters
    init_params = sl.InitParameters()
    init_params.sdk_verbose = 0  # Reduce SDK verbosity (0 = silent, 1 = error, 2 = warning, 3 = info, 4 = debug)

    # Point to SVO file
    init_params.set_from_svo_file(str(svo_file_path))  # type: ignore[attr-defined]

    # Open the camera from SVO file
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        LOGGER.error(f"Failed to open SVO file {svo_file_path}: {status}")
        return False

    try:
        # Get camera information
        camera_info = zed.get_camera_information()

        # Print camera model
        camera_model = camera_info.camera_model
        LOGGER.info(f"Camera Model: {camera_model}")

        # Print additional camera information (with error handling for missing attributes)
        try:
            if hasattr(camera_info, 'camera_firmware_version'):
                LOGGER.info(f"Camera Firmware: {camera_info.camera_firmware_version}")
        except:
            LOGGER.info("Camera Firmware: Not available")

        try:
            if hasattr(camera_info, 'serial_number'):
                LOGGER.info(f"Serial Number: {camera_info.serial_number}")
        except:
            LOGGER.info("Serial Number: Not available")

        return True

    except Exception as e:
        LOGGER.error(f"Error retrieving camera information: {e}")
        return False

    finally:
        # Close the camera
        zed.close()


def main():
    """Main function to run the camera model printing script."""
    args = parse_args()

    LOGGER.info("Starting ZED Camera Model Detection from SVO file")
    LOGGER.info("=" * 50)
    LOGGER.info(f"SVO File: {args.input_file}")
    LOGGER.info("=" * 50)

    success = print_camera_model(args.input_file)

    LOGGER.info("=" * 50)
    if success:
        LOGGER.info("✅ Camera model detection completed successfully")
    else:
        LOGGER.error("❌ Failed to detect camera model")
        sys.exit(1)


if __name__ == "__main__":
    main()
