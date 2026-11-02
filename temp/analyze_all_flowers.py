"""Analyze all flower textures - pixel count, colors, shape patterns."""
import numpy as np
from PIL import Image
import os

TEX_DIR = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

flowers = sorted([f for f in os.listdir(TEX_DIR) if f.endswith('.png') and not f.startswith('flower_spirit') and not f.startswith('wisteria')])

print(f"{'Flower':<30} {'Pixels':>6} {'Colors':>6} {'Width':>6} {'Height':>6} {'Top':>4} {'Bot':>4} {'Centroid_X':>10} {'Centroid_Y':>10}")
print("-" * 90)

results = []
for fname in flowers:
    path = os.path.join(TEX_DIR, fname)
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    h, w = arr.shape[:2]
    
    visible = arr[arr[:,:,3] > 0]
    n_pixels = len(visible)
    
    if n_pixels == 0:
        print(f"{fname:<30} {0:>6} {0:>6} {w:>6} {h:>6}")
        continue
    
    colors = set()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if arr[y, x, 3] > 0:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                colors.add((r, g, b))
                xs.append(x)
                ys.append(y)
    
    top_y = min(ys)
    bot_y = max(ys)
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    
    # Width of visible pixels
    left_x = min(xs)
    right_x = max(xs)
    vis_w = right_x - left_x + 1
    vis_h = bot_y - top_y + 1
    
    flower_name = fname.replace('.png', '')
    results.append({
        'name': flower_name,
        'pixels': n_pixels,
        'colors': len(colors),
        'vis_w': vis_w,
        'vis_h': vis_h,
        'top': top_y,
        'bot': bot_y,
        'cx': cx,
        'cy': cy,
    })
    
    print(f"{flower_name:<30} {n_pixels:>6} {len(colors):>6} {vis_w:>6} {vis_h:>6} {top_y:>4} {bot_y:>4} {cx:>10.1f} {cy:>10.1f}")

# Categorize by pixel density
print("\n=== Categories ===")
large = [r for r in results if r['pixels'] >= 250]
medium = [r for r in results if 150 <= r['pixels'] < 250]
small = [r for r in results if r['pixels'] < 150]

print(f"\nLarge (>250px): {len(large)} flowers")
for r in large:
    print(f"  {r['name']}: {r['pixels']}px, {r['colors']} colors, {r['vis_w']}x{r['vis_h']}")

print(f"\nMedium (150-250px): {len(medium)} flowers")
for r in medium:
    print(f"  {r['name']}: {r['pixels']}px, {r['colors']} colors, {r['vis_w']}x{r['vis_h']}")

print(f"\nSmall (<150px): {len(small)} flowers")
for r in small:
    print(f"  {r['name']}: {r['pixels']}px, {r['colors']} colors, {r['vis_w']}x{r['vis_h']}")
