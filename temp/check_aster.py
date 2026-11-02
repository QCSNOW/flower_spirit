"""Quick visual check of aster v3."""
import numpy as np
from PIL import Image

path = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\aster.png"
img = Image.open(path).convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

xs, ys = [], []
colors = set()
for y in range(h):
    for x in range(w):
        if arr[y, x, 3] > 0:
            r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
            colors.add((r, g, b))
            xs.append(x)
            ys.append(y)

print(f"Pixels: {len(xs)}, Colors: {len(colors)}")
print(f"X: {min(xs)}-{max(xs)}, Y: {min(ys)}-{max(ys)}")
print(f"Centroid: ({sum(xs)/len(xs):.1f}, {sum(ys)/len(ys):.1f})")
print("\nGrid:")
for y in range(h):
    row = ""
    for x in range(w):
        a = arr[y, x, 3]
        if a == 0:
            row += "."
        else:
            r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
            row += f"{r:02x}{g:02x}{b:02x} "
    if row.strip():
        print(f"  {y:2d}: {row}")
