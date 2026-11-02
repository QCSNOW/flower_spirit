"""Manually draw BoP-style textures for dancing_lady, chamomile, oncidium."""
import numpy as np
from PIL import Image

TARGET = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

def save_texture(name, pixels):
    """Save a pixel dict to PNG."""
    img = Image.new('RGBA', (TARGET, TARGET), (0, 0, 0, 0))
    arr = np.array(img)
    for (y, x), (r, g, b) in pixels.items():
        arr[y, x] = [r, g, b, 255]
    img = Image.fromarray(arr, 'RGBA')
    path = f"{DST}\\{name}.png"
    img.save(path, 'PNG')
    n = len(pixels)
    colors = set(pixels.values())
    print(f"  {name}: {n} pixels, {len(colors)} colors")
    return n

# ========== DANCING LADY (Oncidium/Dancing Lady Orchid) ==========
# 3 golden-yellow flowers on an arching stem, each with large ruffled lip
# Colors: bright yellow (250, 200, 30), deep yellow (230, 170, 10), 
#         brown spots (139, 69, 19), stem green (100, 155, 12), dark green (73, 125, 7)

dancing = {}
# Flower 1 (left, upper)
Y1, Y2, Y3 = (250, 200, 30), (230, 170, 10), (139, 69, 19)
G1, G2 = (100, 155, 12), (73, 125, 7)

# Flower 1 at (7-13, 3-9)
f1_pixels = {
    (3, 10): Y2, (3, 11): Y1,
    (4, 8): Y2, (4, 9): Y1, (4, 10): Y1, (4, 11): Y1, (4, 12): Y2,
    (5, 7): Y2, (5, 8): Y1, (5, 9): Y1, (5, 10): Y3, (5, 11): Y1, (5, 12): Y1, (5, 13): Y2,
    (6, 7): Y1, (6, 8): Y1, (6, 9): Y1, (6, 10): Y1, (6, 11): Y1, (6, 12): Y1, (6, 13): Y2,
    (7, 8): Y2, (7, 9): Y1, (7, 10): Y3, (7, 11): Y1, (7, 12): Y2,
    (8, 9): Y2, (8, 10): Y2, (8, 11): Y2,
}
# Flower 2 (center, middle)
f2_pixels = {
    (10, 14): Y2, (10, 15): Y1, (10, 16): Y2,
    (11, 13): Y2, (11, 14): Y1, (11, 15): Y1, (11, 16): Y1, (11, 17): Y2,
    (12, 12): Y2, (12, 13): Y1, (12, 14): Y1, (12, 15): Y3, (12, 16): Y1, (12, 17): Y1, (12, 18): Y2,
    (13, 12): Y1, (13, 13): Y1, (13, 14): Y1, (13, 15): Y1, (13, 16): Y1, (13, 17): Y1, (13, 18): Y2,
    (14, 13): Y2, (14, 14): Y1, (14, 15): Y3, (14, 16): Y1, (14, 17): Y2,
    (15, 14): Y2, (15, 15): Y2, (15, 16): Y2,
}
# Flower 3 (right, lower)
f3_pixels = {
    (17, 18): Y2, (17, 19): Y1, (17, 20): Y2,
    (18, 17): Y2, (18, 18): Y1, (18, 19): Y1, (18, 20): Y1, (18, 21): Y2,
    (19, 16): Y2, (19, 17): Y1, (19, 18): Y1, (19, 19): Y3, (19, 20): Y1, (19, 21): Y1, (19, 22): Y2,
    (20, 16): Y1, (20, 17): Y1, (20, 18): Y1, (20, 19): Y1, (20, 20): Y1, (20, 21): Y1, (20, 22): Y2,
    (21, 17): Y2, (21, 18): Y1, (21, 19): Y3, (21, 20): Y1, (21, 21): Y2,
    (22, 18): Y2, (22, 19): Y2, (22, 20): Y2,
}
dancing.update(f1_pixels)
dancing.update(f2_pixels)
dancing.update(f3_pixels)

# Arching stem connecting flowers
for y, x_range in [(9, range(11, 14)), (16, range(14, 18)), (23, range(16, 19))]:
    for x in x_range:
        dancing[(y, x)] = G1
# Main stem going down
for y in range(23, 32):
    dancing[(y, 15)] = G1
    dancing[(y, 16)] = G1
for y in range(24, 31):
    dancing[(y, 14)] = G2
    dancing[(y, 17)] = G2
# Leaves
for y, x in [(26, 12), (26, 13), (27, 11), (27, 12), (29, 19), (29, 20), (30, 18), (30, 19)]:
    dancing[(y, x)] = G1

print("Drawing dancing_lady...")
save_texture('dancing_lady', dancing)

# ========== CHAMOMILE (Daisy) ==========
# Classic daisy: white petals around yellow center, on a green stem
# Colors: white (250, 250, 250), light gray (220, 220, 220), 
#         yellow center (250, 210, 50), dark yellow (230, 180, 30),
#         stem green (100, 155, 12), dark green (73, 125, 7)

W1, W2 = (250, 250, 250), (220, 220, 220)
YC1, YC2 = (250, 210, 50), (230, 180, 30)

chamomile = {}
# Petals - 12 white petals radiating from center
# Center is at (16, 10)
cx, cy = 16, 10
# Draw 12 petals at different angles
import math
petal_colors = [W1, W2, W1, W2, W1, W1, W2, W1, W2, W1, W1, W2]
for i in range(12):
    angle = i * 30 * math.pi / 180
    for r in range(4, 8):
        px = cx + int(round(r * math.cos(angle)))
        py = cy + int(round(r * math.sin(angle)))
        if 0 <= px < 32 and 0 <= py < 32:
            c = W1 if r < 6 else W2
            chamomile[(py, px)] = c
    # Add petal tip
    px = cx + int(round(7 * math.cos(angle)))
    py = cy + int(round(7 * math.sin(angle)))
    if 0 <= px < 32 and 0 <= py < 32:
        chamomile[(py, px)] = W2

# Yellow center disc
for dy in range(-2, 3):
    for dx in range(-2, 3):
        if dx*dx + dy*dy <= 4:
            px = cx + dx
            py = cy + dy
            if 0 <= px < 32 and 0 <= py < 32:
                if dx*dx + dy*dy <= 1:
                    chamomile[(py, px)] = YC1
                else:
                    chamomile[(py, px)] = YC2

# Fill in some gaps in petals
for y in range(5, 16):
    for x in range(10, 23):
        if (y, x) not in chamomile:
            # Check if near center
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            if 3 <= dist <= 7:
                # Check if between two existing pixels
                has_neighbor = False
                for ddy, ddx in [(-1,0),(1,0),(0,-1),(0,1)]:
                    if (y+ddy, x+ddx) in chamomile:
                        has_neighbor = True
                if has_neighbor:
                    chamomile[(y, x)] = W2

# Green stem
for y in range(17, 32):
    chamomile[(y, 15)] = G1
    chamomile[(y, 16)] = G1
for y in range(18, 31):
    chamomile[(y, 14)] = G2
    chamomile[(y, 17)] = G2

# Leaves
for y, x in [(22, 12), (22, 13), (23, 11), (23, 12), (27, 18), (27, 19), (28, 17), (28, 18)]:
    chamomile[(y, x)] = G1

print("\nDrawing chamomile...")
save_texture('chamomile', chamomile)

# ========== ONCIDIUM (Oncidium Orchid) ==========
# 3-4 compact golden-yellow flowers on short vertical stem
# Similar to dancing lady but more compact, with brown markings
oncidium = {}

# Flower 1 (top)
f1 = {
    (2, 14): Y2, (2, 15): Y1, (2, 16): Y2, (2, 17): Y1,
    (3, 13): Y2, (3, 14): Y1, (3, 15): Y1, (3, 16): Y3, (3, 17): Y1, (3, 18): Y2,
    (4, 13): Y1, (4, 14): Y1, (4, 15): Y1, (4, 16): Y1, (4, 17): Y1, (4, 18): Y2,
    (5, 14): Y2, (5, 15): Y3, (5, 16): Y1, (5, 17): Y2,
    (6, 15): Y2, (6, 16): Y2,
}
# Flower 2 (middle, left)
f2 = {
    (9, 10): Y2, (9, 11): Y1, (9, 12): Y2,
    (10, 9): Y2, (10, 10): Y1, (10, 11): Y1, (10, 12): Y3, (10, 13): Y2,
    (11, 9): Y1, (11, 10): Y1, (11, 11): Y1, (11, 12): Y1, (11, 13): Y2,
    (12, 10): Y2, (12, 11): Y3, (12, 12): Y2,
    (13, 11): Y2,
}
# Flower 3 (middle, right) 
f3 = {
    (10, 19): Y2, (10, 20): Y1, (10, 21): Y2,
    (11, 18): Y2, (11, 19): Y1, (11, 20): Y1, (11, 21): Y3, (11, 22): Y2,
    (12, 18): Y1, (12, 19): Y1, (12, 20): Y1, (12, 21): Y1, (12, 22): Y2,
    (13, 19): Y2, (13, 20): Y3, (13, 21): Y2,
    (14, 20): Y2,
}
# Flower 4 (bottom center)
f4 = {
    (16, 14): Y2, (16, 15): Y1, (16, 16): Y2, (16, 17): Y1,
    (17, 13): Y2, (17, 14): Y1, (17, 15): Y1, (17, 16): Y3, (17, 17): Y1, (17, 18): Y2,
    (18, 13): Y1, (18, 14): Y1, (18, 15): Y1, (18, 16): Y1, (18, 17): Y1, (18, 18): Y2,
    (19, 14): Y2, (19, 15): Y3, (19, 16): Y1, (19, 17): Y2,
    (20, 15): Y2, (20, 16): Y2,
}

oncidium.update(f1)
oncidium.update(f2)
oncidium.update(f3)
oncidium.update(f4)

# Stem connecting flowers
for y in range(6, 10):
    oncidium[(y, 15)] = G1
    oncidium[(y, 16)] = G1
for y in range(14, 17):
    oncidium[(y, 15)] = G1
    oncidium[(y, 16)] = G1
for y in range(21, 32):
    oncidium[(y, 15)] = G1
    oncidium[(y, 16)] = G1
for y in range(22, 31):
    oncidium[(y, 14)] = G2
    oncidium[(y, 17)] = G2

# Leaves
for y, x in [(25, 12), (25, 13), (26, 11), (26, 12), (28, 19), (28, 20), (29, 18), (29, 19)]:
    oncidium[(y, x)] = G1

print("\nDrawing oncidium...")
save_texture('oncidium', oncidium)
