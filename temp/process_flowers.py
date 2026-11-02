"""
Convert AI-generated flower photos to Minecraft 1.20.1 style 32x32 textures.
- Remove white/gray background -> transparent
- Crop to flower bounding box (keep stem!)
- Center on 32x32 canvas
- Quantize colors (8-12 per flower)
- Hard alpha (0 or 255 only)
"""

import os
import sys
import numpy as np
from PIL import Image, ImageFilter

SRC_DIR = r"D:\mcmod\mytestmod\temp\ai_source"
DST_DIR = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
TARGET_SIZE = 32
MAX_COLORS = 12

# Flowers to process (exclude the 4 acceptable ones)
FLOWERS = [
    "dahlia", "gerbera", "ping_pong_chrysanthemum", "firework_chrysanthemum",
    "violet", "astilbe", "trachymene", "ranunculus", "wintersweet", "waxflower",
    "pincushion", "king_protea", "hypericum", "anemone", "alstroemeria",
    "chamomile", "baby_breath", "viburnum", "wisteria", "forget_me_not",
    "gomphrena", "celosia", "lupine", "aster", "clematis", "bells_of_ireland",
    "gloriosa", "oncidium", "dancing_lady", "phalaenopsis", "dendrobium"
]


def remove_background(img):
    """Remove white/light gray background and make it transparent."""
    arr = np.array(img.convert('RGBA')).astype(np.int32)

    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]

    # White or near-white background detection
    # Pixels where all RGB channels are high (>= 230) are background
    brightness = (r + g + b) / 3.0
    is_white = (brightness >= 225) & (np.abs(r - g) < 25) & (np.abs(g - b) < 25)

    # Also remove very light gray (R=G=B, brightness > 215)
    is_light_gray = (brightness >= 215) & (np.abs(r - g) < 15) & (np.abs(g - b) < 15) & (np.abs(r - b) < 15)

    # Remove near-white pixels
    mask_bg = is_white | is_light_gray

    # Set alpha to 0 for background
    arr[mask_bg, 3] = 0

    # For edge pixels (transition between flower and bg), do a soft threshold
    # Pixels that are semi-transparent get snapped to fully opaque or transparent
    result = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    return result


def crop_to_content(img, padding_frac=0.05):
    """Crop image to bounding box of non-transparent content."""
    arr = np.array(img)
    alpha = arr[:,:,3]

    if alpha.max() == 0:
        return img

    rows = np.any(alpha > 0, axis=1)
    cols = np.any(alpha > 0, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # Add small padding
    h, w = alpha.shape
    ph = int((rmax - rmin) * padding_frac)
    pw = int((cmax - cmin) * padding_frac)
    rmin = max(0, rmin - ph)
    rmax = min(h - 1, rmax + ph)
    cmin = max(0, cmin - pw)
    cmax = min(w - 1, cmax + pw)

    return img.crop((cmin, rmin, cmax + 1, rmax + 1))


def resize_to_32(img):
    """Resize to 32x32, centered, preserving aspect ratio."""
    w, h = img.size
    if w == 0 or h == 0:
        return Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))

    scale = min(TARGET_SIZE / w, TARGET_SIZE / h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resized = img.resize((new_w, new_h), Image.LANCZOS)

    # Center on 32x32 canvas
    canvas = Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))
    ox = (TARGET_SIZE - new_w) // 2
    oy = (TARGET_SIZE - new_h) // 2
    canvas.paste(resized, (ox, oy))

    return canvas


def quantize_colors(img, max_colors=MAX_COLORS):
    """Quantize to limited color palette for MC style."""
    # Use PIL's quantize with transparency
    # First, convert to P mode (palette) with alpha
    rgba = img.convert('RGBA')

    # Separate alpha
    arr = np.array(rgba)
    alpha = arr[:,:,3]

    # Only quantize non-transparent pixels
    mask = alpha > 128
    if mask.sum() == 0:
        return rgba

    # Get non-transparent pixels
    pixels = arr[mask][:, :3]  # RGB only

    # Use k-means-like quantization via PIL
    # Create a temp image with only non-transparent pixels
    temp = Image.fromarray(arr[mask][:, :3].reshape(1, -1, 3), 'RGB')
    quantized_temp = temp.quantize(colors=max_colors, method=Image.MEDIANCUT)
    palette = quantized_temp.getpalette()[:max_colors * 3]
    palette = np.array(palette).reshape(-1, 3)

    # Map each pixel to nearest palette color
    quantized_pixels = np.zeros_like(pixels)
    for i in range(len(pixels)):
        if i % 10000 == 0:
            pass  # progress
        dists = np.sum((palette.astype(np.int32) - pixels[i].astype(np.int32))**2, axis=1)
        quantized_pixels[i] = palette[np.argmin(dists)]

    arr[mask, :3] = quantized_pixels
    # Hard alpha
    arr[:,:,3] = np.where(alpha > 128, 255, 0)

    return Image.fromarray(arr, 'RGBA')


def pixel_cleanup(img):
    """Remove isolated single pixels and smooth hard edges slightly."""
    arr = np.array(img)
    alpha = arr[:,:,3].copy()

    # Remove isolated transparent pixels (single pixel surrounded by opaque -> make opaque)
    # And isolated opaque pixels (single pixel surrounded by transparent -> make transparent)
    h, w = alpha.shape
    new_alpha = alpha.copy()

    for y in range(h):
        for x in range(w):
            if alpha[y, x] == 255:
                # Check if isolated (all 4 neighbors are 0)
                neighbors = []
                if y > 0: neighbors.append(alpha[y-1, x])
                if y < h-1: neighbors.append(alpha[y+1, x])
                if x > 0: neighbors.append(alpha[y, x-1])
                if x < w-1: neighbors.append(alpha[y, x+1])
                if len(neighbors) > 0 and all(n == 0 for n in neighbors):
                    new_alpha[y, x] = 0

    arr[:,:,3] = new_alpha
    return Image.fromarray(arr, 'RGBA')


def process_flower(flower_id, src_path, dst_path):
    """Full pipeline: AI image -> MC 32x32 texture."""
    print(f"Processing {flower_id}...")

    img = Image.open(src_path)
    print(f"  Source size: {img.size}")

    # Step 1: Remove background
    img = remove_background(img)

    # Step 2: Crop to content
    img = crop_to_content(img, padding_frac=0.02)
    print(f"  Cropped size: {img.size}")

    # Step 3: Resize to 32x32
    img = resize_to_32(img)

    # Step 4: Quantize colors
    img = quantize_colors(img, MAX_COLORS)

    # Step 5: Clean up isolated pixels
    img = pixel_cleanup(img)

    # Save
    img.save(dst_path, 'PNG')
    print(f"  Saved to: {dst_path}")

    # Verify
    verify = Image.open(dst_path)
    arr = np.array(verify)
    n_visible = np.sum(arr[:,:,3] > 0)
    n_colors = len(set(tuple(arr[y, x, :3]) for y in range(32) for x in range(32) if arr[y, x, 3] > 0))
    print(f"  Visible pixels: {n_visible}, Colors: {n_colors}")


def main():
    os.makedirs(DST_DIR, exist_ok=True)

    processed = 0
    failed = []

    for flower in FLOWERS:
        src_path = os.path.join(SRC_DIR, f"{flower}.jpg")
        dst_path = os.path.join(DST_DIR, f"{flower}.png")

        if not os.path.exists(src_path):
            # Try .png
            src_path = os.path.join(SRC_DIR, f"{flower}.png")
            if not os.path.exists(src_path):
                print(f"SKIP: {flower} - no source image found")
                failed.append(flower)
                continue

        try:
            process_flower(flower, src_path, dst_path)
            processed += 1
        except Exception as e:
            print(f"ERROR processing {flower}: {e}")
            failed.append(flower)
            import traceback
            traceback.print_exc()

    print(f"\n=== Summary ===")
    print(f"Processed: {processed}")
    print(f"Failed: {len(failed)}")
    if failed:
        print(f"Failed flowers: {failed}")


if __name__ == '__main__':
    main()
