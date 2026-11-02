"""Convert AI reference images to 32x32 MC flower textures.
Steps: crop -> resize NEAREST to 32x32 -> white bg to transparent -> color quantization -> edge cleanup
"""
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

def find_bbox(arr):
    """Find bounding box of non-white pixels."""
    h, w = arr.shape[:2]
    # white threshold: all channels > 240
    mask = np.any(arr[:,:,:3] < 240, axis=2)
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not np.any(rows):
        return 0, 0, w-1, h-1
    top, bot = np.argmax(rows), h - 1 - np.argmax(rows[::-1])
    left, right = np.argmax(cols), w - 1 - np.argmax(cols[::-1])
    return left, top, right, bot

def quantize_colors(arr, target_colors=12):
    """Simple color quantization using k-means-like approach."""
    # Get all non-transparent pixels
    mask = arr[:,:,3] > 0
    pixels = arr[mask][:,:3].astype(np.float32)
    if len(pixels) == 0:
        return arr
    
    # Unique colors
    unique_colors = np.unique(pixels, axis=0)
    if len(unique_colors) <= target_colors:
        return arr
    
    # Simple median-cut style quantize
    # For each pixel, find nearest in reduced palette
    # Use uniform sampling to create initial palette
    indices = np.linspace(0, len(unique_colors) - 1, target_colors, dtype=int)
    palette = unique_colors[indices]
    
    # Assign each pixel to nearest palette color
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

def remove_isolated_pixels(arr):
    """Remove single isolated pixels (surrounded by transparency)."""
    result = arr.copy()
    h, w = arr.shape[:2]
    for y in range(h):
        for x in range(w):
            if arr[y, x, 3] == 0:
                continue
            # Count non-transparent neighbors
            neighbors = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and arr[ny, nx, 3] > 0:
                        neighbors += 1
            if neighbors <= 1:
                result[y, x, 3] = 0
    return result

def smooth_edges(arr):
    """Smooth jagged edges by filling 1-pixel gaps between same-color regions."""
    result = arr.copy()
    h, w = arr.shape[:2]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if arr[y, x, 3] > 0:
                continue
            # Check if left and right are same color
            left = arr[y, x - 1]
            right = arr[y, x + 1]
            if left[3] > 0 and right[3] > 0 and np.array_equal(left[:3], right[:3]):
                result[y, x] = left
            # Check if top and bottom are same color
            top = arr[y - 1, x]
            bot = arr[y + 1, x]
            if top[3] > 0 and bot[3] > 0 and np.array_equal(top[:3], bot[:3]):
                result[y, x] = top
    return result

def process_image(src_path, dst_path):
    # Load
    img = Image.open(src_path).convert('RGBA')
    arr = np.array(img)
    
    # Find bounding box of flower
    left, top, right, bot = find_bbox(arr)
    cropped = arr[top:bot+1, left:right+1]
    
    # Calculate resize to fit in 32x32 with some padding
    h, w = cropped.shape[:2]
    # Target: fit in 30x30 (leave 1px padding top/bottom)
    # But flowers should fill most of the space
    max_h = 30
    max_w = 30
    
    scale = min(max_h / h, max_w / w)
    new_h = int(round(h * scale))
    new_w = int(round(w * scale))
    
    # Resize using NEAREST (pixel-perfect)
    crop_img = Image.fromarray(cropped, 'RGBA')
    resized = crop_img.resize((new_w, new_h), Image.NEAREST)
    resized_arr = np.array(resized)
    
    # Place on 32x32 canvas, bottom-aligned (stem at bottom)
    canvas = np.zeros((T, T, 4), dtype=np.uint8)
    # Center horizontally, align to bottom
    x_off = (T - new_w) // 2
    y_off = T - new_h - 1  # 1px padding at bottom
    if y_off < 0:
        y_off = 0
    
    # Paste with white->transparent
    for y in range(new_h):
        for x in range(new_w):
            r, g, b, a = resized_arr[y, x]
            # White background -> transparent
            if r > 240 and g > 240 and b > 240:
                continue
            if y_off + y < T and x_off + x < T:
                canvas[y_off + y, x_off + x] = [r, g, b, 255]
    
    # Quantize colors
    canvas = quantize_colors(canvas, target_colors=14)
    
    # Cleanup: remove isolated pixels
    canvas = remove_isolated_pixels(canvas)
    
    # Smooth edges
    canvas = smooth_edges(canvas)
    
    # Save
    out = Image.fromarray(canvas, 'RGBA')
    out.save(dst_path, 'PNG')
    
    # Stats
    n_px = int(np.sum(canvas[:,:,3] > 0))
    colors = set()
    for y in range(T):
        for x in range(T):
            if canvas[y, x, 3] > 0:
                colors.add(tuple(canvas[y, x, :3]))
    
    return n_px, len(colors)

# Process all
print("Processing 12 flowers...")
for src_name, dst_name in flowers:
    src = os.path.join(SRC, src_name)
    dst = os.path.join(DST, dst_name)
    n, c = process_image(src, dst)
    print(f"  {dst_name:20s}: {n:4d}px, {c:2d} colors")

print("\nDone! All 12 textures generated.")
