"""Debug: check what's in the waxflower texture."""
import numpy as np
from PIL import Image

DST_BLOCK = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
T = 32

arr = np.array(Image.open(DST_BLOCK).convert('RGBA'))

print("Waxflower texture analysis:")
print(f"Total pixels: {T*T}")
print(f"Opaque pixels: {np.sum(arr[:,:,3] > 0)}")
print(f"Transparent pixels: {np.sum(arr[:,:,3] == 0)}")

# Check edges
print("\nEdge row analysis:")
for y in [0, 1, 2, 30, 31]:
    opaque = sum(1 for x in range(T) if arr[y, x, 3] > 0)
    print(f"  Row {y:2d}: {opaque:2d} opaque pixels")

print("\nEdge column analysis:")
for x in [0, 1, 2, 30, 31]:
    opaque = sum(1 for y in range(T) if arr[y, x, 3] > 0)
    print(f"  Col {x:2d}: {opaque:2d} opaque pixels")

# Color list
colors = sorted(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0),
                key=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2])
print(f"\nAll {len(colors)} colors (sorted by luminance):")
for i, c in enumerate(colors):
    r, g, b = c
    # Count pixels of this color
    count = sum(1 for y in range(T) for x in range(T) if arr[y,x,3] > 0 and tuple(arr[y,x,:3]) == c)
    print(f"  {i:2d}. RGB({r:3d},{g:3d},{b:3d}) - {count:3d}px")

# Show ASCII preview
print("\nASCII preview (X=opaque, .=transparent):")
for y in range(T):
    line = ''
    for x in range(T):
        if arr[y, x, 3] > 0:
            r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
            if g > r + 10 and g > b + 5:
                line += 'G'
            elif r > g + 10 and b > g + 5:
                line += 'P'
            elif r > 200 and g > 200:
                line += 'W'
            else:
                line += '#'
        else:
            line += '.'
    print(f"  {y:2d}: {line}")
