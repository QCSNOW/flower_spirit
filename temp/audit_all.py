"""Analyze all 12 BoP-style textures for quality issues."""
import numpy as np
from PIL import Image
import os

TEX_DIR = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
flowers = ["waxflower","aster","dancing_lady","chamomile","oncidium",
           "anemone","astilbe","hydrangea","bells_of_ireland","hypericum",
           "lupine","wintersweet"]

for fname in flowers:
    path = os.path.join(TEX_DIR, f"{fname}.png")
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    h, w = arr.shape[:2]
    
    xs, ys, colors = [], [], set()
    stem_pixels = 0  # green-ish pixels in bottom half
    flower_pixels = 0  # non-green pixels in top half
    
    for y in range(h):
        for x in range(w):
            if arr[y, x, 3] > 0:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                colors.add((r, g, b))
                xs.append(x)
                ys.append(y)
                
                # Check if it's a stem pixel (green dominant, bottom half)
                if y >= 20 and g > r and g > b:
                    stem_pixels += 1
                # Check if it's a flower pixel (top half, not green)
                if y < 20 and not (g > r and g > b):
                    flower_pixels += 1
    
    n = len(xs)
    if n == 0:
        print(f"{fname:20s}: EMPTY!")
        continue
    
    vis_w = max(xs) - min(xs) + 1
    vis_h = max(ys) - max(ys) + 1
    stem_pct = stem_pixels / n * 100
    flower_pct = flower_pixels / n * 100
    
    # Check for "column" stem (stem pixels all in same x range)
    stem_xs = [xs[i] for i in range(len(xs)) if ys[i] >= 20]
    if stem_xs:
        stem_w = max(stem_xs) - min(stem_xs) + 1
    else:
        stem_w = 0
    
    issues = []
    if n < 100:
        issues.append("TOO_FEW_PIXELS")
    if len(colors) < 7:
        issues.append("TOO_FEW_COLORS")
    if stem_pct > 40:
        issues.append("STEM_HEAVY")
    if stem_w <= 2 and stem_pixels > 20:
        issues.append("COLUMN_STEM")
    if flower_pct < 30:
        issues.append("LACKS_FLOWER")
    
    status = "MAJOR_FIX" if len(issues) >= 2 else ("MINOR_FIX" if len(issues) == 1 else "OK")
    
    print(f"{fname:20s}: {n:4d}px {len(colors):2d}c stem={stem_pct:4.0f}% flower={flower_pct:4.0f}% stem_w={stem_w:2d} -> {status} {','.join(issues)}")
