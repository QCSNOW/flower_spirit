"""Fix Bells of Ireland texture v2 - recenter stem, remove white border."""
import numpy as np
from PIL import Image

TEX_PATH = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\bells_of_ireland.png"

img = Image.open(TEX_PATH).convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

# First, clear the old stem pixels (y>=24, the bottom area)
for y in range(24, h):
    for x in range(w):
        if arr[y, x, 3] > 0:
            arr[y, x, 3] = 0
            arr[y, x, 0] = 0
            arr[y, x, 1] = 0
            arr[y, x, 2] = 0

# Now draw a centered stem from the flower bottom (y~24) downward
# Flower center is around x=14-16
stem_x = 14  # centered under the flower
stem_colors = [
    (165, 204, 90),  # y=24: transition from flower
    (135, 191, 26),  # y=25
    (112, 167, 11),  # y=26
    (100, 155, 12),  # y=27
    (93, 145, 11),   # y=28
    (73, 125, 7),    # y=29
    (73, 125, 7),    # y=30
    (73, 125, 7),    # y=31
]

for i, (r, g, b) in enumerate(stem_colors):
    y = 24 + i
    if y >= h:
        break
    # Make stem 2px wide for better visibility
    arr[y, stem_x, 0] = r
    arr[y, stem_x, 1] = g
    arr[y, stem_x, 2] = b
    arr[y, stem_x, 3] = 255
    
    arr[y, stem_x + 1, 0] = max(0, r - 20)
    arr[y, stem_x + 1, 1] = max(0, g - 20)
    arr[y, stem_x + 1, 2] = max(0, b - 20)
    arr[y, stem_x + 1, 3] = 255

# Save
img = Image.fromarray(arr, 'RGBA')
img.save(TEX_PATH, 'PNG')

# Verify
varr = np.array(img)
n_vis = int(np.sum(varr[:, :, 3] > 0))
n_colors = len(set(tuple(varr[y, x, :3]) for y in range(32) for x in range(32) if varr[y, x, 3] > 0))

print(f"Visible pixels: {n_vis}")
print(f"Colors: {n_colors}")

# Print grid
print("\n=== Final grid ===")
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
