"""Final fix for bells_of_ireland and wintersweet - boost to 90%+."""
import numpy as np
from PIL import Image

T = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

G_HL = (160, 215, 75)
G_LT = (130, 195, 50)
G_MD = (100, 165, 30)
G_DK = (70, 120, 18)
G_DP = (45, 85, 8)
G_CALY = (55, 95, 15)

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

def stem(a, cx, top, bot, curve=0):
    for y in range(top, bot + 1):
        t = (y - top) / max(1, bot - top)
        x = cx + int(t * curve)
        px(a, y, x - 1, G_HL)
        px(a, y, x, G_MD)
        px(a, y, x + 1, G_MD)
        px(a, y, x + 2, G_DK)
        if y >= bot - 3:
            px(a, y, x - 2, G_DK)
            px(a, y, x + 3, G_DP)

def leaf(a, cx, cy, side, size=4):
    for dy in range(-size, size + 1):
        w = max(1, size - abs(dy))
        for dx in range(1, w + 2):
            x = cx + dx * side
            y = cy + dy
            if dy < 0:
                px(a, y, x, G_LT if dx <= w // 2 else G_MD)
            elif dy > 0:
                px(a, y, x, G_DK if dx <= w // 2 else G_MD)
            else:
                px(a, y, x, G_HL)


# ===== BELLS OF IRELAND - more green shades, more leaves =====
a = np.zeros((T, T, 4), dtype=np.uint8)

# 7 shades of green for the bells
B1 = (175, 225, 85)    # brightest highlight
B2 = (145, 205, 55)    # light
B3 = (115, 180, 35)    # mid-light
B4 = (90, 155, 25)     # mid
B5 = (65, 120, 15)     # mid-dark
B6 = (45, 90, 8)       # dark
B7 = (30, 65, 5)       # darkest edge
W_IN = (248, 242, 220)  # inner white flower
Y_ST = (240, 205, 55)   # stamen yellow

def draw_bell(a, cx, top, bot, width):
    rows = bot - top + 1
    for i in range(rows):
        y = top + i
        t = i / max(1, rows - 1)
        # Bell shape
        if t < 0.12:
            w = max(1, int(width * 0.3))
        elif t < 0.55:
            w = width
        else:
            w = max(1, int(width * 0.5))
        
        for dx in range(-w, w + 1):
            x = cx + dx
            # 7 layer gradient: center bright -> edges dark
            abs_d = abs(dx)
            if abs_d == w:
                px(a, y, x, B7)
            elif abs_d == w - 1:
                px(a, y, x, B6)
            elif abs_d <= 1:
                px(a, y, x, B1)
            elif abs_d <= 2:
                px(a, y, x, B2)
            elif abs_d <= 3:
                px(a, y, x, B3)
            else:
                px(a, y, x, B4)
    
    # Inner flower
    mid = (top + bot) // 2
    px(a, mid, cx, W_IN)
    px(a, mid, cx + 1, Y_ST)
    px(a, mid - 1, cx, Y_ST)
    px(a, mid + 1, cx, B3)

# 6 bells stacked
draw_bell(a, 15, 1, 4, 3)
draw_bell(a, 15, 6, 10, 4)
draw_bell(a, 15, 11, 15, 5)
draw_bell(a, 15, 16, 19, 4)
draw_bell(a, 15, 20, 22, 3)
draw_bell(a, 15, 23, 25, 2)

# More bract leaves between bells (both sides)
for by, bx, s in [(5, 11, -1), (5, 19, 1),
                   (10, 10, -1), (10, 20, 1),
                   (15, 9, -1), (15, 21, 1),
                   (19, 11, -1), (19, 19, 1),
                   (22, 12, -1), (22, 18, 1)]:
    leaf(a, bx, by, s, size=3)

# Connecting stem between bells
for y in [5, 10, 15, 19, 22]:
    px(a, y, 13, G_LT)
    px(a, y, 14, G_MD)
    px(a, y, 15, G_MD)
    px(a, y, 16, G_DK)
    px(a, y, 17, G_DK)

# Calyx at base of spike
for x in range(11, 20):
    px(a, 25, x, G_CALY)

# Main stem
stem(a, 15, 26, 31, curve=0)
leaf(a, 14, 27, -1, size=4)
leaf(a, 16, 27, 1, size=4)
leaf(a, 14, 30, -1, size=3)
leaf(a, 16, 30, 1, size=3)

img = Image.fromarray(a, 'RGBA')
img.save(f"{DST}\\bells_of_ireland.png", 'PNG')
n = int(np.sum(a[:,:,3] > 0))
colors = set()
for y in range(T):
    for x in range(T):
        if a[y, x, 3] > 0:
            colors.add(tuple(a[y, x, :3]))
print(f"bells_of_ireland: {n}px, {len(colors)}c")


# ===== WINTERSWEET - more green stem + leaves, BoP herb style =====
# Make it more like a BoP flower: prominent green stem with leaves,
# yellow flowers on short side stems, not a woody branch
a = np.zeros((T, T, 4), dtype=np.uint8)

Y_DK = (195, 145, 15)
Y_MD = (225, 175, 35)
Y_LT = (245, 210, 60)
Y_PALE = (252, 235, 120)
R_C = (150, 60, 80)
RC_DK = (110, 40, 60)

def waxy_flower(a, fx, fy):
    """Cup-shaped waxy yellow flower with red center"""
    for dy, dx, c in [
        (-2, 0, Y_DK),
        (-1, -1, Y_MD), (-1, 0, Y_LT), (-1, 1, Y_MD),
        (0, -2, Y_DK), (0, -1, Y_LT), (0, 0, R_C), (0, 1, Y_LT), (0, 2, Y_DK),
        (1, -1, Y_MD), (1, 0, RC_DK), (1, 1, Y_MD),
        (2, 0, Y_DK),
    ]:
        px(a, fy + dy, fx + dx, c)

# Main green stem (vertical, prominent)
stem(a, 15, 12, 31, curve=0)

# Flowers on short side stems - 5 flowers
flower_positions = [
    (8, 3, -1),    # top left
    (22, 5, 1),    # top right
    (6, 10, -1),   # mid left
    (23, 12, 1),   # mid right
    (15, 7, 0),    # center top
]

for fx, fy, side in flower_positions:
    waxy_flower(a, fx, fy)
    # Short side stem connecting to main stem
    if side == -1:
        for x in range(fx + 2, 14):
            px(a, fy, x, G_MD)
            px(a, fy + 1, x, G_DK)
    elif side == 1:
        for x in range(17, fx - 1):
            px(a, fy, x, G_MD)
            px(a, fy + 1, x, G_DK)
    else:  # center
        for y in range(fy + 2, 12):
            px(a, y, 15, G_MD)
            px(a, y, 16, G_DK)

# Leaves along main stem - BoP style, multiple pairs
leaf_positions = [(15, -1, 4), (15, 1, 4),   # upper pair
                  (14, -1, 5), (16, 1, 5),   # mid pair (larger)
                  (14, -1, 5), (16, 1, 5),   # lower-mid pair
                  (14, -1, 4), (16, 1, 4),   # lower pair
                  (14, -1, 3), (16, 1, 3)]   # bottom pair

for ly, side, sz in leaf_positions:
    leaf(a, 14 if side == -1 else 16, ly, side, size=sz)

# Calyx at base of flower cluster
for x in range(11, 20):
    px(a, 12, x, G_CALY)

img = Image.fromarray(a, 'RGBA')
img.save(f"{DST}\\wintersweet.png", 'PNG')
n = int(np.sum(a[:,:,3] > 0))
colors = set()
for y in range(T):
    for x in range(T):
        if a[y, x, 3] > 0:
            colors.add(tuple(a[y, x, :3]))
print(f"wintersweet: {n}px, {len(colors)}c")
