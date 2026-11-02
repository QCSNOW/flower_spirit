"""Process waxflower: shape unchanged, only:
1. White bg -> transparent
2. Color quantization (reduce to ~12 colors)
3. Remove true noise (0-neighbor pixels)
4. Sync item texture
"""
import numpy as np
from PIL import Image

SRC = r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\e9b02282-ea48-43e5-a171-90f1ac375154_aee3403a-dd85-46f4-a9b5-1c6778526c9b_澳洲腊梅.png"
DST_BLOCK = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
DST_ITEM = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\waxflower.png"
T = 32

# Load - already 32x32
img = Image.open(SRC).convert('RGBA')
arr = np.array(img)
print(f"Source: {arr.shape[1]}x{arr.shape[0]}")

# Step 1: White background -> transparent
canvas = np.zeros((T, T, 4), dtype=np.uint8)
for y in range(T):
    for x in range(T):
        r, g, b, a = arr[y, x]
        # Pure white or near-white background -> transparent
        if r > 250 and g > 250 and b > 250:
            continue
        canvas[y, x] = [r, g, b, 255]

n1 = int(np.sum(canvas[:,:,3] > 0))
c1 = len(set(tuple(canvas[y,x,:3]) for y in range(T) for x in range(T) if canvas[y,x,3] > 0))
print(f"After white removal: {n1}px, {c1} colors")

# Step 2: Remove 0-neighbor isolated pixels (true noise only)
cleaned = canvas.copy()
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

print(f"Removed {removed} isolated pixels (0 neighbors)")

# Step 3: Color quantization - preserve shape, reduce color count
# Group colors by type
green = []
cream = []
pink = []
dark = []

for y in range(T):
    for x in range(T):
        if cleaned[y, x, 3] == 0:
            continue
        r, g, b = int(cleaned[y,x,0]), int(cleaned[y,x,1]), int(cleaned[y,x,2])
        c = (r, g, b)
        if g > r + 8 and g > b + 8:
            if c not in green:
                green.append(c)
        elif r > g + 15 and b > g + 15 and r < 180:
            if c not in pink:
                pink.append(c)
        elif r > 180 and g > 180:
            if c not in cream:
                cream.append(c)
        else:
            if c not in dark:
                dark.append(c)

print(f"Color groups: green={len(green)}, cream={len(cream)}, pink={len(pink)}, dark={len(dark)}")

def quantize_list(color_list, target):
    if len(color_list) <= target:
        return {c: c for c in color_list}
    # Sort by luminance
    def lum(c):
        return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
    color_list.sort(key=lum)
    indices = np.linspace(0, len(color_list)-1, target, dtype=int)
    palette = [color_list[i] for i in indices]
    mapping = {}
    for c in color_list:
        dists = [sum((a-b)**2 for a,b in zip(c, p)) for p in palette]
        mapping[c] = palette[dists.index(min(dists))]
    return mapping

# Target: ~12 total colors
green_target = min(5, len(green))
cream_target = min(4, len(cream))
pink_target = min(2, len(pink))
dark_target = max(1, 12 - green_target - cream_target - pink_target)

green_map = quantize_list(green, green_target)
cream_map = quantize_list(cream, cream_target)
pink_map = quantize_list(pink, pink_target)
dark_map = quantize_list(dark, dark_target)

result = cleaned.copy()
for y in range(T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        c = (r, g, b)
        if g > r + 8 and g > b + 8:
            new_c = green_map.get(c, c)
        elif r > g + 15 and b > g + 15 and r < 180:
            new_c = pink_map.get(c, c)
        elif r > 180 and g > 180:
            new_c = cream_map.get(c, c)
        else:
            new_c = dark_map.get(c, c)
        result[y, x] = [new_c[0], new_c[1], new_c[2], 255]

n_final = int(np.sum(result[:,:,3] > 0))
c_final = len(set(tuple(result[y,x,:3]) for y in range(T) for x in range(T) if result[y,x,3] > 0))
print(f"\nFinal: {n_final}px, {c_final} colors")

# Save
Image.fromarray(result, 'RGBA').save(DST_BLOCK, 'PNG')
Image.fromarray(result, 'RGBA').save(DST_ITEM, 'PNG')
print(f"Saved to block and item textures")

# Quick check
print("\n=== Verification ===")
print(f"Shape preserved: 32x32 -> 32x32 (no resize)")
print(f"Pixels: {n_final}")
print(f"Colors: {c_final}")

# Check if any white border remains
white_border = 0
for y in [0, 1, T-1, T-2]:
    for x in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if r > 240 and g > 240 and b > 240:
                white_border += 1
print(f"White border pixels: {white_border}")

print("Done!")
