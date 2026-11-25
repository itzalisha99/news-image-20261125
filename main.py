#!/usr/bin/env python3
"""news-image-20261125 entry program (Python 3.13, standard library only).

The entry image is the file entry.png shipped beside this program: 50 stories
from Wednesday 25 November 2026, drawn from verified reporting. The program
copies it to the output directory as entry.png, byte for byte, so two runs
write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

SOURCE = HERE / "entry.png"
TARGET = OUT_DIR / "entry.png"

MAX_BYTES = 1_048_576  # the bounty gate: at most 1 MiB
MAX_SIDE = 1024  # the bounty gate: at most 1024 by 1024 pixels
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def validate(path):
    """Check the bundled image against the bounty gate before we ship it.

    A blind copy would hand the grader a broken or oversized file and the
    entry would score 0 without ever reaching the judge. Refuse instead.
    Returns the file's sha256 so the caller can confirm the copy matches.
    """
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"image too large: {len(data)} bytes > {MAX_BYTES}")
    if not data.startswith(PNG_MAGIC):
        raise ValueError("not a PNG file")
    # PNG width/height live in the IHDR chunk: 8 magic + 4 length + 4 "IHDR".
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"image too big: {width}x{height} > {MAX_SIDE}x{MAX_SIDE}")
    if width == 0 or height == 0:
        raise ValueError("image has a zero side")
    return hashlib.sha256(data).hexdigest()


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"bundled image missing: {SOURCE}")
    digest = validate(SOURCE)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    # Confirm the copy landed whole: same byte count and same hash.
    if TARGET.stat().st_size != SOURCE.stat().st_size:
        raise IOError(f"incomplete copy: {TARGET} != {SOURCE}")
    if hashlib.sha256(TARGET.read_bytes()).hexdigest() != digest:
        raise IOError("copy hash mismatch")


if __name__ == "__main__":
    main()
