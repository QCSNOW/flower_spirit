"""Fix bells_of_ireland and wintersweet to pass 90% threshold."""
import numpy as np
from PIL import Image

T = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

# Green system
G_HL = (150, 200, 60)
G_LT = (120, 175, 40)
G_MD = (90, 150, 25)
G_DK = (60, 105, 15)
G_DP = (40, 75, 8)
G_CALY = (50, 90, 12)

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

def calyx(a, cx, y, w=3):
    for dx in range(-w - 1, w + 2):
        x = cx + dx
        if abs(dx) >= w:
            px(a, y, x, G_DK)
        else:
            px(a, y, x, G_CALY)


# ===== FIX 1: BELLS OF IRELAND =====
# More bells, more color layers, more leaves
a = np.zeros((T, T, 4), dtype=np.uint8)

# Bell colors: more shades
B_HL = (165, 210, 70)    # bright highlight
B_LT = (135, 190, 50)    # light green
B_MD = (100, 160, 30)    # mid green
B_DK = (70, 120, 15)     # dark green
B_DP = (45, 85, 8)       # darkest
WHITE_INNER = (245, 240, 215)  # tiny white flower inside
YELLOW_STAMEN = (235, 200, 60)  # tiny yellow stamen

def draw_bell_v2(a, cx, top, bot, width):
    rows = bot - top + 1
    for i in range(rows):
        y = top + i
        t = i / max(1, rows - 1)
        # Bell curve: narrow top -> wide mid -> narrow bottom
        if t < 0.15:
            w = max(1, int(width * 0.35))
        elif t < 0.6:
            w = width
        else:
            w = max(1, int(width * 0.55))
        
        for dx in range(-w, w + 1):
            x = cx + dx
            if abs(dx) == w:
                px(a, y, x, B_DP)
            elif abs(dx) == w - 1:
                px(a, y, x, B_DK)
            elif abs(dx) <= 1:
                px(a, y, x, B_HL)
            elif abs(dx) <= 2:
                px(a, y, x, B_LT)
            else:
                px(a, y, x, B_MD)
    
    # Inner flower (white + yellow stamen)
    mid = (top + bot) // 2
    px(a, mid, cx, WHITE_INNER)
    px(a, mid, cx + 1, YELLOW_STAMEN)
    px(a, mid - 1, cx, YELLOW_STAMEN)

# 6 bells (more than before) with varying sizes
draw_bell_v2(a, 15, 1, 4, 3)
draw_bell_v2(a, 15, 6, 10, 4)
draw_bell_v2(a, 15, 11, 15, 5)
draw_bell_v2(a, 15, 16, 19, 4)
draw_bell_v2(a, 15, 20, 23, 3)
draw_bell_v2(a, 15, 24, 26, 2)

# Small bracts/leaves between bells
for by, bx in [(5, 11), (5, 19), (10, 10), (10, 20), (15, 10), (15, 20), (19, 11), (19, 19)]:
    leaf(a, bx, by, -1 if bx < 15 else 1, size=2)

# Stem between bells (thin connecting stem)
for y in [5, 10, 15, 19, 23]:
    px(a, y, 14, G_LT)
    px(a, y, 15, G_MD)
    px(a, y, 16, G_MD)
    px(a, y, 17, G_DK)

# Main stem below
stem(a, 15, 27, 31, curve=0)
leaf(a, 14, 28, -1, size=3)
leaf(a, 16, 30, 1, size=2)

img = Image.fromarray(a, 'RGBA')
img.save(f"{DST}\\bells_of_ireland.png", 'PNG')
n = int(np.sum(a[:,:,3] > 0))
colors = set()
for y in range(T):
    for x in range(T):
        if a[y, x, 3] > 0:
            colors.add(tuple(a[y, x, :3]))
print(f"bells_of_ireland: {n}px, {len(colors)}c")


# ===== FIX 2: WINTERSWEET =====
# Keep brown branch but add green leaves and green base stem
# Also increase flower count and add more color variation
a = np.zeros((T, T, 4), dtype=np.uint8)

BR_LT = (130, 85, 45)
BR_MD = (100, 65, 30)
BR_DK = (70, 45, 15)

Y_DK = (195, 145, 15)
Y_MD = (225, 175, 35)
Y_LT = (245, 210, 60)
Y_PALE = (252, 235, 120)
R_CENTER = (150, 60, 80)
RC_DK = (110, 40, 60)

# Thicker diagonal branch with gradient
branch = [(3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8, 10),
          (9, 11), (10, 12), (11, 13), (12, 14), (13, 15),
          (14, 16), (15, 17), (16, 18), (17, 19), (18, 20),
          (19, 21), (20, 22), (21, 23), (22, 24), (23, 25),
          (24, 26), (25, 27), (26, 28)]

for y, x in branch:
    px(a, y, x, BR_LT)       # upper highlight
    px(a, y, x + 1, BR_MD)   # mid
    px(a, y + 1, x, BR_DK)   # lower shadow

# Branch tip
px(a, 2, 4, BR_DK)
px(a, 2, 5, BR_MD)

# Side twigs
for y, x in [(7, 8), (8, 7), (13, 15), (14, 14), (19, 21), (20, 20)]:
    px(a, y, x, BR_MD)
    px(a, y + 1, x, BR_DK)

# 6 flowers along branch (more than before)
def ws_flower(a, fx, fy):
    # 5-petal cup shape with gradient
    for dy, dx, c in [
        (-2, 0, Y_DK),
        (-1, -1, Y_MD), (-1, 0, Y_LT), (-1, 1, Y_MD),
        (0, -2, Y_DK), (0, -1, Y_LT), (0, 0, R_CENTER), (0, 1, Y_LT), (0, 2, Y_DK),
        (1, -1, Y_MD), (1, 0, RC_DK), (1, 1, Y_MD),
        (2, 0, Y_DK),
    ]:
        px(a, fy + dy, fx + dx, c)

ws_flower(a, 6, 5)
ws_flower(a, 11, 9)
ws_flower(a, 16, 14)
ws_flower(a, 20, 19)
ws_flower(a, 25, 25)
ws_flower(a, 8, 3)    # extra top-left flower

# Green leaves along the branch (key fix: BoP style green leaves)
for lx, ly, side in [(7, 6, -1), (12, 10, 1), (17, 15, -1), (22, 20, 1), (26, 24, -1)]:
    leaf(a, lx, ly, side, size=3)

# Green stem at the base (bottom of branch connects to green stem)
calyx(a, 28, 28, w=2)
stem(a, 28, 29, 31, curve=0)
leaf(a, 27, 30, -1, size=2)

img = Image.fromarray(a, 'RGBA')
img.save(f"{DST}\\wintersweet.png", 'PNG')
n = int(np.sum(a[:,:,3] > 0))
colors = set()
for y in range(T):
    for x in range(T):
        if a[y, x, 3] > 0:
            colors.add(tuple(a[y, x, :3]))
print(f"wintersweet: {n}px, {len(colors)}c")
