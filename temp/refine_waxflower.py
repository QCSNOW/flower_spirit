"""Redraw waxflower in BoP style - 5 distinct small flowers in a cluster."""
import numpy as np
from PIL import Image

path = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
img = Image.open(path).convert('RGBA')
arr = np.array(img)

# Current colors in the texture:
# Pink shades: (253,111,169) light, (251,105,163) mid, (252,102,164) mid2, (241,97,151) mid-dark, (251,94,159) dark-mid, (246,79,147) dark, (223,20,106) darkest
# Green: (74,162,67) leaf
# (238,109,156) transition

# For BoP style, we want to define 5 small flower clusters with clear boundaries
# Strategy: keep the overall shape but add dark gaps between flower clusters to create visual separation

# Let's define 5 flower centers and ensure each has a dark center dot
flower_centers = [
    (15, 5),   # top center
    (9, 10),   # upper left
    (21, 10),  # upper right
    (12, 17),  # lower left
    (19, 17),  # lower right
]

# Add dark pink centers at each flower position
DARK_CENTER = (180, 30, 90)
for cx, cy in flower_centers:
    if 0 <= cy < 32 and 0 <= cx < 32 and arr[cy, cx, 3] > 0:
        arr[cy, cx, 0] = DARK_CENTER[0]
        arr[cy, cx, 1] = DARK_CENTER[1]
        arr[cy, cx, 2] = DARK_CENTER[2]
    # Also color immediate neighbors darker to create a center dot
    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
        ny, nx = cy+dy, cx+dx
        if 0 <= ny < 32 and 0 <= nx < 32 and arr[ny, nx, 3] > 0:
            r, g, b = arr[ny, nx, 0], arr[ny, nx, 1], arr[ny, nx, 2]
            # Only darken if currently pink (not green)
            if g < 150:  # not green
                arr[ny, nx, 0] = 200
                arr[ny, nx, 1] = 50
                arr[ny, nx, 2] = 120

img = Image.fromarray(arr, 'RGBA')
img.save(path, 'PNG')

# Verify
varr = np.array(img)
n = int(np.sum(varr[:,:,3] > 0))
colors = set()
for y in range(32):
    for x in range(32):
        if varr[y, x, 3] > 0:
            colors.add(tuple(varr[y, x, :3]))
print(f"Result: {n} pixels, {len(colors)} colors")
print("Flower centers added at:", flower_centers)
