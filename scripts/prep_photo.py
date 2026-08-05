#!/usr/bin/env python3
"""
Prep a photo for ASCII conversion.

Writes: data/source-prepped.png

Usage:
  python scripts/prep_photo.py /path/to/source-photo.jpg
"""
from pathlib import Path
import sys
from io import BytesIO

from rembg import remove
from PIL import Image
import numpy as np
import cv2

OUT = Path("data/source-prepped.png")

def prep(in_path: str, out_path: Path = OUT):
    p = Path(in_path)
    if not p.exists():
        raise SystemExit(f"Input not found: {in_path}")
    data = p.read_bytes()
    # rembg returns bytes of PNG with alpha
    result_bytes = remove(data)
    img = Image.open(BytesIO(result_bytes)).convert("RGBA")

    rgba = np.array(img)  # RGBA
    bgr = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2BGR)
    alpha = rgba[:, :, 3]

    # CLAHE on grayscale to boost local contrast
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)

    # Composite onto white using alpha mask
    alpha_f = (alpha / 255.0)[:, :, None]
    white = (255 * np.ones_like(enhanced_rgb)).astype("uint8")
    comp = (enhanced_rgb * alpha_f + white * (1 - alpha_f)).astype("uint8")

    out = Image.fromarray(cv2.cvtColor(comp, cv2.COLOR_BGR2RGB))
    out.save(out_path)
    print("Wrote", out_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py /path/to/source-photo.jpg")
        raise SystemExit(1)
    Path("data").mkdir(parents=True, exist_ok=True)
    prep(sys.argv[1], OUT)