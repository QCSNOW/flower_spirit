"""Refine all 12 flower textures: fix sizing, add stem gradient, clean edges, enhance leaves.
Self-check before/after each fix.
"""
import numpy as np
from PIL import Image
import os

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

# Green palette for stem/leaf refinement
G_HL = (140, 195, 55)   # highlight
G_LT = (110, 170, 35)   # light
G_MD = (80, 140, 20)    # mid
G_DK = (55, 100, 12)    # dark
G_DP = (35, 70, 5)      # darkest
G_CALY = (45, 80, 10)   # calyx

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

def load(name):
    return np.array(Image.open(f"{DST}\\{name}").convert('RGBA'))

def save(arr, name):
    Image.fromarray(arr, 'RGBA').save(f"{DST}\\{name}", 'PNG')

def find_stem_region(arr):
    """Find the stem area: bottom portion of image with green vertical pixels."""
    # Find bottom-most continuous green region
    green_rows = []
    for y in range(T):
        green_count = 0
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
                if g > r + 10 and g > b + 10:
                    green_count += 1
        if green_count > 0:
            green_rows.append((y, green_count))
    
    if not green_rows:
        return None, None, None
    
    # Find the stem column (center x of green pixels near bottom)
    bottom_y = max(y for y, _ in green_rows)
    stem_cx = None
    for y in range(bottom_y, max(0, bottom_y - 5), -1):
        green_xs = []
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
                if g > r + 10 and g > b + 10:
                    green_xs.append(x)
        if len(green_xs) >= 2:
            stem_cx = sum(green_xs) // len(green_xs)
            break
    
    return bottom_y, stem_cx, green_rows

def add_stem_gradient(arr):
    """Add left-highlight / right-shadow gradient to stem."""
    # Find stem area
    bottom_y, stem_cx, _ = find_stem_region(arr)
    if stem_cx is None or bottom_y is None:
        return arr
    
    result = arr.copy()
    
    # Walk up from bottom, find all stem pixels
    # For each row in stem region, add highlight on left side, shadow on right
    for y in range(bottom_y, -1, -1):
        # Find green pixels in this row
        green_xs = []
        for x in range(T):
            if result[y, x, 3] > 0:
                r, g, b = int(result[y, x, 0]), int(result[y, x, 1]), int(result[y, x, 2])
                if g > r + 5 and g > b + 5 and g > 50:
                    green_xs.append(x)
        
        if not green_xs:
            continue
        
        # This might be leaves or stem - only process if it's a vertical stem-like structure
        # (narrow, 2-4 pixels wide)
        if len(green_xs) <= 4 and len(green_xs) >= 2:
            left = min(green_xs)
            right = max(green_xs)
            
            # Replace with gradient stem
            # Left pixel = highlight
            px(result, y, left, G_HL)
            # Middle pixels = mid
            for x in range(left + 1, right):
                px(result, y, x, G_MD)
            # Right pixel = shadow
            px(result, y, right, G_DK)
    
    return result

def enhance_leaves(arr):
    """Add gradient shading to leaf shapes (top light, bottom dark)."""
    result = arr.copy()
    
    # Find leaf-like green regions (wider than stem, on sides)
    bottom_y, stem_cx, _ = find_stem_region(arr)
    if stem_cx is None:
        return result
    
    # Look for green pixels that are outside the stem column (leaves)
    for y in range(T):
        green_xs = []
        for x in range(T):
            if result[y, x, 3] > 0:
                r, g, b = int(result[y, x, 0]), int(result[y, x, 1]), int(result[y, x, 2])
                if g > r + 5 and g > b + 5 and g > 50:
                    green_xs.append(x)
        
        if not green_xs:
            continue
        
        # Find left leaf (pixels left of stem - 2)
        stem_left = stem_cx - 2
        left_leaf = [x for x in green_xs if x < stem_left]
        right_leaf = [x for x in green_xs if x > stem_cx + 1]
        
        # Shade left leaf: lighter top, darker bottom
        if left_leaf:
            # Determine if this row is in upper or lower part of leaf
            # Simple: leftmost pixel = darkest edge
            leftmost = min(left_leaf)
            if len(left_leaf) >= 3:
                px(result, y, leftmost, G_DK)
                # Next one in = mid
                px(result, y, leftmost + 1, G_MD)
                # Rightmost (near stem) = light
                px(result, y, max(left_leaf), G_LT)
        
        if right_leaf:
            rightmost = max(right_leaf)
            if len(right_leaf) >= 3:
                px(result, y, rightmost, G_DK)
                px(result, y, rightmost - 1, G_MD)
                px(result, y, min(right_leaf), G_LT)
    
    return result

def clean_edges(arr):
    """Remove single-pixel artifacts and smooth jagged edges."""
    result = arr.copy()
    h, w = arr.shape[:2]
    
    # Remove isolated pixels (0 neighbors)
    for y in range(h):
        for x in range(w):
            if result[y, x, 3] == 0:
                continue
            neighbors = 0
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < h and 0 <= nx < w and result[ny, nx, 3] > 0:
                    neighbors += 1
            if neighbors == 0:
                result[y, x, 3] = 0
    
    # Fill 1-pixel gaps between same-color pixels (horizontal)
    for y in range(h):
        for x in range(1, w - 1):
            if result[y, x, 3] > 0:
                continue
            left = result[y, x - 1]
            right = result[y, x + 1]
            if left[3] > 0 and right[3] > 0 and np.array_equal(left[:3], right[:3]):
                result[y, x] = left
    
    return result

def add_calyx(arr):
    """Add a dark green calyx band at the base of the flower where it meets the stem."""
    result = arr.copy()
    bottom_y, stem_cx, _ = find_stem_region(arr)
    if stem_cx is None:
        return result
    
    # Find where flower (non-green) meets stem (green)
    for y in range(T - 1):
        # Check if this row has flower pixels (non-green) and next row has green stem
        has_flower = False
        for x in range(T):
            if result[y, x, 3] > 0:
                r, g, b = int(result[y, x, 0]), int(result[y, x, 1]), int(result[y, x, 2])
                if not (g > r + 10 and g > b + 10):
                    has_flower = True
                    break
        
        has_stem = False
        stem_xs = []
        for x in range(T):
            if result[y + 1, x, 3] > 0:
                r, g, b = int(result[y + 1, x, 0]), int(result[y + 1, x, 1]), int(result[y + 1, x, 2])
                if g > r + 10 and g > b + 10:
                    has_stem = True
                    stem_xs.append(x)
        
        if has_flower and has_stem and len(stem_xs) >= 2:
            # Add calyx band: dark green slightly wider than stem
            left = min(stem_xs) - 1
            right = max(stem_xs) + 1
            for x in range(left, right + 1):
                if x == left or x == right:
                    px(result, y + 1, x, G_DP)
                else:
                    px(result, y + 1, x, G_CALY)
            break
    
    return result

def resize_texture(arr, scale_factor):
    """Resize texture by scale factor and re-center."""
    img = Image.fromarray(arr, 'RGBA')
    h, w = arr.shape[:2]
    new_w = int(w * scale_factor)
    new_h = int(h * scale_factor)
    resized = img.resize((new_w, new_h), Image.NEAREST)
    resized_arr = np.array(resized)
    
    # Place on new 32x32 canvas, bottom-aligned
    canvas = np.zeros((T, T, 4), dtype=np.uint8)
    x_off = (T - new_w) // 2
    y_off = T - new_h
    if y_off < 0:
        y_off = 0
    
    for y in range(min(new_h, T - y_off)):
        for x in range(min(new_w, T - x_off)):
            if resized_arr[y, x, 3] > 0:
                canvas[y_off + y, x_off + x] = resized_arr[y, x]
    
    return canvas


# ===== Process each flower =====
flowers = [
    "waxflower", "aster", "dancing_lady", "chamomile",
    "oncidium", "anemone", "astilbe", "hydrangea",
    "bells_of_ireland", "hypericum", "lupine", "wintersweet"
]

# Per-flower adjustments
adjustments = {
    "waxflower": 0.75,      # too big, scale down
    "aster": 1.0,
    "dancing_lady": 1.0,
    "chamomile": 1.1,       # slightly small
    "oncidium": 1.1,        # slightly small
    "anemone": 1.0,
    "astilbe": 1.3,         # too small, scale up
    "hydrangea": 0.9,       # slightly big
    "bells_of_ireland": 1.0,
    "hypericum": 0.7,       # too big, scale down
    "lupine": 1.0,
    "wintersweet": 0.7,     # too big, scale down
}

print("Refining all 12 flowers...")
for name in flowers:
    arr = load(f"{name}.png")
    n_before = int(np.sum(arr[:,:,3] > 0))
    
    # 1. Resize if needed
    scale = adjustments.get(name, 1.0)
    if scale != 1.0:
        arr = resize_texture(arr, scale)
    
    # 2. Add stem gradient
    arr = add_stem_gradient(arr)
    
    # 3. Enhance leaves
    arr = enhance_leaves(arr)
    
    # 4. Add calyx
    arr = add_calyx(arr)
    
    # 5. Clean edges
    arr = clean_edges(arr)
    
    save(arr, f"{name}.png")
    
    n_after = int(np.sum(arr[:,:,3] > 0))
    colors = set()
    for y in range(T):
        for x in range(T):
            if arr[y, x, 3] > 0:
                colors.add(tuple(arr[y, x, :3]))
    
    print(f"  {name:20s}: {n_before:4d}px -> {n_after:4d}px, {len(colors):2d}c")

print("\nDone! All textures refined.")
