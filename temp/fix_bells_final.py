"""Fix bells_of_ireland color count - increase to ~12 by adding more green shades."""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

# 12 distinct green shades for bells of ireland
# Bell flower greens (7 shades)
B_HL1 = (175, 225, 85)
B_HL2 = (155, 210, 65)
B_LT = (130, 190, 40)
B_MD = (105, 165, 20)
B_DK = (75, 125, 12)
B_DP = (50, 90, 5)
B_EDGE = (35, 65, 3)

# Stem greens (5 shades)
S_HL = (160, 215, 70)
S_LT = (125, 185, 40)
S_MD = (90, 150, 20)
S_DK = (55, 105, 10)
S_DP = (35, 70, 3)

# Inner flower
WHITE = (250, 245, 220)
YELLOW = (245, 210, 60)

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

a = np.zeros((T, T, 4), dtype=np.uint8)

# 5 bells stacked
def draw_bell(a, cx, top, bot, max_w):
    rows = bot - top + 1
    for i in range(rows):
        y = top + i
        t = i / max(1, rows - 1)
        if t < 0.2:
            w = max(1, int(max_w * 0.35))
        elif t < 0.55:
            w = max_w
        else:
            w = max(1, int(max_w * 0.65))
        
        for dx in range(-w, w + 1):
            x = cx + dx
            abs_d = abs(dx)
            # 7-layer gradient
            if abs_d == w:
                px(a, y, x, B_EDGE)
            elif abs_d == w - 1:
                px(a, y, x, B_DP)
            elif abs_d <= 1:
                px(a, y, x, B_HL1 if abs_d == 0 else B_HL2)
            elif abs_d <= 2:
                px(a, y, x, B_LT)
            else:
                px(a, y, x, B_MD)
    
    # Inner flower
    mid = (top + bot) // 2
    px(a, mid, cx, WHITE)
    px(a, mid, cx + 1, YELLOW)
    px(a, mid - 1, cx, YELLOW)

draw_bell(a, 15, 13, 17, 5)
draw_bell(a, 15, 9, 12, 4)
draw_bell(a, 15, 5, 8, 3)
draw_bell(a, 15, 2, 4, 2)
draw_bell(a, 15, 0, 1, 1)

# Connecting stem between bells (gradient)
for y in range(1, 13):
    px(a, y, 14, S_LT)
    px(a, y, 15, S_MD)
    px(a, y, 16, S_MD)
    px(a, y, 17, S_DK)

# Bracts between bells
for by, bx, s in [(4, 11, -1), (4, 19, 1),
                   (8, 10, -1), (8, 20, 1),
                   (12, 9, -1), (12, 21, 1)]:
    for dy in range(-1, 2):
        for dx in range(1, 3):
            x = bx + dx * s
            if dy == 0:
                px(a, by + dy, x, B_LT)
            else:
                px(a, by + dy, x, B_MD)

# Calyx at base of spike
for x in range(11, 20):
    dx = abs(x - 15)
    if dx >= 3:
        px(a, 17, x, S_DP)
    elif dx >= 2:
        px(a, 17, x, S_DK)
    else:
        px(a, 17, x, S_MD)

# Main stem (5 shades)
for y in range(18, 32):
    px(a, y, 13, S_HL)  # highlight
    px(a, y, 14, S_LT)  # light
    px(a, y, 15, S_MD)  # mid
    px(a, y, 16, S_DK)  # dark
    px(a, y, 17, S_DP)  # shadow
    if y >= 28:
        px(a, y, 12, S_DK)
        px(a, y, 18, S_DP)

# Left leaf at y=27
for dy in range(-4, 5):
    w = 4 - abs(dy)
    if w < 1:
        continue
    for dx in range(1, w + 2):
        x = 12 - dx
        y = 27 + dy
        if dy < 0:
            px(a, y, x, S_LT if dx <= w//2 else S_MD)
        elif dy > 0:
            px(a, y, x, S_DK if dx <= w//2 else S_MD)
        else:
            px(a, y, x, S_HL)

# Right leaf at y=29
for dy in range(-3, 4):
    w = 3 - abs(dy)
    if w < 1:
        continue
    for dx in range(1, w + 2):
        x = 17 + dx
        y = 29 + dy
        if dy < 0:
            px(a, y, x, S_LT if dx <= w//2 else S_MD)
        elif dy > 0:
            px(a, y, x, S_DK if dx <= w//2 else S_MD)
        else:
            px(a, y, x, S_HL)

Image.fromarray(a, 'RGBA').save(f"{DST}\\bells_of_ireland.png", 'PNG')
n = int(np.sum(a[:,:,3] > 0))
c = len(set(tuple(a[y,x,:3]) for y in range(T) for x in range(T) if a[y,x,3] > 0))
print(f"bells_of_ireland: {n}px, {c}c")
