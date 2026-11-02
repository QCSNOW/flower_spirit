"""
v3: Enhanced saturation + flood-fill bg removal + larger flower scaling.
"""

import os
import numpy as np
from PIL import Image
from collections import deque

SRC_DIR = r"D:\mcmod\mytestmod\temp\ai_source"
DST_DIR = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
TARGET_SIZE = 32
MAX_COLORS = 10
SATURATION_BOOST = 1.35  # Increase saturation by 35%
BRIGHTNESS_BOOST = 1.05  # Slight brightness increase


def rgb_to_hsv(r, g, b):
    """Convert RGB (0-255) to HSV."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    v = max_c
    delta = max_c - min_c
    s = delta / max_c if max_c > 0 else 0
    if delta == 0:
        h = 0
    elif max_c == r:
        h = ((g - b) / delta) % 6
    elif max_c == g:
        h = (b - r) / delta + 2
    else:
        h = (r - g) / delta + 4
    h = h / 6.0  # normalize to 0-1
    return h, s, v


def hsv_to_rgb(h, s, v):
    """Convert HSV (0-1) to RGB (0-255)."""
    h = h * 6.0
    i = int(h) % 6
    f = h - int(h)
    v *= 255.0
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    if i == 0:
        return int(v), int(t), int(p)
    elif i == 1:
        return int(q), int(v), int(p)
    elif i == 2:
        return int(p), int(v), int(t)
    elif i == 3:
        return int(p), int(q), int(v)
    elif i == 4:
        return int(t), int(p), int(v)
    else:
        return int(v), int(p), int(q)


def boost_saturation(img):
    """Increase saturation and vibrance of the image."""
    arr = np.array(img).astype(np.int32)
    h, w = arr.shape[:2]

    for y in range(h):
        for x in range(w):
            r, g, b, a = arr[y, x]
            if a == 0:
                continue
            hue, sat, val = rgb_to_hsv(r, g, b)
            # Boost saturation
            sat = min(1.0, sat * SATURATION_BOOST)
            # Slight brightness boost for darker colors
            if val < 0.5:
                val = min(1.0, val * BRIGHTNESS_BOOST)
            nr, ng, nb = hsv_to_rgb(hue, sat, val)
            arr[y, x, 0] = max(0, min(255, nr))
            arr[y, x, 1] = max(0, min(255, ng))
            arr[y, x, 2] = max(0, min(255, nb))

    return Image.fromarray(arr.astype(np.uint8), 'RGBA')


def is_background_pixel(r, g, b):
    """Check if pixel is white/near-white background."""
    brightness = (int(r) + int(g) + int(b)) / 3.0
    max_c = max(int(r), int(g), int(b))
    min_c = min(int(r), int(g), int(b))
    saturation = (max_c - min_c) / max_c if max_c > 0 else 0

    if brightness >= 238 and saturation < 0.08:
        return True
    if brightness >= 245 and saturation < 0.05:
        return True
    return False


def flood_fill_background(arr):
    """Flood-fill from borders to remove only connected background."""
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
                    visited[ny, nx] = True

    return is_bg


def fill_holes(alpha_mask):
    """Fill small holes inside opaque region."""
    h, w = alpha_mask.shape
    result = alpha_mask.copy()
    for _ in range(2):
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


def resize_to_32(img, fill_ratio=0.92):
    """Resize to 32x32 centered, fill more of the canvas."""
    w, h = img.size
    if w == 0 or h == 0:
        return Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))

    scale = min(TARGET_SIZE / w, TARGET_SIZE / h) * fill_ratio
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resized = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))
    ox = (TARGET_SIZE - new_w) // 2
    oy = (TARGET_SIZE - new_h) // 2
    canvas.paste(resized, (ox, oy))
    return canvas


def quantize_colors(img, max_colors=MAX_COLORS):
    """Quantize to limited palette."""
    arr = np.array(img.convert('RGBA'))
    alpha = arr[:, :, 3]
    mask = alpha > 128
    if mask.sum() == 0:
        return img

    pixels = arr[mask][:, :3].astype(np.int32)
    if len(pixels) == 0:
        return img

    temp_img = Image.fromarray(pixels.reshape(1, -1, 3).astype(np.uint8), 'RGB')
    quantized = temp_img.quantize(colors=max_colors, method=Image.MEDIANCUT)
    palette = quantized.getpalette()[:max_colors * 3]
    palette = np.array(palette).reshape(-1, 3).astype(np.int32)

    for i in range(len(pixels)):
        dists = np.sum((palette - pixels[i]) ** 2, axis=1)
        pixels[i] = palette[np.argmin(dists)]

    arr[mask, :3] = pixels.astype(np.uint8)
    arr[:, :, 3] = np.where(alpha > 128, 255, 0)
    return Image.fromarray(arr, 'RGBA')


def cleanup_pixels(img):
    """Remove isolated single pixels."""
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


def process_flower(flower_id, src_path, dst_path, fill_ratio=0.92):
    print(f"Processing {flower_id}...")

    img = Image.open(src_path).convert('RGBA')
    arr = np.array(img).astype(np.uint8)

    # Step 1: Flood-fill background removal
    bg_mask = flood_fill_background(arr)
    arr[bg_mask, 3] = 0
    img = Image.fromarray(arr, 'RGBA')
    visible = int(np.sum(~bg_mask))
    print(f"  After bg removal: {visible} pixels")

    # Step 2: Boost saturation / vibrance
    img = boost_saturation(img)

    # Step 3: Fill holes
    alpha = np.array(img)[:, :, 3]
    alpha_filled = fill_holes(alpha)
    arr = np.array(img)
    arr[:, :, 3] = alpha_filled
    img = Image.fromarray(arr, 'RGBA')

    # Step 4: Crop to content
    img = crop_to_content(img, 0.02)
    print(f"  Cropped: {img.size}")

    # Step 5: Resize to 32x32
    img = resize_to_32(img, fill_ratio)

    # Step 6: Quantize colors
    img = quantize_colors(img, MAX_COLORS)

    # Step 7: Cleanup
    img = cleanup_pixels(img)

    img.save(dst_path, 'PNG')

    # Verify
    varr = np.array(img)
    n_vis = int(np.sum(varr[:, :, 3] > 0))
    n_colors = len(set(tuple(varr[y, x, :3]) for y in range(32) for x in range(32) if varr[y, x, 3] > 0))
    print(f"  Result: {n_vis} pixels, {n_colors} colors")
    return n_vis


def main():
    flowers = [
        ("dahlia_v3", "dahlia", 0.95),
        ("violet_v3", "violet", 0.92),
        ("astilbe_v3", "astilbe", 0.92),
        ("pincushion_v3", "pincushion", 0.93),
        ("hypericum_v3", "hypericum", 0.92),
        ("lupine_v3", "lupine", 0.92),
        ("oncidium_v3", "oncidium", 0.92),
        ("dancing_lady_v3", "dancing_lady", 0.92),
        ("phalaenopsis_v3", "phalaenopsis", 0.92),
        ("dendrobium_v3", "dendrobium", 0.92),
    ]

    for src_name, dst_name, fill in flowers:
        src = os.path.join(SRC_DIR, f"{src_name}.jpg")
        if not os.path.exists(src):
            src = os.path.join(SRC_DIR, f"{src_name}.png")
        dst = os.path.join(DST_DIR, f"{dst_name}.png")
        try:
            process_flower(dst_name, src, dst, fill)
        except Exception as e:
            print(f"ERROR: {dst_name}: {e}")
            import traceback
            traceback.print_exc()

    print("\nDone!")


if __name__ == '__main__':
    main()
