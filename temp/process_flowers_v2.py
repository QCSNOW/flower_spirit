"""
Improved AI-to-MC texture converter v2.
Key improvements:
- Flood-fill background removal from borders (preserves white/light petals)
- Better resize with intermediate scaling
- HSV-based white detection (saturation < 15 AND brightness > 230)
- Morphological hole filling
- Stem preservation
"""

import os
import numpy as np
from PIL import Image, ImageFilter, ImageMorph
from collections import deque

SRC_DIR = r"D:\mcmod\mytestmod\temp\ai_source"
DST_DIR = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
TARGET_SIZE = 32
MAX_COLORS = 10


def is_background_pixel(r, g, b):
    """Check if pixel is background using HSV-like criteria."""
    brightness = (int(r) + int(g) + int(b)) / 3.0
    max_c = max(int(r), int(g), int(b))
    min_c = min(int(r), int(g), int(b))
    saturation = (max_c - min_c) / max_c if max_c > 0 else 0

    # True white/near-white with very low saturation
    if brightness >= 235 and saturation < 0.08:
        return True
    # Very light gray
    if brightness >= 240 and saturation < 0.05:
        return True
    return False


def flood_fill_background(arr):
    """Flood-fill from all border pixels that are background, removing only connected background."""
    h, w = arr.shape[:2]
    visited = np.zeros((h, w), dtype=bool)
    is_bg = np.zeros((h, w), dtype=bool)

    queue = deque()

    # Check all 4 borders
    for x in range(w):
        for y in [0, h-1]:
            if not visited[y, x]:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                if is_background_pixel(r, g, b):
                    queue.append((y, x))
                    visited[y, x] = True
                    is_bg[y, x] = True

    for y in range(h):
        for x in [0, w-1]:
            if not visited[y, x]:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                if is_background_pixel(r, g, b):
                    queue.append((y, x))
                    visited[y, x] = True
                    is_bg[y, x] = True

    # Flood fill
    while queue:
        y, x = queue.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                r, g, b = arr[ny, nx, 0], arr[ny, nx, 1], arr[ny, nx, 2]
                if is_background_pixel(r, g, b):
                    visited[ny, nx] = True
                    is_bg[ny, nx] = True
                    queue.append((ny, nx))
                else:
                    visited[ny, nx] = True  # Mark as visited but not bg

    # Also remove any remaining standalone white pixels (not connected to border)
    # but only if they're very bright white (likely artifacts)
    for y in range(h):
        for x in range(w):
            if not is_bg[y, x]:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                brightness = (int(r) + int(g) + int(b)) / 3.0
                max_c = max(int(r), int(g), int(b))
                min_c = min(int(r), int(g), int(b))
                saturation = (max_c - min_c) / max_c if max_c > 0 else 0
                # Only remove extreme white artifacts, not light petals
                if brightness >= 248 and saturation < 0.03:
                    is_bg[y, x] = True

    return is_bg


def fill_holes(alpha_mask):
    """Fill small holes inside the opaque region (morphological close)."""
    # Simple hole filling: if a transparent pixel has 3+ opaque neighbors, make it opaque
    h, w = alpha_mask.shape
    result = alpha_mask.copy()
    for _ in range(2):  # 2 passes
        temp = result.copy()
        for y in range(h):
            for x in range(w):
                if temp[y, x] == 0:
                    count = 0
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and temp[ny, nx] > 0:
                            count += 1
                    if count >= 3:
                        result[y, x] = 255
    return result


def crop_to_content(img, padding_frac=0.02):
    """Crop to non-transparent content bounding box."""
    arr = np.array(img)
    alpha = arr[:, :, 3]
    if alpha.max() == 0:
        return img

    rows = np.any(alpha > 0, axis=1)
    cols = np.any(alpha > 0, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    h, w = alpha.shape
    ph = max(1, int((rmax - rmin) * padding_frac))
    pw = max(1, int((cmax - cmin) * padding_frac))
    rmin = max(0, rmin - ph)
    rmax = min(h - 1, rmax + ph)
    cmin = max(0, cmin - pw)
    cmax = min(w - 1, cmax + pw)

    return img.crop((cmin, rmin, cmax + 1, rmax + 1))


def resize_to_32(img):
    """Resize to 32x32 centered, preserving aspect ratio."""
    w, h = img.size
    if w == 0 or h == 0:
        return Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))

    # Scale to fill as much of the 32x32 as possible
    scale = min(TARGET_SIZE / w, TARGET_SIZE / h) * 0.95  # slight margin
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resized = img.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))
    ox = (TARGET_SIZE - new_w) // 2
    oy = (TARGET_SIZE - new_h) // 2
    canvas.paste(resized, (ox, oy))

    return canvas


def quantize_colors(img, max_colors=MAX_COLORS):
    """Quantize to limited palette for MC style."""
    arr = np.array(img.convert('RGBA'))
    alpha = arr[:, :, 3]
    mask = alpha > 128

    if mask.sum() == 0:
        return img

    # Get visible pixels
    pixels = arr[mask][:, :3].astype(np.int32)
    if len(pixels) == 0:
        return img

    # Use PIL quantize on just the visible pixels
    temp_img = Image.fromarray(pixels.reshape(1, -1, 3).astype(np.uint8), 'RGB')
    quantized = temp_img.quantize(colors=max_colors, method=Image.MEDIANCUT)
    palette = quantized.getpalette()[:max_colors * 3]
    palette = np.array(palette).reshape(-1, 3).astype(np.int32)

    # Map each pixel to nearest palette color
    quantized_pixels = np.zeros_like(pixels)
    for i in range(len(pixels)):
        dists = np.sum((palette - pixels[i]) ** 2, axis=1)
        quantized_pixels[i] = palette[np.argmin(dists)]

    arr[mask, :3] = quantized_pixels.astype(np.uint8)
    arr[:, :, 3] = np.where(alpha > 128, 255, 0)

    return Image.fromarray(arr, 'RGBA')


def cleanup_pixels(img):
    """Remove isolated single pixels, fill single-pixel holes."""
    arr = np.array(img)
    alpha = arr[:, :, 3].copy()
    h, w = alpha.shape

    for y in range(h):
        for x in range(w):
            if alpha[y, x] == 255:
                neighbors = []
                if y > 0: neighbors.append(alpha[y-1, x])
                if y < h-1: neighbors.append(alpha[y+1, x])
                if x > 0: neighbors.append(alpha[y, x-1])
                if x < w-1: neighbors.append(alpha[y, x+1])
                if len(neighbors) > 0 and all(n == 0 for n in neighbors):
                    alpha[y, x] = 0

    arr[:, :, 3] = alpha
    return Image.fromarray(arr, 'RGBA')


def process_flower(flower_id, src_path, dst_path):
    print(f"Processing {flower_id}...")

    img = Image.open(src_path).convert('RGBA')
    arr = np.array(img).astype(np.uint8)

    # Step 1: Flood-fill background removal
    bg_mask = flood_fill_background(arr)
    arr[bg_mask, 3] = 0
    img = Image.fromarray(arr, 'RGBA')
    visible_after_bg = np.sum(~bg_mask)
    print(f"  After bg removal: {visible_after_bg} pixels visible")

    # Step 2: Fill holes in alpha
    alpha = np.array(img)[:, :, 3]
    alpha_filled = fill_holes(alpha)
    arr = np.array(img)
    arr[:, :, 3] = alpha_filled
    img = Image.fromarray(arr, 'RGBA')

    # Step 3: Crop to content
    img = crop_to_content(img, 0.02)
    print(f"  Cropped: {img.size}")

    # Step 4: Resize to 32x32
    img = resize_to_32(img)

    # Step 5: Quantize colors
    img = quantize_colors(img, MAX_COLORS)

    # Step 6: Cleanup
    img = cleanup_pixels(img)

    # Save
    img.save(dst_path, 'PNG')

    # Verify
    verify = Image.open(dst_path)
    varr = np.array(verify)
    n_visible = np.sum(varr[:, :, 3] > 0)
    n_colors = len(set(tuple(varr[y, x, :3]) for y in range(32) for x in range(32) if varr[y, x, 3] > 0))
    print(f"  Result: {n_visible} pixels, {n_colors} colors")
    return n_visible


FLOWERS = [
    "dahlia", "gerbera", "ping_pong_chrysanthemum", "firework_chrysanthemum",
    "violet", "astilbe", "trachymene", "ranunculus", "wintersweet", "waxflower",
    "pincushion", "king_protea", "hypericum", "anemone", "alstroemeria",
    "chamomile", "baby_breath", "viburnum", "wisteria", "forget_me_not",
    "gomphrena", "celosia", "lupine", "aster", "clematis", "bells_of_ireland",
    "gloriosa", "oncidium", "dancing_lady", "phalaenopsis", "dendrobium"
]


def main():
    results = {}
    for flower in FLOWERS:
        src = os.path.join(SRC_DIR, f"{flower}.jpg")
        if not os.path.exists(src):
            src = os.path.join(SRC_DIR, f"{flower}.png")
        dst = os.path.join(DST_DIR, f"{flower}.png")
        try:
            n = process_flower(flower, src, dst)
            results[flower] = n
        except Exception as e:
            print(f"ERROR: {flower}: {e}")
            import traceback
            traceback.print_exc()
            results[flower] = -1

    print("\n=== Summary ===")
    sparse = {f: n for f, n in results.items() if n < 80}
    good = {f: n for f, n in results.items() if 80 <= n < 200}
    dense = {f: n for f, n in results.items() if n >= 200}
    print(f"Sparse (<80px): {len(sparse)} - {list(sparse.keys())}")
    print(f"Good (80-200px): {len(good)} - {list(good.keys())}")
    print(f"Dense (200+px): {len(dense)} - {list(dense.keys())}")


if __name__ == '__main__':
    main()
