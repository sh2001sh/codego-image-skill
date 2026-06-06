#!/usr/bin/env python3
"""Shortcut entrypoint for Shu26 image generation."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an image through Shu26 with a single prompt."
    )
    parser.add_argument("prompt", nargs="+", help="Image prompt text.")
    parser.add_argument(
        "--output",
        default="generated-image.png",
        help="Output image path. Defaults to generated-image.png.",
    )
    parser.add_argument(
        "--size",
        default="1024x1024",
        help="Image size: 1024x1024, 1536x1024, 1024x1536, or auto.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of image variants to request.",
    )
    parser.add_argument(
        "--image",
        action="append",
        default=[],
        help="Optional input image path or HTTPS URL. Repeat for composition.",
    )
    parser.add_argument("--mask", help="Optional mask for localized edits.")
    parser.add_argument(
        "--raw-prompt",
        action="store_true",
        help="Send the prompt exactly as written.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    script_path = Path(__file__).resolve().parent / "generate_image.py"
    command = [
        sys.executable,
        str(script_path),
        "--prompt",
        " ".join(args.prompt),
        "--output",
        args.output,
        "--size",
        args.size,
        "--count",
        str(args.count),
    ]
    for image in args.image:
        command.extend(["--image", image])
    if args.mask:
        command.extend(["--mask", args.mask])
    if args.raw_prompt:
        command.append("--raw-prompt")

    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
