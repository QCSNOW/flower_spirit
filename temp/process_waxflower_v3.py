"""Waxflower v3: fix pink color detection and better quantization.
Shape stays 100% unchanged - only transparency + color reduction.
"""
import numpy as np
from PIL import Image

SRC = r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\e9b02282-ea48-43e5-a171-90f1ac375154_aee3403a-dd85-46f4-a9b5-1c6778526c9b_澳洲腊梅.png"
DST_BLOCK = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
DST_ITEM = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\waxflower.png"
T = 32

img = Image.open(SRC).convert('RGBA')
arr = np.array(img)

# Step 1: White bg -> transparent
canvas = np.zeros((T, T, 4), dtype=np.uint8)
for y in range(T):
    for x in range(T):
        r, g, b, a = arr[y, x]
        if r > 250 and g > 250 and b > 250:
            continue
        canvas[y, x] = [r, g, b, 255]

# Step 2: Better color grouping
all_colors = []
for y in range(T):
    for x in range(T):
        if canvas[y, x, 3] > 0:
            c = (int(canvas[y,x,0]), int(canvas[y,x,1]), int(canvas[y,x,2]))
            if c not in all_colors:
                all_colors.append(c)

print(f"Total unique colors: {len(all_colors)}")

# Classify each color
greens = []
creams = []
pinks = []
darks = []

for c in all_colors:
    r, g, b = c
    # Green: g significantly higher than r and b
    if g > r + 10 and g > b + 5:
        greens.append(c)
    # Pink: r high, g low-medium, b medium-high
    # Pink has r > g and b > g, but r > b
    elif r > g + 10 and b > g + 5 and r >= b - 20:
        pinks.append(c)
    # Cream/white: all channels high, relatively equal
    elif r > 180 and g > 180 and b > 160:
        creams.append(c)
    # Dark / other
    else:
        darks.append(c)

print(f"Green: {len(greens)}, Cream: {len(creams)}, Pink: {len(pinks)}, Dark/other: {len(darks)}")

# Print some sample pinks
if pinks:
    print(f"Pink samples: {pinks[:5]}")
else:
    # If no pink detected, look at high-r low-g colors
    candidates = [c for c in all_colors if c[0] > c[1] + 15]
    candidates.sort(key=lambda c: c[0] - c[1], reverse=True)
    print(f"High-red candidates: {candidates[:8]}")

# Quantize each group
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

# Target distribution: green=5, cream=4, pink=2, dark=1 = 12 total
green_target = min(5, len(greens))
cream_target = min(4, len(creams))
pink_target = min(2, max(1, len(pinks)))
dark_target = max(1, 12 - green_target - cream_target - pink_target)

print(f"\nTarget colors: green={green_target}, cream={cream_target}, pink={pink_target}, dark={dark_target}")

green_map = quantize(greens, green_target)
cream_map = quantize(creams, cream_target)
pink_map = quantize(pinks, pink_target)
dark_map = quantize(darks, dark_target)

# Apply
result = canvas.copy()
for y in range(T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        c = (r, g, b)
        
        if g > r + 10 and g > b + 5:
            new_c = green_map.get(c, c)
        elif r > g + 10 and b > g + 5 and r >= b - 20:
            new_c = pink_map.get(c, c)
        elif r > 180 and g > 180 and b > 160:
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

# Verify
print("\n=== Verification ===")
print(f"Size: 32x32 (shape unchanged)")
print(f"Pixels: {n_final}")
print(f"Colors: {c_final}")

# Pink check
final_pinks = 0
for y in range(T):
    for x in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if r > g + 10 and b > g + 5 and r >= b - 20:
                final_pinks += 1
print(f"Pink pixels: {final_pinks}")

# White border check
white_edge = 0
for y in [0, 1, T-1, T-2]:
    for x in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if r > 245 and g > 245 and b > 245:
                white_edge += 1
for x in [0, 1, T-1, T-2]:
    for y in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if r > 245 and g > 245 and b > 245:
                white_edge += 1
print(f"White edge pixels: {white_edge}")

print("\nDone! Both block and item textures saved.")
