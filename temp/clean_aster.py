"""Clean up black pixels from aster texture."""
import numpy as np
from PIL import Image

path = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\aster.png"
img = Image.open(path).convert('RGBA')
arr = np.array(img)

# Remove pure black pixels (000000) - these are background artifacts
changed = 0
for y in range(32):
    for x in range(32):
        r, g, b, a = arr[y, x]
        if a > 0 and r == 0 and g == 0 and b == 0:
            arr[y, x, 3] = 0
            changed += 1

# Also clean up the brown-ish (bea5b8) pixels that look like artifacts
for y in range(32):
    for x in range(32):
        r, g, b, a = arr[y, x]
        if a > 0 and r >= 180 and g >= 150 and b >= 170 and b > g:
            # This is a pinkish-brown artifact, remove
            arr[y, x, 3] = 0
            changed += 1

img = Image.fromarray(arr, 'RGBA')
img.save(path, 'PNG')

n = int(np.sum(arr[:,:,3] > 0))
colors = set()
for y in range(32):
    for x in range(32):
        if arr[y, x, 3] > 0:
            colors.add(tuple(arr[y, x, :3]))
print(f"Removed {changed} artifact pixels")
print(f"Result: {n} pixels, {len(colors)} colors")
