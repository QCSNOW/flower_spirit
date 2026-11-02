"""Process the uploaded waxflower reference image into MC texture.
User says: shape cannot change, only minor pixel polish allowed.
Steps: check size -> if not 32x32, resize NEAREST -> white bg to transparent ->
color quantize -> remove edge artifacts -> clean up stem -> sync item
"""
import numpy as np
from PIL import Image

SRC = r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\e9b02282-ea48-43e5-a171-90f1ac375154_aee3403a-dd85-46f4-a9b5-1c6778526c9b_澳洲腊梅.png"
DST_BLOCK = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
DST_ITEM = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\waxflower.png"
T = 32

# Load
img = Image.open(SRC).convert('RGBA')
arr = np.array(img)
h, w = arr.shape[:2]
print(f"Source image: {w}x{h}")

# Check if it's already pixel-art style (low resolution)
# Find bounding box of non-white pixels
def find_bbox(arr, threshold=240):
    mask = np.any(arr[:,:,:3] < threshold, axis=2)
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    h, w = arr.shape[:2]
    top, bot = np.argmax(rows), h - 1 - np.argmax(rows[::-1])
    left, right = np.argmax(cols), w - 1 - np.argmax(cols[::-1])
    return left, top, right, bot

left, top, right, bot = find_bbox(arr)
print(f"Bounding box: ({left},{top}) - ({right},{bot}) = {right-left+1}x{bot-top+1}")

# Crop
cropped = arr[top:bot+1, left:right+1]
ch, cw = cropped.shape[:2]

# Resize to fit in 32x32 with bottom alignment
# Calculate scale to make it fit 31px height (leave 1px bottom margin)
target_h = 30
target_w = 30
scale = min(target_h / ch, target_w / cw)
new_h = max(1, int(round(ch * scale)))
new_w = max(1, int(round(cw * scale)))

print(f"Resizing: {cw}x{ch} -> {new_w}x{new_h} (scale={scale:.3f})")

# Resize NEAREST
crop_img = Image.fromarray(cropped, 'RGBA')
resized = crop_img.resize((new_w, new_h), Image.NEAREST)
resized_arr = np.array(resized)

# Place on 32x32 canvas, bottom-aligned, horizontally centered
canvas = np.zeros((T, T, 4), dtype=np.uint8)
x_off = (T - new_w) // 2
y_off = T - new_h - 1  # 1px padding at bottom

for y in range(new_h):
    for x in range(new_w):
        r, g, b, a = resized_arr[y, x]
        # White/near-white background -> transparent
        if r > 245 and g > 245 and b > 245:
            continue
        cy, cx = y_off + y, x_off + x
        if 0 <= cy < T and 0 <= cx < T:
            canvas[cy, cx] = [r, g, b, 255]

# Count before polish
n_before = int(np.sum(canvas[:,:,3] > 0))
c_before = len(set(tuple(canvas[y,x,:3]) for y in range(T) for x in range(T) if canvas[y,x,3] > 0))
print(f"\nBefore polish: {n_before}px, {c_before} colors")

# === Minor polish (shape unchanged, only cleanup) ===

# 1. Remove single isolated pixels (0 neighbors) - true noise
polished = canvas.copy()
for y in range(T):
    for x in range(T):
        if polished[y, x, 3] == 0:
            continue
        nbr = 0
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < T and 0 <= nx < T and polished[ny, nx, 3] > 0:
                nbr += 1
        if nbr == 0:
            polished[y, x, 3] = 0

# 2. Fill 1-pixel horizontal gaps between same-color pixels
for y in range(T):
    for x in range(1, T - 1):
        if polished[y, x, 3] > 0:
            continue
        left = polished[y, x - 1]
        right = polished[y, x + 1]
        if left[3] > 0 and right[3] > 0 and np.array_equal(left[:3], right[:3]):
            polished[y, x] = left

# 3. Fill 1-pixel vertical gaps
for x in range(T):
    for y in range(1, T - 1):
        if polished[y, x, 3] > 0:
            continue
        top_p = polished[y - 1, x]
        bot_p = polished[y + 1, x]
        if top_p[3] > 0 and bot_p[3] > 0 and np.array_equal(top_p[:3], bot_p[:3]):
            polished[y, x] = top_p

# 4. Color quantization: reduce to ~12 colors (green + flower + pink)
# Separate by color groups
green_colors = set()
white_colors = set()
pink_colors = set()
dark_colors = set()

for y in range(T):
    for x in range(T):
        if polished[y, x, 3] == 0:
            continue
        r, g, b = int(polished[y,x,0]), int(polished[y,x,1]), int(polished[y,x,2])
        if g > r + 10 and g > b + 10:
            green_colors.add((r, g, b))
        elif abs(r - g) < 20 and abs(g - b) < 20 and r > 180:
            white_colors.add((r, g, b))
        elif r > g + 20 and r > b + 20 and g < 150:
            pink_colors.add((r, g, b))
        else:
            dark_colors.add((r, g, b))

print(f"Color groups: green={len(green_colors)}, white={len(white_colors)}, pink={len(pink_colors)}, other={len(dark_colors)}")

def quantize_group(color_set, target_n):
    if len(color_set) <= target_n:
        return {c: c for c in color_set}
    colors = sorted(color_set, key=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2])
    indices = np.linspace(0, len(colors)-1, target_n, dtype=int)
    palette = [colors[i] for i in indices]
    mapping = {}
    for c in color_set:
        dists = [sum((a-b)**2 for a,b in zip(c, p)) for p in palette]
        mapping[c] = palette[dists.index(min(dists))]
    return mapping

green_map = quantize_group(green_colors, 5)
white_map = quantize_group(white_colors, 4)
pink_map = quantize_group(pink_colors, 3)
dark_map = quantize_group(dark_colors, 2)

result = polished.copy()
for y in range(T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        c = (r, g, b)
        if g > r + 10 and g > b + 10:
            new_c = green_map.get(c, c)
        elif abs(r - g) < 20 and abs(g - b) < 20 and r > 180:
            new_c = white_map.get(c, c)
        elif r > g + 20 and r > b + 20 and g < 150:
            new_c = pink_map.get(c, c)
        else:
            new_c = dark_map.get(c, c)
        result[y, x] = [new_c[0], new_c[1], new_c[2], 255]

n_after = int(np.sum(result[:,:,3] > 0))
c_after = len(set(tuple(result[y,x,:3]) for y in range(T) for x in range(T) if result[y,x,3] > 0))
print(f"After polish: {n_after}px, {c_after} colors")

# Save block texture
Image.fromarray(result, 'RGBA').save(DST_BLOCK, 'PNG')
print(f"\nSaved block texture: {DST_BLOCK}")

# Save item texture (same)
Image.fromarray(result, 'RGBA').save(DST_ITEM, 'PNG')
print(f"Saved item texture: {DST_ITEM}")

# === Quality check ===
print("\n=== Quality Check ===")

# Check stem gradient
has_grad = False
for y in range(26, 31):
    greens = []
    for x in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if g > r + 10 and g > b + 10:
                greens.append((x, g))
    if len(greens) >= 2:
        greens.sort()
        if greens[0][1] > greens[-1][1] + 10:
            has_grad = True

print(f"Stem gradient: {'YES' if has_grad else 'NO'}")

# Check flower-stem connection
flower_bot = -1
for y in range(T-1, -1, -1):
    for x in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if not (g > r + 10 and g > b + 10):
                flower_bot = y
                break
    if flower_bot >= 0:
        break

stem_top = T
for y in range(T):
    for x in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if g > r + 10 and g > b + 10:
                stem_top = y
                break
    if stem_top < T:
        break

connected = stem_top <= flower_bot + 2
print(f"Flower bottom: y={flower_bot}, Stem top: y={stem_top}, Connected: {connected}")

# Isolated pixels
isolated = 0
for y in range(T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        nbr = 0
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < T and 0 <= nx < T and result[ny, nx, 3] > 0:
                nbr += 1
        if nbr == 0:
            isolated += 1
print(f"Isolated pixels (0 neighbors): {isolated}")

print(f"\nTotal: {n_after}px, {c_after} colors")
print("Done!")
