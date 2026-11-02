"""Targeted fixes for remaining issues in AI-converted textures."""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

G_HL = (140, 195, 55)
G_LT = (110, 170, 35)
G_MD = (80, 140, 20)
G_DK = (55, 100, 12)
G_DP = (35, 70, 5)
G_CALY = (45, 80, 10)

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

def load(name):
    return np.array(Image.open(f"{DST}\\{name}.png").convert('RGBA'))

def save(arr, name):
    Image.fromarray(arr, 'RGBA').save(f"{DST}\\{name}.png", 'PNG')

def count_px(arr):
    return int(np.sum(arr[:,:,3] > 0))

def count_colors(arr):
    return len(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0))


# ===== FIX 1: Waxflower - remove black outline artifacts =====
# Replace black/dark gray edge pixels with appropriate dark cream color
arr = load("waxflower")
# Find black pixels that are adjacent to white/cream flower pixels
for y in range(T):
    for x in range(T):
        if arr[y, x, 3] == 0:
            continue
        r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
        # Check if it's very dark (black outline artifact)
        if r < 40 and g < 40 and b < 40:
            # Find nearest light flower pixel to determine replacement color
            neighbors_light = []
            for dy in [-1,0,1]:
                for dx in [-1,0,1]:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < T and 0 <= nx < T and arr[ny, nx, 3] > 0:
                        nr, ng, nb = int(arr[ny,nx,0]), int(arr[ny,nx,1]), int(arr[ny,nx,2])
                        if nr > 150 and ng > 150 and nb > 130:  # light flower color
                            neighbors_light.append((nr, ng, nb))
            if neighbors_light:
                # Replace with darker version of flower color (as edge)
                avg_r = int(sum(c[0] for c in neighbors_light) / len(neighbors_light))
                avg_g = int(sum(c[1] for c in neighbors_light) / len(neighbors_light))
                avg_b = int(sum(c[2] for c in neighbors_light) / len(neighbors_light))
                dark_r = max(100, int(avg_r * 0.65))
                dark_g = max(95, int(avg_g * 0.65))
                dark_b = max(80, int(avg_b * 0.65))
                px(arr, y, x, (dark_r, dark_g, dark_b))

# Also clean: any remaining very dark pixels near flowers
for y in range(T):
    for x in range(T):
        if arr[y, x, 3] == 0:
            continue
        r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
        if r < 60 and g < 60 and b < 50:
            # Check if surrounded by flower pixels
            flower_neighbors = 0
            for dy in [-1,0,1]:
                for dx in [-1,0,1]:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < T and 0 <= nx < T and arr[ny, nx, 3] > 0:
                        nr, ng, nb = int(arr[ny,nx,0]), int(arr[ny,nx,1]), int(arr[ny,nx,2])
                        if nr > 120 and ng > 120:
                            flower_neighbors += 1
            if flower_neighbors >= 2:
                px(arr, y, x, (140, 130, 110))

save(arr, "waxflower")
print(f"waxflower: {count_px(arr)}px, {count_colors(arr)}c")


# ===== FIX 2: Dancing Lady - connect flowers to stem =====
arr = load("dancing_lady")
# The flowers are on the right, stem curves from bottom left
# Need to connect the green stem to the flower cluster
# Find rightmost green pixel of the stem near flowers
stem_right_x = 0
stem_y = 0
for y in range(5, 15):
    for x in range(T):
        if arr[y, x, 3] > 0:
            r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
            if g > r + 10 and g > b + 10 and x > stem_right_x:
                stem_right_x = x
                stem_y = y

# Find leftmost flower pixel at similar height
flower_left_x = T
flower_y = 0
for y in range(2, 12):
    for x in range(T):
        if arr[y, x, 3] > 0:
            r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
            if not (g > r + 10 and g > b + 10) and x < flower_left_x:
                flower_left_x = x
                flower_y = y

# Draw connecting stem segment
if stem_right_x > 0 and flower_left_x < T:
    # Draw a curved green line from stem tip to flower base
    start_y, start_x = stem_y, stem_right_x
    end_y, end_x = flower_y, flower_left_x - 1
    # Simple line drawing
    steps = max(abs(end_y - start_y), abs(end_x - start_x))
    for i in range(steps + 1):
        t = i / max(1, steps)
        y = int(start_y + t * (end_y - start_y))
        x = int(start_x + t * (end_x - start_x))
        px(arr, y, x, G_MD)
        px(arr, y, x + 1, G_DK)
        if y > start_y:
            px(arr, y, x - 1, G_LT)

save(arr, "dancing_lady")
print(f"dancing_lady: {count_px(arr)}px, {count_colors(arr)}c")


# ===== FIX 3: Astilbe - enlarge and add more feather detail =====
arr = load("astilbe")
# Scale up the flower portion
img = Image.fromarray(arr, 'RGBA')
resized = img.resize((42, 42), Image.NEAREST)  # scale up
resized_arr = np.array(resized)

# Crop/place on 32x32, bottom aligned
new_canvas = np.zeros((T, T, 4), dtype=np.uint8)
# Place from bottom
for y in range(min(42, T)):
    for x in range(min(42, T)):
        src_y = 42 - T + y  # bottom part
        src_x = (42 - T) // 2 + x  # center horizontally
        if 0 <= src_y < 42 and 0 <= src_x < 42:
            if resized_arr[src_y, src_x, 3] > 0:
                new_canvas[y, x] = resized_arr[src_y, src_x]

# Add stem gradient at bottom
for y in range(26, 32):
    px(new_canvas, y, 15, G_HL)
    px(new_canvas, y, 16, G_MD)
    px(new_canvas, y, 17, G_MD)
    px(new_canvas, y, 18, G_DK)

# Add leaves
leaf_y1, leaf_y2 = 27, 29
for dx in range(1, 5):
    px(new_canvas, leaf_y1, 14 - dx, G_LT if dx < 3 else G_MD)
    px(new_canvas, leaf_y2, 19 + dx, G_MD if dx < 3 else G_DK)

save(new_canvas, "astilbe")
print(f"astilbe: {count_px(new_canvas)}px, {count_colors(new_canvas)}c")


# ===== FIX 4: Bells of Ireland - widen and add detail =====
arr = load("bells_of_ireland")
# Scale horizontally to make it wider
img = Image.fromarray(arr, 'RGBA')
resized = img.resize((40, 32), Image.NEAREST)
resized_arr = np.array(resized)

# Center on 32x32
new_canvas = np.zeros((T, T, 4), dtype=np.uint8)
x_off = (40 - T) // 2
for y in range(T):
    for x in range(T):
        if resized_arr[y, x + x_off, 3] > 0:
            new_canvas[y, x] = resized_arr[y, x + x_off]

# Add stem gradient
for y in range(26, 32):
    px(new_canvas, y, 14, G_HL)
    px(new_canvas, y, 15, G_MD)
    px(new_canvas, y, 16, G_MD)
    px(new_canvas, y, 17, G_DK)

# Add side leaves
for dx in range(1, 4):
    px(new_canvas, 28, 13 - dx, G_LT if dx < 2 else G_MD)
    px(new_canvas, 29, 18 + dx, G_MD if dx < 2 else G_DK)

save(new_canvas, "bells_of_ireland")
print(f"bells_of_ireland: {count_px(new_canvas)}px, {count_colors(new_canvas)}c")


# ===== FIX 5: Lupine - fix fragmented leaves =====
arr = load("lupine")

# Find stem
stem_cx = 15  # approximate
for y in range(28, 32):
    for x in range(T):
        if arr[y, x, 3] > 0:
            r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
            if g > r + 10 and g > b + 10:
                stem_cx = x
                break

# Redraw cleaner leaves at bottom
# Left leaf at y=28-30
leaf_cx = stem_cx - 1
for dy in range(-2, 3):
    w = 3 - abs(dy)
    for dx in range(1, w + 2):
        x = leaf_cx - dx
        y = 29 + dy
        if dy < 0:
            px(arr, y, x, G_LT if dx <= w//2 else G_MD)
        elif dy > 0:
            px(arr, y, x, G_DK if dx <= w//2 else G_MD)
        else:
            px(arr, y, x, G_HL)

# Right leaf
leaf_cx_r = stem_cx + 2
for dy in range(-2, 3):
    w = 3 - abs(dy)
    for dx in range(1, w + 2):
        x = leaf_cx_r + dx
        y = 29 + dy
        if dy < 0:
            px(arr, y, x, G_LT if dx <= w//2 else G_MD)
        elif dy > 0:
            px(arr, y, x, G_DK if dx <= w//2 else G_MD)
        else:
            px(arr, y, x, G_HL)

save(arr, "lupine")
print(f"lupine: {count_px(arr)}px, {count_colors(arr)}c")


# ===== FIX 6: Hydrangea - re-center (was cut off on right) =====
arr = load("hydrangea")
# Shift left by a few pixels to center the flower cluster
shifted = np.zeros((T, T, 4), dtype=np.uint8)
shift = 2  # shift left by 2
for y in range(T):
    for x in range(T):
        if x + shift < T:
            shifted[y, x] = arr[y, x + shift]

# Clean up right side artifacts
save(shifted, "hydrangea")
print(f"hydrangea: {count_px(shifted)}px, {count_colors(shifted)}c")


print("\nAll fixes applied!")
