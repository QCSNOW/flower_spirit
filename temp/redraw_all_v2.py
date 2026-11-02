"""
Comprehensive redraw of all 12 BoP-style flower textures.
Key fixes:
- Natural stems: 2px wide, gradient light->dark, slight curve, leaves branching
- Flower clusters: not single columns, multiple blooms or proper petal structure
- Color transition: stem top blends into flower base
- Leaves: 3px oval with light top/dark bottom shading
"""
import numpy as np
from PIL import Image
import math

TARGET = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

# ========== COLOR PALETTES ==========
# Green stem system - 4 shades for gradient
G_VLIGHT = (145, 195, 55)   # brightest highlight
G_LIGHT  = (115, 170, 35)   # light green
G_MID    = (85, 145, 20)    # mid green  
G_DARK   = (55, 100, 10)    # dark shadow
G_DEEP   = (35, 75, 5)      # deepest shadow

def px(arr, y, x, color):
    """Set pixel if in bounds."""
    if 0 <= y < TARGET and 0 <= x < TARGET:
        r, g, b = color
        arr[y, x] = [r, g, b, 255]

def draw_stem(arr, cx, top_y, bot_y, curve=0):
    """Draw a natural tapered stem with gradient. curve>0 bends right."""
    for y in range(top_y, bot_y + 1):
        t = (y - top_y) / max(1, bot_y - top_y)
        offset = int(t * curve)
        x = cx + offset
        # 2px wide center with 3px at wider points
        px(arr, y, x, G_MID)
        px(arr, y, x + 1, G_MID)
        px(arr, y, x - 1, G_LIGHT)
        px(arr, y, x + 2, G_DARK)
        # Thicker at base
        if y > bot_y - 4:
            px(arr, y, x - 2, G_DARK)
            px(arr, y, x + 3, G_DEEP)

def draw_leaf_left(arr, cx, cy, size=3):
    """Draw a leaf pointing left from stem."""
    for dy in range(-size, size + 1):
        w = max(1, size - abs(dy))
        for dx in range(-w - 1, 0):
            y, x = cy + dy, cx + dx
            if dy < 0:
                px(arr, y, x, G_LIGHT)
            elif dy > 0:
                px(arr, y, x, G_DARK)
            else:
                px(arr, y, x, G_VLIGHT if dx > -w else G_MID)

def draw_leaf_right(arr, cx, cy, size=3):
    """Draw a leaf pointing right from stem."""
    for dy in range(-size, size + 1):
        w = max(1, size - abs(dy))
        for dx in range(1, w + 2):
            y, x = cy + dy, cx + dx
            if dy < 0:
                px(arr, y, x, G_LIGHT)
            elif dy > 0:
                px(arr, y, x, G_DARK)
            else:
                px(arr, y, x, G_VLIGHT if dx < w else G_MID)

def draw_stem_with_leaves(arr, cx, top_y, bot_y, curve=0, leaf_ys=None):
    """Draw stem with leaves at specified y positions."""
    draw_stem(arr, cx, top_y, bot_y, curve)
    if leaf_ys:
        for i, ly in enumerate(leaf_ys):
            if i % 2 == 0:
                draw_leaf_left(arr, cx, ly, size=3)
            else:
                draw_leaf_right(arr, cx + 1, ly, size=3)

def save(name, arr):
    """Save texture and print stats."""
    img = Image.fromarray(arr, 'RGBA')
    path = f"{DST}\\{name}.png"
    img.save(path, 'PNG')
    n = int(np.sum(arr[:,:,3] > 0))
    colors = set()
    for y in range(TARGET):
        for x in range(TARGET):
            if arr[y, x, 3] > 0:
                colors.add(tuple(arr[y, x, :3]))
    print(f"  {name}: {n}px, {len(colors)} colors")

def new_canvas():
    arr = np.zeros((TARGET, TARGET, 4), dtype=np.uint8)
    return arr


# ============================================================
# 1. WAXFLOWER - 5 small cream-white flowers in a cluster + stem
# ============================================================
print("1. Waxflower...")
arr = new_canvas()

# Flower colors
W1 = (252, 245, 220)  # cream white highlight
W2 = (240, 225, 190)  # cream
W3 = (220, 200, 160)  # cream shadow
P1 = (230, 200, 180)  # pale pink center
P2 = (200, 170, 150)  # darker pink

# 5 small flowers clustered at top 2/3
flower_positions = [(9, 5), (16, 4), (22, 6), (12, 11), (19, 12)]
for fcx, fcy in flower_positions:
    # Each flower: 5px circle with center dot
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            d = dx*dx + dy*dy
            if d <= 4:
                y, x = fcy + dy, fcx + dx
                if d == 0:
                    px(arr, y, x, P1)
                elif d <= 1:
                    px(arr, y, x, W1)
                elif d <= 2:
                    px(arr, y, x, W2)
                else:
                    px(arr, y, x, W3)

# Green leaves interspersed
for lx, ly in [(6, 7), (14, 8), (24, 9), (7, 13), (24, 14)]:
    px(arr, ly, lx, G_LIGHT)
    px(arr, ly, lx+1, G_VLIGHT)
    px(arr, ly+1, lx, G_MID)

# Stem
draw_stem_with_leaves(arr, 15, 16, 31, curve=1, leaf_ys=[20, 25])

save('waxflower', arr)


# ============================================================
# 2. ASTER - Radial purple flower + natural stem
# ============================================================
print("2. Aster...")
arr = new_canvas()

P_DEEP = (60, 30, 120)    # deep purple
P_MID  = (95, 55, 150)    # mid purple
P_LIGHT = (140, 100, 190) # light purple
P_PALE  = (175, 140, 220) # pale lavender
Y_BRIGHT = (250, 210, 50) # yellow center bright
Y_DARK  = (210, 165, 25)  # yellow center dark

cx, cy = 16, 9
# 14 radial petals
for i in range(14):
    angle = i * (360/14) * math.pi / 180
    for r in range(3, 8):
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        if r < 5:
            px(arr, y, x, P_LIGHT)
        elif r < 7:
            px(arr, y, x, P_MID)
        else:
            px(arr, y, x, P_DEEP)
    # Petal tip
    x = cx + int(round(7 * math.cos(angle)))
    y = cy + int(round(7 * math.sin(angle)))
    px(arr, y, x, P_PALE)

# Fill gaps
for y in range(3, 16):
    for x in range(9, 24):
        if arr[y, x, 3] == 0:
            dist = math.sqrt((x-cx)**2 + (y-cy)**2)
            if 3 <= dist <= 7:
                has_n = any(arr[y+dy, x+dx, 3] > 0 for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= y+dy < 32 and 0 <= x+dx < 32)
                if has_n:
                    px(arr, y, x, P_LIGHT)

# Yellow center
for dy in range(-2, 3):
    for dx in range(-2, 3):
        d = dx*dx + dy*dy
        if d <= 4:
            if d <= 1: px(arr, cy+dy, cx+dx, Y_BRIGHT)
            elif d <= 2: px(arr, cy+dy, cx+dx, Y_DARK)
            else: px(arr, cy+dy, cx+dx, P_DEEP)

# Transition: base of flower to stem
for x in range(14, 19):
    px(arr, 17, x, G_DARK)
    px(arr, 18, x, G_MID)

# Natural stem
draw_stem_with_leaves(arr, 16, 18, 31, curve=-1, leaf_ys=[22, 27])

save('aster', arr)


# ============================================================
# 3. DANCING LADY - 3 yellow flowers on arching stem
# ============================================================
print("3. Dancing Lady...")
arr = new_canvas()

Y1 = (252, 220, 60)   # bright yellow
Y2 = (240, 190, 30)   # yellow
Y3 = (210, 160, 10)   # deep yellow
B1 = (139, 69, 19)     # brown spots

def draw_dancing_flower(arr, cx, cy):
    """Small orchid flower: 3 upper petals + large lower lip"""
    # Upper petals
    for dy, dx, c in [(-3, 0, Y2), (-3, 1, Y1), (-2, -1, Y2), (-2, 0, Y1), (-2, 1, Y1), (-2, 2, Y2)]:
        px(arr, cy+dy, cx+dx, c)
    # Side petals
    for dy, dx, c in [(-1, -2, Y2), (-1, -1, Y1), (-1, 0, B1), (-1, 1, Y1), (-1, 2, Y2), (-1, 3, Y3)]:
        px(arr, cy+dy, cx+dx, c)
    # Lower lip (large)
    for dy, dx, c in [(0, -2, Y3), (0, -1, Y1), (0, 0, B1), (0, 1, Y1), (0, 2, Y3),
                       (1, -1, Y3), (1, 0, Y2), (1, 1, Y3)]:
        px(arr, cy+dy, cx+dx, c)

# 3 flowers along arching stem
draw_dancing_flower(arr, 10, 3)   # left upper
draw_dancing_flower(arr, 17, 7)   # center
draw_dancing_flower(arr, 21, 12)  # right lower

# Arching stem connecting flowers
for y, x in [(5, 12), (5, 13), (6, 13), (6, 14), (6, 15)]:
    px(arr, y, x, G_MID)
    px(arr, y, x+1, G_LIGHT)
for y, x in [(9, 15), (9, 16), (10, 16), (10, 17), (10, 18)]:
    px(arr, y, x, G_MID)
    px(arr, y, x+1, G_LIGHT)
for y, x in [(13, 18), (13, 19), (14, 19), (14, 20)]:
    px(arr, y, x, G_MID)
    px(arr, y, x+1, G_LIGHT)

# Main stem going down from (19, 14)
draw_stem_with_leaves(arr, 16, 16, 31, curve=2, leaf_ys=[20, 25])

save('dancing_lady', arr)


# ============================================================
# 4. CHAMOMILE - Daisy with proper stem
# ============================================================
print("4. Chamomile...")
arr = new_canvas()

W1 = (252, 252, 252)
W2 = (235, 235, 235)
W3 = (210, 210, 210)
YC1 = (252, 220, 60)
YC2 = (230, 180, 30)

cx, cy = 16, 8
# 16 white petals
for i in range(16):
    angle = i * (360/16) * math.pi / 180
    for r in range(3, 6):
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        if r < 5:
            px(arr, y, x, W1)
        else:
            px(arr, y, x, W2)
    # Tip
    x = cx + int(round(6 * math.cos(angle)))
    y = cy + int(round(6 * math.sin(angle)))
    px(arr, y, x, W3)

# Fill petal gaps
for y in range(3, 14):
    for x in range(10, 23):
        if arr[y, x, 3] == 0:
            dist = math.sqrt((x-cx)**2 + (y-cy)**2)
            if 2 <= dist <= 6:
                has_n = any(arr[y+dy, x+dx, 3] > 0 for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= y+dy < 32 and 0 <= x+dx < 32)
                if has_n:
                    px(arr, y, x, W2)

# Yellow center
for dy in range(-1, 2):
    for dx in range(-1, 2):
        if dx*dx + dy*dy <= 1:
            px(arr, cy+dy, cx+dx, YC1)
        else:
            px(arr, cy+dy, cx+dx, YC2)

# Transition to stem
for x in range(14, 19):
    px(arr, 13, x, G_DARK)

# Natural stem
draw_stem_with_leaves(arr, 16, 14, 31, curve=-1, leaf_ys=[18, 24])

save('chamomile', arr)


# ============================================================
# 5. ONCIDIUM - 4 yellow flowers on vertical stem
# ============================================================
print("5. Oncidium...")
arr = new_canvas()

def draw_onc_flower(arr, cx, cy):
    """Compact orchid flower"""
    for dy, dx, c in [(-3, 0, Y2), (-3, 1, Y1), (-2, -1, Y2), (-2, 0, Y1), (-2, 1, Y1), (-2, 2, Y2),
                       (-1, -2, Y2), (-1, -1, Y1), (-1, 0, B1), (-1, 1, Y1), (-1, 2, Y2), (-1, 3, Y3),
                       (0, -2, Y3), (0, -1, Y1), (0, 0, B1), (0, 1, Y1), (0, 2, Y3),
                       (1, -1, Y3), (1, 0, Y2), (1, 1, Y3)]:
        px(arr, cy+dy, cx+dx, c)

# 4 flowers
draw_onc_flower(arr, 15, 3)
draw_onc_flower(arr, 10, 9)
draw_onc_flower(arr, 21, 9)
draw_onc_flower(arr, 15, 15)

# Connecting stem segments
for y in range(6, 9):
    px(arr, y, 15, G_MID); px(arr, y, 16, G_LIGHT)
for y in range(12, 15):
    px(arr, y, 15, G_MID); px(arr, y, 16, G_LIGHT)

# Main stem
draw_stem_with_leaves(arr, 16, 18, 31, curve=1, leaf_ys=[22, 27])

save('oncidium', arr)


# ============================================================
# 6. ANEMONE - Cup-shaped flower + stem
# ============================================================
print("6. Anemone...")
arr = new_canvas()

P_DEEP = (50, 20, 100)
P_DARK = (80, 40, 130)
P_MID  = (120, 70, 160)
P_LIGHT = (160, 110, 200)
P_PALE = (195, 150, 225)
B_CENTER = (40, 30, 60)  # dark center

cx, cy = 16, 9
# 6 large cup petals
for i in range(6):
    angle = i * 60 * math.pi / 180 + math.pi / 6  # offset
    for r in range(2, 9):
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        if r < 4:
            px(arr, y, x, P_MID)
        elif r < 6:
            px(arr, y, x, P_DARK)
        elif r < 8:
            px(arr, y, x, P_LIGHT)
        else:
            px(arr, y, x, P_PALE)
    # Petal tip
    for r in [8]:
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        px(arr, y, x, P_PALE)

# Fill between petals
for y in range(2, 17):
    for x in range(8, 25):
        if arr[y, x, 3] == 0:
            dist = math.sqrt((x-cx)**2 + (y-cy)**2)
            if 2 <= dist <= 8:
                has_n = any(arr[y+dy, x+dx, 3] > 0 for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= y+dy < 32 and 0 <= x+dx < 32)
                if has_n:
                    px(arr, y, x, P_MID if dist < 5 else P_LIGHT)

# Dark center
for dy in range(-2, 3):
    for dx in range(-2, 3):
        if dx*dx + dy*dy <= 3:
            px(arr, cy+dy, cx+dx, B_CENTER)

# Transition + stem
for x in range(14, 19):
    px(arr, 17, x, G_DARK)
draw_stem_with_leaves(arr, 16, 17, 31, curve=-1, leaf_ys=[21, 26])

save('anemone', arr)


# ============================================================
# 7. ASTILBE - Feathery plume + stem
# ============================================================
print("7. Astilbe...")
arr = new_canvas()

P1 = (220, 100, 140)   # pink bright
P2 = (200, 80, 120)    # pink mid
P3 = (170, 60, 100)    # pink dark
P4 = (240, 150, 170)   # pale pink
P5 = (150, 40, 80)     # deep pink base

# Feathery plume - triangular fluffy shape at top
# Row by row, getting wider then narrower
plume_rows = [
    (2, [16], [P4]),
    (3, [15, 16], [P1, P4]),
    (4, [14, 15, 16, 17], [P2, P1, P4, P1]),
    (5, [13, 14, 15, 16, 17, 18], [P3, P2, P1, P4, P1, P2]),
    (6, [12, 13, 14, 15, 16, 17, 18, 19], [P5, P3, P2, P1, P4, P1, P2, P3]),
    (7, [11, 12, 13, 14, 15, 16, 17, 18, 19, 20], [P5, P3, P2, P1, P4, P4, P1, P2, P3, P5]),
    (8, [11, 12, 13, 14, 15, 16, 17, 18, 19, 20], [P5, P3, P2, P1, P4, P4, P1, P2, P3, P5]),
    (9, [12, 13, 14, 15, 16, 17, 18, 19], [P3, P2, P1, P4, P4, P1, P2, P3]),
    (10, [12, 13, 14, 15, 16, 17, 18, 19], [P3, P2, P1, P4, P4, P1, P2, P3]),
    (11, [13, 14, 15, 16, 17, 18], [P2, P1, P4, P4, P1, P2]),
    (12, [13, 14, 15, 16, 17, 18], [P2, P1, P4, P4, P1, P2]),
    (13, [14, 15, 16, 17], [P2, P1, P4, P2]),
    (14, [15, 16], [P3, P2]),
    (15, [16], [P5]),
]

for row_y, xs, colors in plume_rows:
    for i, x in enumerate(xs):
        c = colors[i] if i < len(colors) else P2
        px(arr, row_y, x, c)
        # Add fluff: scatter pixels around
        if i % 2 == 0 and row_y < 13:
            px(arr, row_y - 1, x, P4)

# Small green leaves at base of plume
px(arr, 15, 14, G_LIGHT)
px(arr, 15, 18, G_LIGHT)

# Stem
draw_stem_with_leaves(arr, 16, 15, 31, curve=0, leaf_ys=[20, 25])

save('astilbe', arr)


# ============================================================
# 8. HYDRANGEA - Ball cluster + stem
# ============================================================
print("8. Hydrangea...")
arr = new_canvas()

B_DEEP = (40, 60, 140)
B_DARK = (60, 90, 170)
B_MID  = (90, 120, 200)
B_LIGHT = (130, 160, 225)
B_PALE  = (170, 195, 240)
G_LEAF = (90, 155, 35)

cx, cy = 16, 9
# Ball of small 4-petal flowers
# Each "mini flower" is a plus shape
mini_flower_positions = []
for ring in range(4, 0, -1):
    count = ring * 4
    for i in range(count):
        angle = i * (360/count) * math.pi / 180
        r = ring * 2
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        if 4 <= x <= 28 and 1 <= y <= 17:
            mini_flower_positions.append((x, y))

# Center flower
mini_flower_positions.append((cx, cy))
# Add some more
for dy in range(-3, 4):
    for dx in range(-4, 5):
        d = math.sqrt(dx*dx + dy*dy)
        if d <= 6 and (cx+dx, cy+dy) not in [(p[0], p[1]) for p in mini_flower_positions]:
            if d <= 3 or abs(dx) <= 1 or abs(dy) <= 1:
                mini_flower_positions.append((cx+dx, cy+dy))

# Draw mini flowers
for fx, fy in mini_flower_positions:
    if 0 <= fx < 32 and 0 <= fy < 32:
        dist = math.sqrt((fx-cx)**2 + (fy-cy)**2)
        if dist < 2:
            c1, c2 = B_PALE, B_LIGHT
        elif dist < 4:
            c1, c2 = B_LIGHT, B_MID
        else:
            c1, c2 = B_MID, B_DARK
        # Plus shape (4 petals)
        px(arr, fy, fx, c1)  # center
        px(arr, fy-1, fx, c2)  # top
        px(arr, fy+1, fx, c2)  # bottom
        px(arr, fy, fx-1, c2)  # left
        px(arr, fy, fx+1, c2)  # right

# Green sepals at base
for x in range(13, 20):
    px(arr, 16, x, G_DARK)

# Stem
draw_stem_with_leaves(arr, 16, 17, 31, curve=1, leaf_ys=[21, 26])

save('hydrangea', arr)


# ============================================================
# 9. BELLS OF IRELAND - 5 green bell calyces on stem
# ============================================================
print("9. Bells of Ireland...")
arr = new_canvas()

def draw_bell(arr, cx, top_y, bot_y, width):
    """Bell-shaped calyx: narrow top, wide middle, narrow bottom"""
    rows = bot_y - top_y + 1
    for i in range(rows):
        y = top_y + i
        t = i / max(1, rows - 1)
        if t < 0.25:
            w = max(1, int(width * 0.5))
        elif t < 0.75:
            w = width
        else:
            w = max(1, int(width * 0.7))
        
        for dx in range(-w, w + 1):
            x = cx + dx
            if abs(dx) == w:
                px(arr, y, x, G_DEEP)    # edge
            elif abs(dx) == w - 1:
                px(arr, y, x, G_DARK)    # inner shadow
            elif abs(dx) <= 1:
                px(arr, y, x, G_VLIGHT) # highlight
            elif abs(dx) <= 2:
                px(arr, y, x, G_LIGHT)
            else:
                px(arr, y, x, G_MID)
    
    # Tiny white flower inside bell
    px(arr, top_y + rows // 2, cx, (240, 235, 200))

# 5 bells stacked
bells = [(16, 1, 4, 3), (16, 5, 8, 4), (16, 9, 12, 4), (16, 13, 16, 4), (16, 17, 20, 4)]
for bx, top, bot, w in bells:
    draw_bell(arr, bx, top, bot, w)

# Stem below
draw_stem_with_leaves(arr, 16, 21, 31, curve=0, leaf_ys=[25])

save('bells_of_ireland', arr)


# ============================================================
# 10. HYPERICUM - 3 red berries with stamen + stem
# ============================================================
print("10. Hypericum...")
arr = new_canvas()

R1 = (220, 40, 40)    # bright red
R2 = (190, 25, 25)    # red
R3 = (150, 15, 15)    # dark red
R4 = (240, 80, 60)    # highlight
R5 = (100, 10, 10)    # deepest
F1 = (200, 180, 100)  # filament tan

# 3 berries
berry_positions = [(11, 4), (20, 5), (15, 10)]
for bx, by in berry_positions:
    # Berry circle
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            d = dx*dx + dy*dy
            if d <= 9:
                y, x = by + dy, bx + dx
                if d == 0:
                    px(arr, y, x, R4)  # center highlight
                elif d <= 2:
                    px(arr, y, x, R1)
                elif d <= 5:
                    px(arr, y, x, R2)
                elif d <= 7:
                    px(arr, y, x, R3)
                else:
                    px(arr, y, x, R5)
    
    # Stamen filaments radiating
    for angle_i in range(8):
        angle = angle_i * 45 * math.pi / 180
        x = bx + int(round(4 * math.cos(angle)))
        y = by + int(round(4 * math.sin(angle)))
        px(arr, y, x, F1)

# Small green leaves between berries
for lx, ly in [(7, 5), (24, 6), (8, 10), (23, 11)]:
    px(arr, ly, lx, G_LIGHT)
    px(arr, ly, lx+1, G_VLIGHT)

# Connecting stem segments
for y in range(7, 10):
    px(arr, y, 15, G_MID); px(arr, y, 16, G_LIGHT)
for y in range(13, 15):
    px(arr, y, 16, G_MID); px(arr, y, 17, G_LIGHT)

# Main stem
draw_stem_with_leaves(arr, 16, 15, 31, curve=-1, leaf_ys=[19, 25])

save('hypericum', arr)


# ============================================================
# 11. LUPINE - Tower of small flowers + stem
# ============================================================
print("11. Lupine...")
arr = new_canvas()

P_DEEP = (100, 40, 130)
P_DARK = (130, 60, 160)
P_MID  = (160, 90, 185)
P_LIGHT = (190, 120, 210)
P_PALE = (220, 160, 235)

# Tower: 6 tiers of flowers, each tier 3-4 flowers in a ring
tiers = [
    (3, 2, [P_PALE]),
    (5, 3, [P_LIGHT, P_PALE, P_LIGHT]),
    (7, 4, [P_MID, P_LIGHT, P_PALE, P_LIGHT]),
    (9, 5, [P_DARK, P_MID, P_LIGHT, P_PALE, P_LIGHT]),
    (11, 5, [P_DEEP, P_DARK, P_MID, P_LIGHT, P_MID]),
    (13, 4, [P_DEEP, P_DARK, P_MID, P_DARK]),
    (15, 3, [P_DEEP, P_DARK, P_DEEP]),
]

for y, count, colors in tiers:
    for i in range(count):
        x = 16 - count + 1 + i * 2
        # Small pea-like flower (3px)
        c = colors[i % len(colors)]
        px(arr, y, x, c)
        px(arr, y, x+1, c)
        px(arr, y-1, x, P_PALE if i % 2 == 0 else P_LIGHT)
        # Bud shape
        if y < 13:
            px(arr, y+1, x, P_DARK)

# Green calyx under each flower
for y in [4, 6, 8, 10, 12, 14]:
    for x in range(12, 21):
        if arr[y, x, 3] == 0:
            px(arr, y, x, G_DARK)

# Leaves at base
draw_leaf_left(arr, 15, 2, size=2)
draw_leaf_right(arr, 16, 2, size=2)

# Stem
draw_stem_with_leaves(arr, 16, 15, 31, curve=0, leaf_ys=[20, 26])

save('lupine', arr)


# ============================================================
# 12. WINTERSWEET - Branch with yellow flowers
# ============================================================
print("12. Wintersweet...")
arr = new_canvas()

Y1 = (250, 220, 80)   # bright yellow
Y2 = (230, 190, 50)   # yellow
Y3 = (200, 160, 30)   # deep yellow
B1 = (139, 90, 40)     # brown branch
B2 = (100, 65, 25)     # dark brown
B3 = (80, 50, 15)      # deepest brown
P_CENTER = (140, 60, 80)  # purplish center

def draw_wintersweet_flower(arr, cx, cy):
    """Small waxy flower: 5 petals + center"""
    for dy, dx, c in [(-2, 0, Y2), (-1, -1, Y1), (-1, 0, Y2), (-1, 1, Y1),
                       (0, -2, Y2), (0, -1, Y1), (0, 0, P_CENTER), (0, 1, Y1), (0, 2, Y2),
                       (1, -1, Y1), (1, 0, Y2), (1, 1, Y1),
                       (2, 0, Y3)]:
        px(arr, cy+dy, cx+dx, c)

# Branch: diagonal from lower-left to upper-right
branch_path = [(31, 3), (30, 4), (29, 5), (28, 6), (27, 7), (26, 8),
                (25, 9), (24, 10), (23, 11), (22, 12), (21, 13), (20, 14),
                (19, 15), (18, 16), (17, 17), (16, 18), (15, 19),
                (14, 20), (13, 21), (12, 22)]

for i, (y, x) in enumerate(branch_path):
    c = B1 if i % 3 != 0 else B2
    px(arr, y, x, c)
    if i % 2 == 0:
        px(arr, y, x + 1, B2)
    else:
        px(arr, y + 1, x, B3)

# Flowers along branch
flower_positions = [(5, 28), (9, 24), (13, 20), (18, 15), (22, 11)]
for fy, fx in flower_positions:
    draw_wintersweet_flower(arr, fx, fy)

# Small leaves
for lx, ly in [(7, 25), (15, 17), (25, 7)]:
    px(arr, ly, lx, G_MID)
    px(arr, ly, lx+1, G_LIGHT)

save('wintersweet', arr)

print("\n=== ALL DONE ===")
