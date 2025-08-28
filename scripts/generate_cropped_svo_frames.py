#!/usr/bin/env python3
"""
Crop AirSLAM data images by 55% along the height dimension.

For every `.png` in `data/airslam-data`, crop the image by removing 55% from the bottom
and write the cropped image to `data/airslam-data-cropped`, preserving the
relative directory structure.

Optimizations:
- Parallel I/O and processing using a bounded queue of workers
- Low PNG compression (default 1) for much faster writes
- Skips already-processed outputs (resume-friendly)
- Memory-efficient processing with bounded worker queue

GPU note: For this specific task, disk I/O and PNG encoding dominate runtime.
Image cropping is negligible on CPU. This script focuses on maximizing
I/O throughput; GPU is optional and typically unnecessary.
"""

from __future__ import annotations

import argparse
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future, as_completed
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Tuple

from PIL import Image
from tqdm import tqdm
import logging
import shutil

# Logger and colored warnings
LOGGER = logging.getLogger(__name__)
import coloredlogs
coloredlogs.install(
    level='INFO',
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    level_styles={'WARNING': {'color': 'yellow', 'bold': True}},
    field_styles={'asctime': {'color': 'cyan'}, 'levelname': {'bold': True}}
)


def list_pngs(root: Path) -> Iterator[Path]:
    """Yield all .png files under root (recursively)."""
    # Using os.walk avoids building a massive list in memory
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".png"):
                yield Path(dirpath) / name

def ensure_parent(path: Path) -> None:
    """Create parent directory of a path if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)


def crop_and_save_image(
    image_path: Path,
    output_path: Path,
    crop_percentage: float,
    png_compression: int,
) -> bool:
    """Crop image by percentage along height and save as PNG.

    Returns True on success.
    """
    try:
        # Open image
        img = Image.open(image_path)
        width, height = img.size

        # Calculate new height (crop from bottom)
        crop_height = int(height * (1 - crop_percentage/100))

        # Crop image (from top to crop_height)
        cropped_img = img.crop((0, 0, width, crop_height))

        # Handle different image modes for saving
        if cropped_img.mode == 'RGBA':
            # Convert RGBA to RGB for PNG compatibility (optional but consistent)
            cropped_img = cropped_img.convert('RGB')

        ensure_parent(output_path)

        # Save as PNG with specified compression
        if cropped_img.mode == 'RGB':
            # For RGB images, save as RGB PNG
            cropped_img.save(output_path, 'PNG', compress_level=png_compression)
        else:
            # For grayscale or other modes
            cropped_img.save(output_path, 'PNG', compress_level=png_compression)

        return True
    except Exception:
        return False


def worker_task(args: Tuple[str, str, float, int, bool]) -> Tuple[str, bool]:
    """Worker wrapper to be used by executors.

    Returns (output_path, success).
    """
    img_path_str, out_path_str, crop_percentage, compression, skip_existing = args
    img_path = Path(img_path_str)
    out_path = Path(out_path_str)

    if skip_existing and out_path.exists():
        return (out_path_str, True)

    ok = crop_and_save_image(img_path, out_path, crop_percentage, compression)
    return (out_path_str, ok)


def process_all(
    input_dir: Path,
    base_input_dir: Path,
    base_output_dir: Path,
    workers: int,
    use_processes: bool,
    png_compression: int,
    skip_existing: bool,
    max_pending: int,
    max_files: Optional[int],
    crop_percentage: float,
    overwrite: bool,
) -> None:
    """Main processing loop with a bounded queue of futures."""
    Executor = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
    submitted: List[Future] = []
    total_submitted = 0
    successes = 0
    failures = 0

    # Determine the per-sequence target root deterministically by mapping input_dir
    # target_root = _resolve_target_root_for_input_dir(input_dir, base_output_dir, input_dir_base)
    output_dir = base_output_dir / input_dir.relative_to(base_input_dir)

    LOGGER.warning("=======================")  
    LOGGER.warning(f"output_dir: {output_dir}")
    LOGGER.warning("=======================")
    
    # Handle overwrite behavior for the target_root only (not the entire base_output_dir)
    if output_dir.exists() and any(output_dir.iterdir()):
        if overwrite:
            LOGGER.warning(f"⚠️  OVERWRITING EXISTING DIRECTORY: {output_dir}")
            LOGGER.warning("All existing cropped images in this directory will be deleted!")
            shutil.rmtree(output_dir)
        else:
            LOGGER.warning("⚠️  SKIPPING CROPPING: Output directory already exists and is not empty")
            LOGGER.warning(f"Directory: {output_dir}")
            LOGGER.warning("Use --overwrite flag to delete existing images and re-process")
            return output_dir

    with Executor(max_workers=workers) as ex, tqdm(unit="img") as pbar:
        for img_path in list_pngs(input_dir):
            
            input_img_path = img_path
            output_img_path = output_dir / img_path.relative_to(input_dir)
            
            # out_path = resolve_output_path(img_path, input_dir, base_output_dir, input_dir_base)

            fut = ex.submit(
                worker_task,
                (str(input_img_path), str(output_img_path), float(crop_percentage), int(png_compression), bool(skip_existing)),
            )
            submitted.append(fut)
            total_submitted += 1

            # Bounded in-flight futures to cap memory
            if len(submitted) >= max_pending:
                for done in as_completed(submitted[: workers]):
                    _out_path_str, ok = done.result()
                    pbar.update(1)
                    successes += int(ok)
                    failures += int(not ok)
                    submitted.remove(done)

            if max_files is not None and total_submitted >= max_files:
                break

        # Drain remaining futures
        for done in as_completed(submitted):
            _out_path_str, ok = done.result()
            successes += int(ok)
            failures += int(not ok)
            tqdm.write("")  # flush
            pbar.update(1)

    LOGGER.info("=======================")
    LOGGER.info(f"Successful: {successes}")
    LOGGER.info(f"Failed: {failures}")
    LOGGER.info("=======================")

    return output_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Crop AirSLAM images by percentage along height and write cropped copies, "
            "preserving the directory structure."
        )
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Input directory containing images to crop (PNG files)\
            e.g. data/uncropped/chino_valley/2024_02_13/front/front_2024-02-13-09-47-14",
    )

    parser.add_argument(
        "--base-input-dir",
        type=Path,
        default=Path("data/uncropped"),
        help="Base input directory for cropped images \
            e.g. data/uncropped",
    )

    parser.add_argument(
        "--base-output-dir",
        type=Path,
        default=Path("data/cropped"),
        help="Base output directory for cropped images (PNG) \
            e.g. data/cropped",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If set, delete the output directory if it exists and is not empty",
    )

    parser.add_argument(
        "--crop-percentage",
        type=float,
        default=55.0,
        help="Percentage to crop from bottom (default: 55.0)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=max(os.cpu_count() or 8, 8),
        help="Number of parallel workers",
    )
    parser.add_argument(
        "--processes",
        action="store_true",
        help="Use process-based parallelism (faster for PNG encode). Default uses threads.",
    )
    parser.add_argument(
        "--compression",
        type=int,
        default=1,
        help="PNG compression level (0=none, 9=max). Lower is faster.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip images whose outputs already exist (resume)",
    )
    parser.add_argument(
        "--max-pending",
        type=int,
        default=4096,
        help="Max in-flight tasks to bound memory",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Optionally limit number of images for testing",
    )

    # Robust machine-readable output for callers (e.g., bash)
    parser.add_argument(
        "--output-dir-outfile",
        type=Path,
        default=Path("/tmp/airslam_cropped_output_dir.txt"),
        help="File to write the resolved output directory path to (single line). Default: /tmp/airslam_cropped_output_dir.txt",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    LOGGER.warning("=======================")
    for k, v in vars(args).items():
        LOGGER.warning(f"{k}: {v}")
    LOGGER.warning("=======================")

    output_dir = process_all(
        input_dir=args.input_dir,
        base_input_dir=args.base_input_dir,
        base_output_dir=args.base_output_dir,
        workers=args.workers,
        use_processes=bool(args.processes),
        png_compression=int(args.compression),
        skip_existing=bool(args.skip_existing),
        max_pending=int(args.max_pending),
        max_files=args.max_files,
        crop_percentage=float(args.crop_percentage),
        overwrite=bool(getattr(args, 'overwrite', False)),
    )

    # Write the resolved output directory to an outfile (single line)
    try:
        # Delete existing file if it exists
        if args.output_dir_outfile.exists():
            args.output_dir_outfile.unlink()

        # Ensure parent directory exists
        args.output_dir_outfile.parent.mkdir(parents=True, exist_ok=True)

        # Write the output directory path
        args.output_dir_outfile.write_text(str(output_dir))
    except Exception as exc:
        LOGGER.error(f"Failed to write output dir to {args.output_dir_outfile}: {exc}")

    return output_dir


if __name__ == "__main__":
    main()
