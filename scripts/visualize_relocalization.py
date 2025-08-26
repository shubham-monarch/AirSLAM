#!/usr/bin/env python3

"""
Visualize relocalization results stored in debug/relocalization.txt.

The expected file format is one record per line:
  [status] [frame_id] [tx] [ty] [tz] [qx] [qy] [qz] [qw]

Where:
  - status: one of {base, success, fail}
  - frame_id: zero-padded image/frame index
  - tx, ty, tz: translation in meters
  - qx, qy, qz, qw: quaternion orientation

This script renders a 3D scatter/line plot for the camera trajectory where
successful relocalizations are highlighted, failed attempts are shown as faint
markers, and the base/reference pose is called out.

Usage examples:
  python src/AirSLAM/scripts/visualize_relocalization.py \
    --file src/AirSLAM/debug/relocalization.txt

  python src/AirSLAM/scripts/visualize_relocalization.py \
    --file /absolute/path/to/relocalization.txt --save Figure.png
"""

import argparse
import os
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (required for 3D projection)


@dataclass
class RelocalizationRecord:
    status: str
    frame_id: str
    translation: Tuple[float, float, float]
    quaternion: Tuple[float, float, float, float]


def parse_relocalization_file(file_path: str) -> List[RelocalizationRecord]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    records: List[RelocalizationRecord] = []
    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 10:
                # Unexpected line format, skip politely
                continue

            status, frame_id = parts[0], parts[1]
            try:
                tx, ty, tz = float(parts[2]), float(parts[3]), float(parts[4])
                qx, qy, qz, qw = (
                    float(parts[5]),
                    float(parts[6]),
                    float(parts[7]),
                    float(parts[8]),
                )
            except ValueError:
                # Skip malformed numeric entries
                continue

            records.append(
                RelocalizationRecord(
                    status=status,
                    frame_id=frame_id,
                    translation=(tx, ty, tz),
                    quaternion=(qx, qy, qz, qw),
                )
            )

    return records


def compute_stats(records: List[RelocalizationRecord]) -> Tuple[int, int, float]:
    total_attempts = 0
    successes = 0
    for r in records:
        if r.status in {"success", "fail"}:
            total_attempts += 1
            if r.status == "success":
                successes += 1
    recall = (successes / total_attempts) if total_attempts > 0 else 0.0
    return total_attempts, successes, recall


def visualize(records: List[RelocalizationRecord], title: str, save_path: str = "") -> None:
    xs_success, ys_success, zs_success = [], [], []
    xs_fail, ys_fail, zs_fail = [], [], []
    xs_all, ys_all, zs_all = [], [], []
    base_point = None

    for r in records:
        x, y, z = r.translation
        xs_all.append(x)
        ys_all.append(y)
        zs_all.append(z)
        if r.status == "base":
            base_point = (x, y, z)
        elif r.status == "success":
            xs_success.append(x)
            ys_success.append(y)
            zs_success.append(z)
        elif r.status == "fail":
            xs_fail.append(x)
            ys_fail.append(y)
            zs_fail.append(z)

    total_attempts, successes, recall = compute_stats(records)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Plot overall path as a light line for context
    if xs_all:
        ax.plot(xs_all, ys_all, zs_all, color="#cccccc", linewidth=1.0, label="Path (all)")

    # Plot successes and failures
    if xs_success:
        ax.scatter(xs_success, ys_success, zs_success, c="#2ca02c", s=12, label="Success")
    if xs_fail:
        ax.scatter(xs_fail, ys_fail, zs_fail, c="#d62728", s=10, alpha=0.6, label="Fail")

    if base_point is not None:
        ax.scatter([base_point[0]], [base_point[1]], [base_point[2]], c="#1f77b4", s=50, marker="*", label="Base")

    ax.set_title(f"Relocalization Results: {title}\nAttempts={total_attempts}, Successes={successes}, Recall={recall:.3f}")
    ax.set_xlabel("tx [m]")
    ax.set_ylabel("ty [m]")
    ax.set_zlabel("tz [m]")
    ax.legend(loc="best")
    ax.grid(True)

    # Make axes equal scale for better spatial interpretation
    try:
        x_limits = (min(xs_all), max(xs_all)) if xs_all else (-1, 1)
        y_limits = (min(ys_all), max(ys_all)) if ys_all else (-1, 1)
        z_limits = (min(zs_all), max(zs_all)) if zs_all else (-1, 1)
        max_range = max(
            x_limits[1] - x_limits[0],
            y_limits[1] - y_limits[0],
            z_limits[1] - z_limits[0],
        )
        if max_range > 0:
            x_mid = sum(x_limits) / 2.0
            y_mid = sum(y_limits) / 2.0
            z_mid = sum(z_limits) / 2.0
            half = max_range / 2.0
            ax.set_xlim(x_mid - half, x_mid + half)
            ax.set_ylim(y_mid - half, y_mid + half)
            ax.set_zlim(z_mid - half, z_mid + half)
    except Exception:
        # Keep default limits if any issue arises
        pass

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200)
    else:
        plt.show()


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Visualize AirSLAM relocalization results.")
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to debug/relocalization.txt",
    )
    parser.add_argument(
        "--save",
        type=str,
        default="",
        help="Optional path to save the figure instead of showing it interactively.",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="relocalization.txt",
        help="Optional plot title suffix.",
    )
    return parser


def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()

    records = parse_relocalization_file(args.file)
    visualize(records, title=args.title, save_path=args.save)


if __name__ == "__main__":
    main()


