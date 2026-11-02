"""Check source image alpha channel carefully."""
import numpy as np
from PIL import Image

SRC = r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\e9b02282-ea48-43e5-a171-90f1ac375154_aee3403a-dd85-46f4-a9b5-1c6778526c9b_澳洲腊梅.png"

img = Image.open(SRC).convert('RGBA')
arr = np.array(img)

print(f"Image shape: {arr.shape}")
print(f"Alpha channel analysis:")
print(f"  Fully opaque (a=255): {np.sum(arr[:,:,3] == 255)}")
print(f"  Fully transparent (a=0): {np.sum(arr[:,:,3] == 0)}")
print(f"  Partial transparency: {np.sum((arr[:,:,3] > 0) & (arr[:,:,3] < 255))}")

# Check if alpha is all 255
if np.all(arr[:,:,3] == 255):
    print("\nAlpha channel is ALL 255 - image has no transparency!")
    print("The image is likely on a white background.")
else:
    print(f"\nAlpha has transparency. Range: [{arr[:,:,3].min()}, {arr[:,:,3].max()}]")

# Show alpha map
print("\nAlpha channel preview (X=opaque, .=transparent):")
for y in range(32):
    line = ''
    for x in range(32):
        if arr[y, x, 3] > 128:
            line += 'X'
        else:
            line += '.'
    print(f"  {y:2d}: {line}")

# Check color of transparent/background areas
print("\nColor of top-left corner (likely background):")
for y in range(3):
    for x in range(3):
        r, g, b, a = arr[y, x]
        print(f"  ({x},{y}): RGB({r},{g},{b}) A={a}")
