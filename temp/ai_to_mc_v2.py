"""Improved AI->MC converter with better sizing and quality control."""
import numpy as np
from PIL import Image
import os

SRC = r"D:\mcmod\mytestmod\temp"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

flowers = [
    ("ref_waxflower.jpg", "waxflower.png"),
    ("ref_aster.jpg", "aster.png"),
    ("ref_dancing_lady.jpg", "dancing_lady.png"),
    ("ref_chamomile.jpg", "chamomile.png"),
    ("ref_oncidium.jpg", "oncidium.png"),
    ("ref_anemone.jpg", "anemone.png"),
    ("ref_astilbe.jpg", "astilbe.png"),
    ("ref_hydrangea.jpg", "hydrangea.png"),
    ("ref_bells_of_ireland.jpg", "bells_of_ireland.png"),
    ("ref_hypericum.jpg", "hypericum.png"),
    ("ref_lupine.jpg", "lupine.png"),
    ("ref_wintersweet.jpg", "wintersweet.png"),
]

def find_bbox(arr, threshold=240):
    mask = np.any(arr[:,:,:3] < threshold, axis=2)
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not np.any(rows):
        return 0, 0, arr.shape[1]-1, arr.shape[0]-1
    h, w = arr.shape[:2]
    top, bot = np.argmax(rows), h - 1 - np.argmax(rows[::-1])
    left, right = np.argmax(cols), w - 1 - np.argmax(cols[::-1])
    return left, top, right, bot

def quantize_median_cut(arr, n_colors=12):
    """Median cut color quantization."""
    mask = arr[:,:,3] > 0
    pixels = arr[mask][:,:3].astype(np.float32)
    if len(pixels) == 0:
        return arr
    
    unique = np.unique(pixels, axis=0)
    if len(unique) <= n_colors:
        return arr
    
    # Simple approach: use uniform sampling from sorted unique colors
    # Sort by luminance
    luminance = 0.299 * unique[:,0] + 0.587 * unique[:,1] + 0.114 * unique[:,2]
    order = np.argsort(luminance)
    sorted_unique = unique[order]
    
    indices = np.linspace(0, len(sorted_unique) - 1, n_colors, dtype=int)
    palette = sorted_unique[indices]
    
    # Assign nearest palette color
    result = arr.copy()
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i, j, 3] == 0:
                continue
            px = arr[i, j, :3].astype(np.float32)
            dists = np.sum((palette - px) ** 2, axis=1)
            nearest = palette[np.argmin(dists)]
            result[i, j, :3] = nearest.astype(np.uint8)
    
    return result

def clean_texture(arr):
    """Self-check and cleanup: remove artifacts, fix common issues."""
    result = arr.copy()
    h, w = arr.shape[:2]
    
    # 1. Remove single isolated pixels (noise)
    for y in range(h):
        for x in range(w):
            if result[y, x, 3] == 0:
                continue
            neighbors = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and result[ny, nx, 3] > 0:
                        neighbors += 1
            if neighbors == 0:
                result[y, x, 3] = 0
    
    # 2. Fill 1-pixel holes (enclosed by same color)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if result[y, x, 3] > 0:
                continue
            # Check 4-directional neighbors
            n_colors = []
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y+dy, x+dx
                if result[ny, nx, 3] > 0:
                    n_colors.append(tuple(result[ny, nx, :3]))
            if len(n_colors) >= 3 and len(set(n_colors)) == 1:
                result[y, x] = [n_colors[0][0], n_colors[0][1], n_colors[0][2], 255]
    
    # 3. Remove 2px hanging spikes (pixels with only 1 connection)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if result[y, x, 3] == 0:
                continue
            # Count 4-connected neighbors
            conn = 0
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < h and 0 <= nx < w and result[ny, nx, 3] > 0:
                    conn += 1
            if conn == 1:
                # Check if it's an end pixel that should stay (flower tip)
                # Only remove if the single neighbor also has only 1 conn (spike)
                pass  # keep as is for now
    
    return result

def process_image_v2(src_path, dst_path):
    img = Image.open(src_path).convert('RGBA')
    arr = np.array(img)
    
    # Find flower bbox
    left, top, right, bot = find_bbox(arr, threshold=245)
    cropped = arr[top:bot+1, left:right+1]
    
    h, w = cropped.shape[:2]
    
    # Target size: fill 32x32 with 1px margin on sides, 0px bottom (stem touches bottom)
    # Use different strategies based on flower type
    # Generally: height should be ~30px, width proportional
    target_h = 31  # leave 1px at top
    target_w = 30  # leave 1px each side
    
    scale_h = target_h / h
    scale_w = target_w / w
    scale = min(scale_h, scale_w)
    
    # But ensure minimum size (some flowers too thin)
    # If the result would be very narrow, scale to fill width more
    new_h = int(round(h * scale))
    new_w = int(round(w * scale))
    
    # Resize NEAREST
    crop_img = Image.fromarray(cropped, 'RGBA')
    resized = crop_img.resize((new_w, new_h), Image.NEAREST)
    resized_arr = np.array(resized)
    
    # Place on canvas
    canvas = np.zeros((T, T, 4), dtype=np.uint8)
    x_off = (T - new_w) // 2
    y_off = T - new_h  # bottom-aligned (stem at bottom)
    
    # White to alpha
    for y in range(new_h):
        for x in range(new_w):
            r, g, b, a = resized_arr[y, x]
            if r > 245 and g > 245 and b > 245:
                continue
            cy, cx = y_off + y, x_off + x
            if 0 <= cy < T and 0 <= cx < T:
                canvas[cy, cx] = [r, g, b, 255]
    
    # Quantize
    canvas = quantize_median_cut(canvas, n_colors=12)
    
    # Cleanup
    canvas = clean_texture(canvas)
    
    # Save
    out = Image.fromarray(canvas, 'RGBA')
    out.save(dst_path, 'PNG')
    
    n_px = int(np.sum(canvas[:,:,3] > 0))
    colors = set()
    for y in range(T):
        for x in range(T):
            if canvas[y, x, 3] > 0:
                colors.add(tuple(canvas[y, x, :3]))
    
    return n_px, len(colors)

# Process all
print("Processing 12 flowers (v2 - better sizing)...")
total = 0
for src_name, dst_name in flowers:
    src = os.path.join(SRC, src_name)
    dst = os.path.join(DST, dst_name)
    n, c = process_image_v2(src, dst)
    total += n
    print(f"  {dst_name:20s}: {n:4d}px, {c:2d}c")

print(f"\nTotal pixels across all: {total}")
print("Done!")
