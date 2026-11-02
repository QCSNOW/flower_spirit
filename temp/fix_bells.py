"""Fix Bells of Ireland texture - remove white border, fix stem, replace white pixels."""
import numpy as np
from PIL import Image

TEX_PATH = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\bells_of_ireland.png"

img = Image.open(TEX_PATH).convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

# Color palette for replacement
GREEN_LIGHT = (187, 223, 113)   # light green
GREEN_MID = (135, 191, 26)      # mid green
GREEN_DARK = (93, 145, 11)      # dark green
GREEN_STEM = (100, 155, 12)     # stem green
GREEN_STEM_DARK = (73, 125, 7)  # dark stem

changed = 0

for y in range(h):
    for x in range(w):
        r, g, b, a = arr[y, x]
        if a == 0:
            continue
        
        # Detect near-white pixels (the white border and white highlights)
        brightness = (int(r) + int(g) + int(b)) / 3.0
        max_c = max(int(r), int(g), int(b))
        min_c = min(int(r), int(g), int(b))
        saturation = (max_c - min_c) / max_c if max_c > 0 else 0
        
        if brightness >= 200 and saturation < 0.15:
            # This is a white/near-white pixel
            
            # Top border area (y <= 3): make transparent (these are border artifacts)
            if y <= 3:
                arr[y, x, 3] = 0
                changed += 1
                continue
            
            # Stem area (y >= 24, x >= 19): replace with stem green
            if y >= 24 and x >= 19:
                # Create a stem with gradient
                if y <= 26:
                    arr[y, x, 0] = GREEN_STEM[0]
                    arr[y, x, 1] = GREEN_STEM[1]
                    arr[y, x, 2] = GREEN_STEM[2]
                else:
                    arr[y, x, 0] = GREEN_STEM_DARK[0]
                    arr[y, x, 1] = GREEN_STEM_DARK[1]
                    arr[y, x, 2] = GREEN_STEM_DARK[2]
                changed += 1
                continue
            
            # Flower body white highlights: replace with light green
            arr[y, x, 0] = GREEN_LIGHT[0]
            arr[y, x, 1] = GREEN_LIGHT[1]
            arr[y, x, 2] = GREEN_LIGHT[2]
            changed += 1

# Also clean up isolated single pixels
alpha = arr[:, :, 3].copy()
for y in range(h):
    for x in range(w):
        if alpha[y, x] == 255:
            neighbors = []
            if y > 0: neighbors.append(alpha[y-1, x])
            if y < h-1: neighbors.append(alpha[y+1, x])
            if x > 0: neighbors.append(alpha[y, x-1])
            if x < w-1: neighbors.append(alpha[y, x+1])
            if len(neighbors) > 0 and all(n == 0 for n in neighbors):
                arr[y, x, 3] = 0

# Save
img = Image.fromarray(arr, 'RGBA')
img.save(TEX_PATH, 'PNG')

# Verify
varr = np.array(img)
n_vis = int(np.sum(varr[:, :, 3] > 0))
n_white = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = varr[y, x]
        if a > 0:
            brightness = (int(r) + int(g) + int(b)) / 3.0
            max_c = max(int(r), int(g), int(b))
            min_c = min(int(r), int(g), int(b))
            sat = (max_c - min_c) / max_c if max_c > 0 else 0
            if brightness >= 200 and sat < 0.15:
                n_white += 1

print(f"Changed {changed} pixels")
print(f"Visible pixels: {n_vis}")
print(f"Remaining near-white pixels: {n_white}")

# Print grid
print("\n=== Fixed grid ===")
for y in range(h):
    row = ""
    for x in range(w):
        a = varr[y, x, 3]
        if a == 0:
            row += ". "
        else:
            r, g, b = varr[y, x, 0], varr[y, x, 1], varr[y, x, 2]
            row += f"({r:3d},{g:3d},{b:3d}) "
    print(row)
