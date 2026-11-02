"""Analyze waxflower v3 and aster v3 pixel layout."""
import numpy as np
from PIL import Image

for name in ["waxflower", "aster"]:
    path = rf"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\{name}.png"
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    h, w = arr.shape[:2]
    
    visible = arr[arr[:,:,3] > 0]
    n = len(visible)
    colors = set()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if arr[y, x, 3] > 0:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                colors.add((r, g, b))
                xs.append(x)
                ys.append(y)
    
    print(f"\n=== {name} ===")
    print(f"Pixels: {n}, Colors: {len(colors)}")
    print(f"X range: {min(xs)}-{max(xs)} (w={max(xs)-min(xs)+1})")
    print(f"Y range: {min(ys)}-{max(ys)} (h={max(ys)-min(ys)+1})")
    print(f"Centroid: ({sum(xs)/len(xs):.1f}, {sum(ys)/len(ys):.1f})")
    
    # Print color palette
    print("Colors:")
    for c in sorted(colors):
        r, g, b = c
        bright = (r+g+b)/3
        print(f"  ({r:3d},{g:3d},{b:3d}) brightness={bright:.0f}")
    
    # Print grid (compact)
    print("Grid:")
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
