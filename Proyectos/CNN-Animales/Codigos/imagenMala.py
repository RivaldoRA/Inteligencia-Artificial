import os
import re
from PIL import Image
from pathlib import Path

SRC_DIR = r"C:\Users\rival\Downloads\Dataset\Dataset"
DST_DIR = r"C:\Users\rival\Downloads\Dataset\Dataset_85x85"

IMG_SIZE = (85, 85)
VALID_EXT = re.compile(r"\.(jpg|jpeg|png|bmp|tiff)$", re.IGNORECASE)

for root, _, files in os.walk(SRC_DIR):
    for filename in files:
        if not VALID_EXT.search(filename):
            continue

        src_path = os.path.join(root, filename)

        # Keep folder structure
        rel_path = os.path.relpath(root, SRC_DIR)
        dst_folder = os.path.join(DST_DIR, rel_path)
        os.makedirs(dst_folder, exist_ok=True)

        dst_path = os.path.join(dst_folder, filename)

        try:
            with Image.open(src_path) as img:
                img = img.convert("RGB")
                img = img.resize(IMG_SIZE, Image.BILINEAR)
                img.save(dst_path, format="JPEG", quality=90, optimize=True)

        except Exception as e:
            print("Skipped:", src_path, e)

print("✅ Dataset normalization complete")
