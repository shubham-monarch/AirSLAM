#!/usr/bin/env python3

import argparse
import os
from typing import List, Tuple

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (needed for 3D projection)
import numpy as np


def parse_relocalization_file(file_path: str) -> List[Tuple[str, np.ndarray, np.ndarray]]:
    parsed: List[Tuple[str, np.ndarray, np.ndarray]] = []
    with open(file_path, 'r') as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 8:
                # Expecting at least label (could be multiple tokens) + 7 numeric values
                continue
            # Last 7 tokens are numeric: tx ty tz qx qy qz qw
            try:
                numeric = list(map(float, parts[-7:]))
            except ValueError:
                continue
            tx, ty, tz, qx, qy, qz, qw = numeric
            label_tokens = parts[:-7]
            label = " ".join(label_tokens)
            t = np.array([tx, ty, tz], dtype=float)
            q = np.array([qx, qy, qz, qw], dtype=float)
            parsed.append((label, t, q))
    return parsed


def plot_2d(parsed: List[Tuple[str, np.ndarray, np.ndarray]], save_path: str = None, skip_base: bool = False, axis: str = 'xy') -> None:
    # axis selects which plane to project: 'xy', 'xz', or 'yz'
    axis = axis.lower()
    idx_map = {
        'xy': (0, 1),
        'xz': (0, 2),
        'yz': (1, 2),
    }
    if axis not in idx_map:
        axis = 'xy'
    i, j = idx_map[axis]

    xs_success, ys_success = [], []
    xs_fail, ys_fail = [], []
    xs_all_success, ys_all_success = [], []  # for drawing path of successes only
    base_point = None

    for label, t, _ in parsed:
        if skip_base and label.startswith('base'):
            continue
        if label.startswith('base'):
            base_point = (t[i], t[j])
            continue
        if label.startswith('success'):
            xs_success.append(t[i])
            ys_success.append(t[j])
            xs_all_success.append(t[i])
            ys_all_success.append(t[j])
        elif label.startswith('fail'):
            xs_fail.append(t[i])
            ys_fail.append(t[j])

    fig, ax = plt.subplots(figsize=(8, 6))
    if xs_all_success:
        ax.plot(xs_all_success, ys_all_success, '-', color='#1f77b4', linewidth=1.5, label='success path')
    if xs_success:
        ax.scatter(xs_success, ys_success, c='#2ca02c', s=12, label='success')
    if xs_fail:
        ax.scatter(xs_fail, ys_fail, c='#d62728', s=12, label='fail', alpha=0.7, marker='x')
    if base_point is not None:
        ax.scatter([base_point[0]], [base_point[1]], c='#9467bd', s=50, marker='*', label='base')

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel(f'{axis[0]} [m]')
    ax.set_ylabel(f'{axis[1]} [m]')
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_title(f'Relocalization trajectory (2D {axis.upper()} projection)')

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight', dpi=200)
    else:
        plt.show()


def plot_3d(parsed: List[Tuple[str, np.ndarray, np.ndarray]], save_path: str = None, skip_base: bool = False) -> None:
    xs_success, ys_success, zs_success = [], [], []
    xs_fail, ys_fail, zs_fail = [], [], []
    xs_all_success, ys_all_success, zs_all_success = [], [], []
    base_point = None

    for label, t, _ in parsed:
        if skip_base and label.startswith('base'):
            continue
        if label.startswith('base'):
            base_point = (t[0], t[1], t[2])
            continue
        if label.startswith('success'):
            xs_success.append(t[0])
            ys_success.append(t[1])
            zs_success.append(t[2])
            xs_all_success.append(t[0])
            ys_all_success.append(t[1])
            zs_all_success.append(t[2])
        elif label.startswith('fail'):
            xs_fail.append(t[0])
            ys_fail.append(t[1])
            zs_fail.append(t[2])

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    if xs_all_success:
        ax.plot(xs_all_success, ys_all_success, zs_all_success, '-', color='#1f77b4', linewidth=1.5, label='success path')
    if xs_success:
        ax.scatter(xs_success, ys_success, zs_success, c='#2ca02c', s=10, label='success')
    if xs_fail:
        ax.scatter(xs_fail, ys_fail, zs_fail, c='#d62728', s=10, label='fail', alpha=0.7, marker='x')
    if base_point is not None:
        ax.scatter([base_point[0]], [base_point[1]], [base_point[2]], c='#9467bd', s=60, marker='*', label='base')

    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_title('Relocalization trajectory (3D)')

    # Try to set equal aspect
    try:
        xs = (xs_success + xs_fail + ([base_point[0]] if base_point else []))
        ys = (ys_success + ys_fail + ([base_point[1]] if base_point else []))
        zs = (zs_success + zs_fail + ([base_point[2]] if base_point else []))
        if len(xs) > 0:
            x_min, x_max = np.min(xs), np.max(xs)
            y_min, y_max = np.min(ys), np.max(ys)
            z_min, z_max = np.min(zs), np.max(zs)
            max_range = float(max(x_max - x_min, y_max - y_min, z_max - z_min))
            if max_range > 0:
                x_mid = 0.5 * (x_max + x_min)
                y_mid = 0.5 * (y_max + y_min)
                z_mid = 0.5 * (z_max + z_min)
                ax.set_xlim(x_mid - 0.5 * max_range, x_mid + 0.5 * max_range)
                ax.set_ylim(y_mid - 0.5 * max_range, y_mid + 0.5 * max_range)
                ax.set_zlim(z_mid - 0.5 * max_range, z_mid + 0.5 * max_range)
    except Exception:
        pass

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight', dpi=200)
    else:
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description='Visualize relocalization trajectory saved by SaveTumTrajectoryToFile (string label variant).')
    parser.add_argument('--traj', type=str, required=False,
                        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'debug', 'relocalization.txt'),
                        help='Path to relocalization.txt')
    parser.add_argument('--mode', type=str, choices=['2d', '3d'], default='2d', help='Plot mode')
    parser.add_argument('--plane', type=str, choices=['xy', 'xz', 'yz'], nargs='+', default=['xy'], help='2D projection plane(s). Can pass multiple, e.g., --plane xy xz')
    parser.add_argument('--all-planes', action='store_true', help='Plot all 2D planes (xy, xz, yz). Overrides --plane')
    parser.add_argument('--skip-base', action='store_true', help='Skip plotting the base frame')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of frames (after base). 0 means no limit')
    parser.add_argument('--save', type=str, default='', help='Save figure to this path instead of showing')

    args = parser.parse_args()

    parsed = parse_relocalization_file(args.traj)

    if args.limit and args.limit > 0:
        base_entries = [item for item in parsed if item[0].startswith('base')]
        non_base_entries = [item for item in parsed if not item[0].startswith('base')]
        parsed = base_entries + non_base_entries[:args.limit]

    if args.mode == '3d':
        plot_3d(parsed, save_path=args.save if args.save else None, skip_base=args.skip_base)
    else:
        planes = ['xy', 'xz', 'yz'] if args.all_planes else args.plane
        if args.save and (len(planes) > 1):
            base, ext = os.path.splitext(args.save)
            for pl in planes:
                out_path = f"{base}_{pl}{ext if ext else '.png'}"
                plot_2d(parsed, save_path=out_path, skip_base=args.skip_base, axis=pl)
        else:
            for idx, pl in enumerate(planes):
                # When showing interactively and multiple planes, open sequentially
                save_arg = args.save if (args.save and len(planes) == 1 and idx == 0) else None
                plot_2d(parsed, save_path=save_arg, skip_base=args.skip_base, axis=pl)


if __name__ == '__main__':
    main()
