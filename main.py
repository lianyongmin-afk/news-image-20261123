#!/usr/bin/env python3
"""Entry point for the news-image-20261123 competition.

Writes the pre-rendered 23 November 2026 world-news infographic to
``$MAKEFUN_OUTPUT_DIR/entry.png`` (``/output/entry.png`` when the
variable is unset, matching the grader container's layout).

The image lives in this repository as ``entry.png``; this program only
checks it against the gate limits (PNG, at most 1 MiB, at most
1024 x 1024) and copies it byte for byte, so repeated runs produce
identical output. Standard library only.

To re-render the image from scratch, run ``python3 generate.py``.
"""

import os
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png_size(path: Path) -> tuple[int, int]:
    """Return (width, height) from a PNG file's IHDR chunk."""
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != PNG_MAGIC or header[12:16] != b"IHDR":
        raise ValueError("not a PNG file with an IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        return fail(f"missing {source}")

    try:
        width, height = read_png_size(source)
    except (OSError, ValueError) as exc:
        return fail(str(exc))
    if width > MAX_SIDE or height > MAX_SIDE:
        return fail(f"image is {width}x{height}, over the "
                    f"{MAX_SIDE}x{MAX_SIDE} limit")
    size = source.stat().st_size
    if size > MAX_BYTES:
        return fail(f"image is {size} bytes, over the 1 MiB limit")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(source.read_bytes())
    print(f"wrote {target} ({width}x{height}, {size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
