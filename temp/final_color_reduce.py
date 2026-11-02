"""Final pass: reduce color counts to MC-appropriate levels (10-14 colors)."""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

flowers = [
    "waxflower", "aster", "dancing_lady", "chamomile",
    "oncidium", "anemone", "astilbe", "hydrangea",
    "bells_of_ireland", "hypericum", "lupine", "wintersweet"
]

def reduce_colors(arr, target=12):
    """Reduce color count using k-means-like approach, preserving green stem colors separately."""
    # Separate flower colors and green colors
    flower_pixels = []
    green_pixels = []
    
    for y in range(T):
        for x in range(T):
            if arr[y, x, 3] == 0:
                continue
            r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
            if g > r + 8 and g > b + 8 and g > 50:
                green_pixels.append((r, g, b))
            else:
                flower_pixels.append((r, g, b))
    
    # Quantize greens to 5-6 shades
    green_target = min(6, max(4, len(set(green_pixels))))
    # Quantize flower to target - green_target
    flower_target = max(5, target - green_target)
    
    def quantize_pixels(pixels, n_colors):
        if not pixels:
            return {}
        unique = list(set(pixels))
        if len(unique) <= n_colors:
            return {c: c for c in unique}
        
        # Sort by luminance, sample evenly
        def lum(c):
            return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
        unique.sort(key=lum)
        indices = np.linspace(0, len(unique)-1, n_colors, dtype=int)
        palette = [unique[i] for i in indices]
        
        # Map each unique color to nearest palette color
        mapping = {}
        for c in unique:
            dists = [sum((a-b)**2 for a,b in zip(c, p)) for p in palette]
            nearest = palette[dists.index(min(dists))]
            mapping[c] = nearest
        return mapping
    
    green_map = quantize_pixels(green_pixels, green_target)
    flower_map = quantize_pixels(flower_pixels, flower_target)
    
    # Apply mapping
    result = arr.copy()
    for y in range(T):
        for x in range(T):
            if result[y, x, 3] == 0:
                continue
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            c = (r, g, b)
            if g > r + 8 and g > b + 8 and g > 50:
                if c in green_map:
                    new_c = green_map[c]
                    result[y, x] = [new_c[0], new_c[1], new_c[2], 255]
            else:
                if c in flower_map:
                    new_c = flower_map[c]
                    result[y, x] = [new_c[0], new_c[1], new_c[2], 255]
    
    return result

def count_colors(arr):
    return len(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0))

print("Reducing colors to 10-14 range...")
for name in flowers:
    arr = np.array(Image.open(f"{DST}\\{name}.png").convert('RGBA'))
    n_before = count_colors(arr)
    
    target = 12
    arr = reduce_colors(arr, target)
    n_after = count_colors(arr)
    
    Image.fromarray(arr, 'RGBA').save(f"{DST}\\{name}.png", 'PNG')
    
    n_px = int(np.sum(arr[:,:,3] > 0))
    print(f"  {name:20s}: {n_before:2d}c -> {n_after:2d}c  ({n_px}px)")

print("\nDone!")
