"""Manually draw BoP-style bells_of_ireland (Moluccella) - green bell calyces stacked on a stem."""
import numpy as np
from PIL import Image

TARGET = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

# Colors
G_BRIGHT = (140, 200, 60)   # bright green highlight
G_LIGHT = (120, 180, 50)   # light green
G_MID = (90, 155, 35)      # mid green
G_DARK = (65, 125, 20)     # dark green shadow
G_DEEP = (45, 95, 10)      # deepest green
W_FLOWER = (240, 235, 200)  # tiny white flower inside bell

pixels = {}

def draw_bell(cx, cy_top, cy_bot, width):
    """Draw a bell-shaped calyx at position cx, from cy_top to cy_bot."""
    rows = cy_bot - cy_top + 1
    for i in range(rows):
        y = cy_top + i
        # Bell shape: narrow at top, wide in middle, narrow at bottom
        t = i / max(1, rows - 1)
        if t < 0.3:
            w = max(1, int(width * (0.5 + t)))
        elif t < 0.7:
            w = width
        else:
            w = max(1, int(width * (1.2 - t * 0.5)))
        
        for dx in range(-w, w + 1):
            x = cx + dx
            if 0 <= x < 32 and 0 <= y < 32:
                if dx == 0 and i == rows // 2:
                    pixels[(y, x)] = W_FLOWER  # tiny white flower inside
                elif abs(dx) == w:
                    pixels[(y, x)] = G_DARK    # edge shadow
                elif abs(dx) == w - 1:
                    pixels[(y, x)] = G_DEEP    # inner shadow
                elif abs(dx) <= 1:
                    pixels[(y, x)] = G_BRIGHT # center highlight
                elif abs(dx) <= 2:
                    pixels[(y, x)] = G_LIGHT   # near center
                else:
                    pixels[(y, x)] = G_MID     # mid

# 5 green bells stacked on a stem
bell_positions = [
    (15, 3, 7, 4),   # top bell
    (15, 8, 12, 5),  # bell 2
    (15, 13, 17, 5), # bell 3
    (15, 18, 22, 5), # bell 4
    (15, 23, 27, 4), # bell 5
]

for cx, top, bot, w in bell_positions:
    draw_bell(cx, top, bot, w)

# Central stem
for y in range(28, 32):
    pixels[(y, 15)] = G_MID
    pixels[(y, 16)] = G_MID
for y in range(29, 31):
    pixels[(y, 14)] = G_DARK
    pixels[(y, 17)] = G_DARK

# Small leaves at base
for y, x in [(29, 12), (29, 13), (30, 11)]:
    pixels[(y, x)] = G_LIGHT
for y, x in [(30, 18), (30, 19), (31, 19)]:
    pixels[(y, x)] = G_LIGHT

img = Image.new('RGBA', (TARGET, TARGET), (0, 0, 0, 0))
arr = np.array(img)
for (y, x), (r, g, b) in pixels.items():
    arr[y, x] = [r, g, b, 255]
img = Image.fromarray(arr, 'RGBA')
path = f"{DST}\\bells_of_ireland.png"
img.save(path, 'PNG')

n = len(pixels)
colors = set(pixels.values())
print(f"bells_of_ireland: {n} pixels, {len(colors)} colors")
