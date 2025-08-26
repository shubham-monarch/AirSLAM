#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


import cv2
from tqdm import tqdm

import pyzed.sl as sl

from .logger import LOGGER



def parse_args(argv: list[str] | None = None):
    p = argparse.ArgumentParser(description="Extract left images from SVO files")
    p.add_argument(
        "--input-file",
        required=True,
        type=Path,
        help="Path to the SVO file to extract frames from",
    )
    p.add_argument(
        "--output-dir",
        default="data/uncropped",
        type=Path,
        help="Output directory where frames will be written",
    )
    p.add_argument(
        "--svo-files-base",
        default="data/svo-files",
        type=Path,
        help="Base directory containing SVO files (used to calculate relative paths)",
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
    return p.parse_args(argv)





def ensure_cv2():  # pragma: no cover
    if cv2 is None:
        raise RuntimeError("OpenCV (cv2) is required to save images but is not installed.")


def extract_frames(svo_file: Path, rel_path: Path, output_dir: Path, resolution: str = "640,480", frame_step: int = 10):
    """Extract left and right images from *svo_file* into *output_dir / rel_path / cam0/data* and *cam1/data*"""
    ensure_cv2()

    LOGGER.info(f"Extracting frames from {svo_file}")

    zed = sl.Camera()

    init_params = sl.InitParameters(sdk_verbose=False)

    # Disable depth for faster decode
    if hasattr(sl.DEPTH_MODE, "NONE"):
        init_params.depth_mode = sl.DEPTH_MODE.NONE  # type: ignore[attr-defined]
    # Point to SVO
    init_params.set_from_svo_file(str(svo_file))  # type: ignore[attr-defined]

    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:  # type: ignore[attr-defined]
        raise RuntimeError(f"Failed to open {svo_file}: {status}")

    # Prepare output directory structure: output_dir/rel_path/cam0/data and cam1/data
    base_dir = (output_dir / rel_path).with_suffix("")  # drop .svo
    cam0_dir = base_dir / "cam0" / "data"
    cam1_dir = base_dir / "cam1" / "data"

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
            desc=f"  {rel_path.name}",
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
                    LOGGER.warning(f"Failed to save left frame {saved_frame_id} for {rel_path}")
                if right_save_status != sl.ERROR_CODE.SUCCESS:  # type: ignore[attr-defined]
                    LOGGER.warning(f"Failed to save right frame {saved_frame_id} for {rel_path}")

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

    # Resolve paths (they may be relative)
    input_file: Path = args.input_file.expanduser().resolve()
    output_dir: Path = args.output_dir.expanduser().resolve()
    svo_files_base: Path = args.svo_files_base.expanduser().resolve()

    # Check if input file exists and has .svo extension
    if not input_file.exists():
        LOGGER.error(f"Input file does not exist: {input_file}")
        return

    if input_file.suffix.lower() != ".svo":
        LOGGER.error(f"Input file must have .svo extension: {input_file}")
        return

    # Find the relative path with respect to svo-files-base
    try:
        # Calculate relative path from svo-files-base to the input file
        rel_path = input_file.relative_to(svo_files_base)
        # Remove the .svo extension to get the directory name
        rel_path = rel_path.with_suffix("")
    except ValueError:
        # If the input file is not under svo-files-base, use just the filename
        LOGGER.warning(f"Input file {input_file} is not under {svo_files_base}. Using filename only.")
        rel_path = Path(input_file.stem)

    LOGGER.info(f"Processing {input_file}")

    start_time = time.perf_counter()
    try:
        n_frames = extract_frames(input_file, Path(rel_path), output_dir, args.resolution, args.frame_step)
    except Exception as exc:
        LOGGER.error(f"Failed to process {input_file}: {exc}")
        return

    duration = time.perf_counter() - start_time
    fps = n_frames / duration if duration else 0

    LOGGER.info(f"Done. Extracted {n_frames} frames in {duration:.1f}s ({fps:.1f} fps)")


if __name__ == "__main__":
    main()