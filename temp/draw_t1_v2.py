"""Enhance manually drawn textures with more color layers."""
import numpy as np
from PIL import Image

TARGET = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

def save_and_count(name, pixels):
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

# ========== DANCING LADY - enhanced with more color layers ==========
Y_BRIGHT = (252, 220, 60)   # brightest yellow highlight
Y_LIGHT = (250, 200, 30)   # light yellow
Y_MID = (230, 170, 10)     # mid yellow
Y_DEEP = (200, 140, 5)     # deep yellow shadow
B_SPOTS = (139, 69, 19)    # brown spots
G_LIGHT = (130, 175, 40)   # light green
G_MID = (100, 155, 12)     # mid green
G_DARK = (73, 125, 7)      # dark green

dancing = {}

def draw_dancing_flower(cx, cy, pixels):
    """Draw a dancing lady flower at (cx, cy)."""
    # Upper petals (3 small petals on top)
    pixels[(cy-4, cx-1)] = Y_MID
    pixels[(cy-4, cx)] = Y_LIGHT
    pixels[(cy-4, cx+1)] = Y_MID
    pixels[(cy-4, cx+2)] = Y_LIGHT
    
    # Side petals
    pixels[(cy-3, cx-2)] = Y_MID
    pixels[(cy-3, cx-1)] = Y_LIGHT
    pixels[(cy-3, cx)] = Y_BRIGHT
    pixels[(cy-3, cx+1)] = Y_BRIGHT
    pixels[(cy-3, cx+2)] = Y_LIGHT
    pixels[(cy-3, cx+3)] = Y_MID
    
    # Mid row - widest
    pixels[(cy-2, cx-2)] = Y_LIGHT
    pixels[(cy-2, cx-1)] = Y_BRIGHT
    pixels[(cy-2, cx)] = B_SPOTS   # brown spot center
    pixels[(cy-2, cx+1)] = Y_BRIGHT
    pixels[(cy-2, cx+2)] = Y_LIGHT
    pixels[(cy-2, cx+3)] = Y_MID
    
    # Lower lip (large ruffled petal)
    pixels[(cy-1, cx-3)] = Y_MID
    pixels[(cy-1, cx-2)] = Y_LIGHT
    pixels[(cy-1, cx-1)] = Y_BRIGHT
    pixels[(cy-1, cx)] = Y_BRIGHT
    pixels[(cy-1, cx+1)] = Y_BRIGHT
    pixels[(cy-1, cx+2)] = Y_LIGHT
    pixels[(cy-1, cx+3)] = Y_MID
    
    # Bottom of lip
    pixels[(cy, cx-2)] = Y_DEEP
    pixels[(cy, cx-1)] = Y_MID
    pixels[(cy, cx)] = B_SPOTS
    pixels[(cy, cx+1)] = Y_MID
    pixels[(cy, cx+2)] = Y_DEEP
    
    # Lip extension
    pixels[(cy+1, cx-1)] = Y_DEEP
    pixels[(cy+1, cx)] = Y_MID
    pixels[(cy+1, cx+1)] = Y_DEEP

# Flower 1 at (10, 5)
draw_dancing_flower(10, 5, dancing)
# Flower 2 at (16, 9) - center, slightly lower
draw_dancing_flower(16, 9, dancing)
# Flower 3 at (19, 14) - lower right
draw_dancing_flower(19, 14, dancing)

# Arching stem
for y, x in [(7, 12), (7, 13), (8, 13), (8, 14)]:
    dancing[(y, x)] = G_MID
for y, x in [(12, 14), (12, 15), (13, 15), (13, 16)]:
    dancing[(y, x)] = G_MID
for y, x in [(17, 16), (17, 17)]:
    dancing[(y, x)] = G_MID

# Main stem
for y in range(20, 32):
    dancing[(y, 15)] = G_MID
    dancing[(y, 16)] = G_MID
for y in range(21, 31):
    dancing[(y, 14)] = G_DARK
    dancing[(y, 17)] = G_DARK
for y in range(22, 30):
    dancing[(y, 13)] = G_DARK

# Leaves
for y, x in [(25, 11), (25, 12), (26, 10), (26, 11)]:
    dancing[(y, x)] = G_LIGHT
for y, x in [(28, 19), (28, 20), (29, 18), (29, 19)]:
    dancing[(y, x)] = G_LIGHT

print("Enhanced dancing_lady...")
save_and_count('dancing_lady', dancing)


# ========== CHAMOMILE - enhanced daisy ==========
import math

W_BRIGHT = (252, 252, 252)  # brightest white
W_LIGHT = (240, 240, 240)   # light white
W_SHADOW = (210, 210, 210)  # shadow gray
YC_BRIGHT = (252, 220, 60)  # bright yellow center
YC_MID = (245, 195, 40)     # mid yellow
YC_DARK = (210, 165, 25)    # dark yellow center

chamomile = {}
cx, cy = 16, 10

# Draw 14 petals radiating from center
for i in range(14):
    angle = i * (360/14) * math.pi / 180
    # Inner petal
    for r in range(3, 5):
        px = cx + int(round(r * math.cos(angle)))
        py = cy + int(round(r * math.sin(angle)))
        if 0 <= px < 32 and 0 <= py < 32:
            chamomile[(py, px)] = W_LIGHT
    # Mid petal
    for r in range(5, 7):
        px = cx + int(round(r * math.cos(angle)))
        py = cy + int(round(r * math.sin(angle)))
        if 0 <= px < 32 and 0 <= py < 32:
            chamomile[(py, px)] = W_BRIGHT
    # Outer petal tip
    px = cx + int(round(7 * math.cos(angle)))
    py = cy + int(round(7 * math.sin(angle)))
    if 0 <= px < 32 and 0 <= py < 32:
        chamomile[(py, px)] = W_SHADOW

# Fill gaps between petals
for y in range(4, 17):
    for x in range(9, 24):
        if (y, x) not in chamomile:
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            if 3 <= dist <= 7:
                has_neighbor = False
                for ddy, ddx in [(-1,0),(1,0),(0,-1),(0,1)]:
                    if (y+ddy, x+ddx) in chamomile:
                        has_neighbor = True
                if has_neighbor:
                    chamomile[(y, x)] = W_LIGHT

# Yellow center disc
for dy in range(-2, 3):
    for dx in range(-2, 3):
        d = dx*dx + dy*dy
        if d <= 4:
            px, py = cx + dx, cy + dy
            if 0 <= px < 32 and 0 <= py < 32:
                if d <= 1:
                    chamomile[(py, px)] = YC_BRIGHT
                elif d <= 2:
                    chamomile[(py, px)] = YC_MID
                else:
                    chamomile[(py, px)] = YC_DARK

# Stem
for y in range(17, 32):
    chamomile[(y, 15)] = G_MID
    chamomile[(y, 16)] = G_MID
for y in range(18, 31):
    chamomile[(y, 14)] = G_DARK
    chamomile[(y, 17)] = G_DARK
for y in range(19, 30):
    chamomile[(y, 13)] = G_DARK

# Leaves
for y, x in [(22, 11), (22, 12), (23, 10), (23, 11)]:
    chamomile[(y, x)] = G_LIGHT
for y, x in [(27, 19), (27, 20), (28, 18), (28, 19)]:
    chamomile[(y, x)] = G_LIGHT

print("\nEnhanced chamomile...")
save_and_count('chamomile', chamomile)


# ========== ONCIDIUM - enhanced ==========
oncidium = {}

def draw_oncidium_flower(cx, cy, pixels):
    """Draw a compact oncidium flower."""
    # Top petals (2)
    pixels[(cy-3, cx)] = Y_MID
    pixels[(cy-3, cx+1)] = Y_LIGHT
    
    # Upper petals
    pixels[(cy-2, cx-1)] = Y_MID
    pixels[(cy-2, cx)] = Y_BRIGHT
    pixels[(cy-2, cx+1)] = Y_BRIGHT
    pixels[(cy-2, cx+2)] = Y_MID
    
    # Side petals
    pixels[(cy-1, cx-2)] = Y_LIGHT
    pixels[(cy-1, cx-1)] = Y_BRIGHT
    pixels[(cy-1, cx)] = B_SPOTS
    pixels[(cy-1, cx+1)] = Y_BRIGHT
    pixels[(cy-1, cx+2)] = Y_LIGHT
    pixels[(cy-1, cx+3)] = Y_MID
    
    # Lower lip (wide)
    pixels[(cy, cx-2)] = Y_MID
    pixels[(cy, cx-1)] = Y_BRIGHT
    pixels[(cy, cx)] = B_SPOTS
    pixels[(cy, cx+1)] = Y_BRIGHT
    pixels[(cy, cx+2)] = Y_MID
    
    # Bottom of lip
    pixels[(cy+1, cx-1)] = Y_DEEP
    pixels[(cy+1, cx)] = Y_MID
    pixels[(cy+1, cx+1)] = Y_DEEP

# 4 flowers on vertical stem
draw_oncidium_flower(15, 4, oncidium)   # top
draw_oncidium_flower(11, 10, oncidium)  # mid-left
draw_oncidium_flower(20, 10, oncidium)  # mid-right
draw_oncidium_flower(15, 16, oncidium)  # bottom

# Stem connecting
for y in range(7, 10):
    oncidium[(y, 15)] = G_MID
    oncidium[(y, 16)] = G_MID
for y in range(14, 16):
    oncidium[(y, 15)] = G_MID
    oncidium[(y, 16)] = G_MID
for y in range(19, 32):
    oncidium[(y, 15)] = G_MID
    oncidium[(y, 16)] = G_MID
for y in range(20, 31):
    oncidium[(y, 14)] = G_DARK
    oncidium[(y, 17)] = G_DARK

# Leaves
for y, x in [(25, 11), (25, 12), (26, 10), (26, 11)]:
    oncidium[(y, x)] = G_LIGHT
for y, x in [(28, 19), (28, 20), (29, 18), (29, 19)]:
    oncidium[(y, x)] = G_LIGHT

print("\nEnhanced oncidium...")
save_and_count('oncidium', oncidium)
