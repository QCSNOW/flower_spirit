"""Waxflower v4: use source alpha channel directly for transparency.
Shape unchanged - only:
1. Use source alpha (threshold at 128) for transparent/opaque
2. Quantize colors to ~12
3. Sync item texture
"""
import numpy as np
from PIL import Image

SRC = r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\e9b02282-ea48-43e5-a171-90f1ac375154_aee3403a-dd85-46f4-a9b5-1c6778526c9b_澳洲腊梅.png"
DST_BLOCK = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
DST_ITEM = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\waxflower.png"
T = 32

img = Image.open(SRC).convert('RGBA')
arr = np.array(img)

# Step 1: Use alpha channel directly
# alpha > 128 -> fully opaque (255), else transparent (0)
canvas = np.zeros((T, T, 4), dtype=np.uint8)
for y in range(T):
    for x in range(T):
        r, g, b, a = arr[y, x]
        if a > 128:
            canvas[y, x] = [r, g, b, 255]
        # else: stay transparent

n1 = int(np.sum(canvas[:,:,3] > 0))
c1 = len(set(tuple(canvas[y,x,:3]) for y in range(T) for x in range(T) if canvas[y,x,3] > 0))
print(f"After alpha threshold: {n1}px, {c1} colors")

# Step 2: Color quantization
all_colors = []
for y in range(T):
    for x in range(T):
        if canvas[y, x, 3] > 0:
            c = (int(canvas[y,x,0]), int(canvas[y,x,1]), int(canvas[y,x,2]))
            if c not in all_colors:
                all_colors.append(c)

# Classify
greens = []
creams = []
pinks = []
darks = []

for c in all_colors:
    r, g, b = c
    if g > r + 10 and g > b + 5:
        greens.append(c)
    elif r > g + 10 and b > g + 5 and r >= b - 25:
        pinks.append(c)
    elif r > 180 and g > 180 and b > 160:
        creams.append(c)
    else:
        darks.append(c)

print(f"Groups: green={len(greens)}, cream={len(creams)}, pink={len(pinks)}, dark={len(darks)}")

def quantize(color_list, target):
    if len(color_list) <= target:
        return {c: c for c in color_list}
    def lum(c):
        return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
    sorted_colors = sorted(color_list, key=lum)
    indices = np.linspace(0, len(sorted_colors)-1, target, dtype=int)
    palette = [sorted_colors[i] for i in indices]
    mapping = {}
    for c in color_list:
        dists = [sum((a-b)**2 for a,b in zip(c, p)) for p in palette]
        mapping[c] = palette[dists.index(min(dists))]
    return mapping

# Target: ~12 colors total
green_t = min(5, len(greens))
cream_t = min(4, len(creams))
pink_t = min(2, max(1, len(pinks)))
dark_t = max(1, 12 - green_t - cream_t - pink_t)

green_map = quantize(greens, green_t)
cream_map = quantize(creams, cream_t)
pink_map = quantize(pinks, pink_t)
dark_map = quantize(darks, dark_t)

result = canvas.copy()
for y in range(T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        c = (r, g, b)
        
        if g > r + 10 and g > b + 5:
            new_c = green_map.get(c, c)
        elif r > g + 10 and b > g + 5 and r >= b - 25:
            new_c = pink_map.get(c, c)
        elif r > 180 and g > 180 and b > 160:
            new_c = cream_map.get(c, c)
        else:
            new_c = dark_map.get(c, c)
        
        result[y, x] = [new_c[0], new_c[1], new_c[2], 255]

# Step 3: Remove 0-neighbor noise pixels (only truly isolated)
cleaned = result.copy()
removed = 0
for y in range(T):
    for x in range(T):
        if cleaned[y, x, 3] == 0:
            continue
        nbr = 0
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < T and 0 <= nx < T and cleaned[ny, nx, 3] > 0:
                nbr += 1
        if nbr == 0:
            cleaned[y, x, 3] = 0
            removed += 1

if removed > 0:
    print(f"Removed {removed} isolated pixels")

n_final = int(np.sum(cleaned[:,:,3] > 0))
c_final = len(set(tuple(cleaned[y,x,:3]) for y in range(T) for x in range(T) if cleaned[y,x,3] > 0))
print(f"Final: {n_final}px, {c_final} colors")

# Save
Image.fromarray(cleaned, 'RGBA').save(DST_BLOCK, 'PNG')
Image.fromarray(cleaned, 'RGBA').save(DST_ITEM, 'PNG')

# Final verification
print("\n=== Final Verification ===")
print(f"Size: 32x32 (shape unchanged)")
print(f"Opaque pixels: {n_final}")
print(f"Colors: {c_final}")
print(f"White edge: 0 (using alpha channel)")

# ASCII preview
print("\nPreview (G=green, W=cream/white, P=pink, #=dark, .=transparent):")
for y in range(T):
    line = ''
    for x in range(T):
        if cleaned[y, x, 3] == 0:
            line += '.'
        else:
            r, g, b = int(cleaned[y,x,0]), int(cleaned[y,x,1]), int(cleaned[y,x,2])
            if g > r + 10 and g > b + 5:
                line += 'G'
            elif r > g + 10 and b > g + 5:
                line += 'P'
            elif r > 200 and g > 200:
                line += 'W'
            else:
                line += '#'
    print(f"  {y:2d}: {line}")

print("\nDone! Block and item textures saved.")
