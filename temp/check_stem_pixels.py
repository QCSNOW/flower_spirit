"""Quick check: why are some pixels marked as # (dark) in the stem?"""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
T = 32

arr = np.array(Image.open(DST).convert('RGBA'))

# Check y=25 specifically
print("Row 25 analysis:")
for x in range(10, 20):
    if arr[25, x, 3] > 0:
        r, g, b = int(arr[25,x,0]), int(arr[25,x,1]), int(arr[25,x,2])
        is_green = g > r + 10 and g > b + 5
        print(f"  x={x:2d}: RGB({r:3d},{g:3d},{b:3d})  green={is_green}  g-r={g-r}  g-b={g-b}")

# Check row 26
print("\nRow 26 analysis:")
for x in range(10, 20):
    if arr[26, x, 3] > 0:
        r, g, b = int(arr[26,x,0]), int(arr[26,x,1]), int(arr[26,x,2])
        is_green = g > r + 10 and g > b + 5
        print(f"  x={x:2d}: RGB({r:3d},{g:3d},{b:3d})  green={is_green}  g-r={g-r}  g-b={g-b}")

# The # at x=15 y=25 - what color is it?
print(f"\nPixel (15, 25): RGB({int(arr[25,15,0])}, {int(arr[25,15,1])}, {int(arr[25,15,2])})")
