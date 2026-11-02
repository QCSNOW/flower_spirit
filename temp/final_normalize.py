"""Final color normalization: all flowers to 10-13 colors."""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32
TARGET = 12

flowers = [
    "waxflower", "aster", "dancing_lady", "chamomile",
    "oncidium", "anemone", "astilbe", "hydrangea",
    "bells_of_ireland", "hypericum", "lupine", "wintersweet"
]

def quantize(arr, target):
    # Separate green and non-green
    green = set()
    flower = set()
    for y in range(T):
        for x in range(T):
            if arr[y, x, 3] == 0:
                continue
            r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
            if g > r + 8 and g > b + 8 and g > 45:
                green.add((r, g, b))
            else:
                flower.add((r, g, b))
    
    green_n = min(6, len(green), max(4, target // 2))
    flower_n = target - green_n
    if flower_n < 4:
        flower_n = 4
        green_n = target - flower_n
    
    def make_palette(color_set, n):
        if len(color_set) <= n:
            return list(color_set)
        colors = sorted(color_set, key=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2])
        indices = np.linspace(0, len(colors)-1, n, dtype=int)
        return [colors[i] for i in indices]
    
    green_pal = make_palette(green, green_n)
    flower_pal = make_palette(flower, flower_n)
    
    def nearest(c, palette):
        dists = [sum((a-b)**2 for a,b in zip(c, p)) for p in palette]
        return palette[dists.index(min(dists))]
    
    result = arr.copy()
    for y in range(T):
        for x in range(T):
            if result[y, x, 3] == 0:
                continue
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            c = (r, g, b)
            if g > r + 8 and g > b + 8 and g > 45:
                new_c = nearest(c, green_pal)
            else:
                new_c = nearest(c, flower_pal)
            result[y, x] = [new_c[0], new_c[1], new_c[2], 255]
    
    return result

print("Final color normalization...")
for name in flowers:
    arr = np.array(Image.open(f"{DST}\\{name}.png").convert('RGBA'))
    c_before = len(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0))
    
    arr = quantize(arr, TARGET)
    c_after = len(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0))
    n_px = int(np.sum(arr[:,:,3] > 0))
    
    Image.fromarray(arr, 'RGBA').save(f"{DST}\\{name}.png", 'PNG')
    print(f"  {name:20s}: {c_before:2d}c -> {c_after:2d}c  ({n_px}px)")

print("\nDone!")
