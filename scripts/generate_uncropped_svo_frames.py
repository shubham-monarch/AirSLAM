#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
import shutil


import cv2
from tqdm import tqdm

import pyzed.sl as sl

from .logger import LOGGER

# Configure coloredlogs for better warning visibility
import coloredlogs
coloredlogs.install(
    level='INFO',
    logger=LOGGER,
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    level_styles={'WARNING': {'color': 'yellow', 'bold': True}},
    field_styles={'asctime': {'color': 'cyan'}, 'levelname': {'bold': True}}
)



def parse_args(argv: list[str] | None = None):
    p = argparse.ArgumentParser(description="Extract left images from SVO files")
    p.add_argument(
        "--input-file",
        required=True,
        type=Path,
        help="Path to the SVO file to extract frames from \
            e.g. data/svo-files/2025-08-29-10-00-00.svo",
    )

    p.add_argument(
        "--base-input-dir",
        default="data/svo-files",
        type=Path,
        help="Base input directory for SVO files \
            e.g. data/svo-files",
    )

    p.add_argument(
        "--base-output-dir",
        default="data/uncropped",
        type=Path,
        help="Base output directory where the frame extraction directory structure will be created \
            e.g. data/uncropped",
    )
   
    p.add_argument(
        "--resolution",
        default="640,480",
        help="Image resolution as 'width,height' (e.g., '640,480', '1920,1080')",
    )
    p.add_argument(
        "--frame-step",
        default=10,
        type=int,
        help="Extract every Nth frame (default: 10, meaning 1/10 of all frames)",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="If set, delete the output directory for this sequence if it already exists and is not empty",
    )
    return p.parse_args(argv)

def extract_frames(
    svo_file_path: Path,
    base_input_dir: Path,
    base_output_dir: Path,
    resolution: str = "640,480",
    frame_step: int = 10,
    overwrite: bool = False,
):
    """Extract left and right images from *svo_file* into *base_output_dir / rel_path / cam0/data* and *cam1/data*"""

    output_dir = base_output_dir / svo_file_path.relative_to(base_input_dir)

    LOGGER.warning("=======================")
    LOGGER.warning(f"Extracting frames from {svo_file_path} to {output_dir}")
    LOGGER.warning("=======================")

    zed = sl.Camera()

    init_params = sl.InitParameters(sdk_verbose=False)

    # Disable depth for faster decode
    if hasattr(sl.DEPTH_MODE, "NONE"):
        init_params.depth_mode = sl.DEPTH_MODE.NONE  # type: ignore[attr-defined]
    # Point to SVO
    init_params.set_from_svo_file(str(svo_file_path))  # type: ignore[attr-defined]

    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:  # type: ignore[attr-defined]
        raise RuntimeError(f"Failed to open {svo_file_path}: {status}")

    # Handle existing directory state
    if output_dir.exists():
        # Directory exists and may contain previous extraction
        if any(output_dir.iterdir()):
            if overwrite:
                LOGGER.warning(f"⚠️  OVERWRITING EXISTING DIRECTORY: {output_dir}")
                LOGGER.warning("All existing frames in this directory will be deleted!")
                shutil.rmtree(output_dir)
            else:
                LOGGER.warning(f"⚠️  SKIPPING EXTRACTION: Output directory already exists and is not empty")
                LOGGER.warning(f"Directory: {output_dir}")
                LOGGER.warning("Use --overwrite flag to delete existing frames and re-extract")
                return 0

    cam0_dir = output_dir / "cam0" / "data"
    cam1_dir = output_dir / "cam1" / "data"

    # Create output directories only after SVO is successfully opened
    cam0_dir.mkdir(parents=True, exist_ok=True)
    cam1_dir.mkdir(parents=True, exist_ok=True)

    total_frames: int | None = None
    if hasattr(zed, "get_svo_number_of_frames"):
        total_frames = zed.get_svo_number_of_frames()
        LOGGER.info(f"Total frames: {total_frames}")
    else:
        LOGGER.warning("Could not get total number of frames")
        total_frames = None


    mat_left = sl.Mat()
    mat_right = sl.Mat()
    runtime_params = sl.RuntimeParameters()

    # Create progress bar for current file
    if tqdm is not None:
        progress_it = tqdm(
            total=total_frames,
            unit="frame",
            desc=f"  {svo_file_path.name}",
            leave=False,
            position=1,  # Second line
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
        )
    else:
        progress_it = None

    frame_id = 0
    saved_frame_id = 0
    try:
        while True:
            # LOGGER.info(f"Grabbing frame {frame_id}")
            grab_status = zed.grab(runtime_params)
            if grab_status == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:  # type: ignore[attr-defined]
                break
            if grab_status != sl.ERROR_CODE.SUCCESS:  # type: ignore[attr-defined]
                continue  # skip errors – warn?

            # Only process every Nth frame based on frame_step parameter
            if frame_id % frame_step == 0:
                # LOGGER.info(f"Retrieving frame {frame_id}")
                # Parse resolution from string (e.g., "640,480")
                width, height = map(int, resolution.split(","))
                custom_res = sl.Resolution(width, height)

                # Extract LEFT frame
                zed.retrieve_image(mat_left, sl.VIEW.LEFT, resolution=custom_res)  # type: ignore[attr-defined]
                left_file = cam0_dir / f"{saved_frame_id:06d}.png"
                left_save_status = mat_left.write(str(left_file))

                # Extract RIGHT frame
                zed.retrieve_image(mat_right, sl.VIEW.RIGHT, resolution=custom_res)  # type: ignore[attr-defined]
                right_file = cam1_dir / f"{saved_frame_id:06d}.png"
                right_save_status = mat_right.write(str(right_file))

                # Check if both saves were successful
                if left_save_status != sl.ERROR_CODE.SUCCESS:  # type: ignore[attr-defined]
                    LOGGER.warning(f"Failed to save left frame {saved_frame_id} for {svo_file_path}")
                if right_save_status != sl.ERROR_CODE.SUCCESS:  # type: ignore[attr-defined]
                    LOGGER.warning(f"Failed to save right frame {saved_frame_id} for {svo_file_path}")

                if left_save_status == sl.ERROR_CODE.SUCCESS and right_save_status == sl.ERROR_CODE.SUCCESS:  # type: ignore[attr-defined]
                    saved_frame_id += 1
                    if tqdm is not None:
                        progress_it.update(1)

            frame_id += 1
    finally:
        if tqdm is not None and hasattr(progress_it, "close"):
            progress_it.close()
        zed.close()

    return saved_frame_id


def main(argv: list[str] | None = None):
    args = parse_args(argv)

    LOGGER.warning("=======================")
    for k, v in vars(args).items():
        LOGGER.warning(f"{k}: {v}")
    LOGGER.warning("=======================")


    # # Resolve paths (they may be relative)
    # input_file: Path = args.input_file.expanduser().resolve()
    # base_output_dir: Path = args.base_output_dir.expanduser().resolve()
    # # svo_files_base: Path = args.svo_files_base.expanduser().resolve()
    # overwrite: bool = bool(getattr(args, "overwrite", False))

    # Check if input file exists and has .svo extension
    if not args.input_file.exists():
        LOGGER.error(f"Input file does not exist: {input_file}")
        return

    if args.input_file.suffix.lower() != ".svo":
        LOGGER.error(f"Input file must have .svo extension: {args.input_file}")
        return

    # Find the relative path with respect to svo-files-base
    # try:
    #     # Calculate relative path from svo-files-base to the input file
    #     rel_path = input_file.relative_to(svo_files_base)
    #     # Remove the .svo extension to get the directory name
    #     rel_path = rel_path.with_suffix("")
    # except ValueError:
    #     # If the input file is not under svo-files-base, use just the filename
    #     LOGGER.warning(f"Input file {input_file} is not under {svo_files_base}. Using filename only.")
    #     rel_path = Path(input_file.stem)

    # LOGGER.info(f"Processing {input_file}")

    start_time = time.perf_counter()
    try:
        n_frames = extract_frames(
            args.input_file,
            args.base_input_dir,
            args.base_output_dir,
            args.resolution,
            args.frame_step,
            args.overwrite
        )
    except Exception as exc:
        LOGGER.error(f"Failed to process {args.input_file}: {exc}")
        return

    duration = time.perf_counter() - start_time
    fps = n_frames / duration if duration else 0

    LOGGER.info("=======================")
    LOGGER.info(f"Done. Extracted {n_frames} frames in {duration:.1f}s ({fps:.1f} fps)")
    LOGGER.info("=======================")


if __name__ == "__main__":
    main()