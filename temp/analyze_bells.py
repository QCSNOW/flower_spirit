"""Analyze and fix Bells of Ireland texture - remove white border, optimize stem."""
import numpy as np
from PIL import Image

TEX_PATH = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\bells_of_ireland.png"

img = Image.open(TEX_PATH).convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]

print(f"Texture size: {w}x{h}")
print(f"Total pixels: {h*w}")
print(f"Visible pixels (alpha>0): {np.sum(arr[:,:,3]>0)}")
print(f"Transparent pixels (alpha=0): {np.sum(arr[:,:,3]==0)}")

# Show all visible pixels with their colors
print("\n=== All visible pixels ===")
for y in range(h):
    for x in range(w):
        r, g, b, a = arr[y, x]
        if a > 0:
            print(f"  ({x},{y}): R={r} G={g} B={b} A={a}")

# Check for near-white pixels (potential white border)
print("\n=== Near-white pixels (R>=200, G>=200, B>=200) ===")
for y in range(h):
    for x in range(w):
        r, g, b, a = arr[y, x]
        if a > 0 and r >= 200 and g >= 200 and b >= 200:
            print(f"  ({x},{y}): R={r} G={g} B={b} A={a}")

# Print grid visualization
print("\n=== Grid visualization (alpha channel) ===")
for y in range(h):
    row = ""
    for x in range(w):
        a = arr[y, x, 3]
        if a == 0:
            row += ". "
        else:
            r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
            row += f"({r:3d},{g:3d},{b:3d}) "
    print(row)
