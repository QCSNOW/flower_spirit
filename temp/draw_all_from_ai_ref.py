"""Rebuild all 12 flowers pixel-by-pixel, using AI reference as design guide.
Each flower is drawn programmatically to ensure clean pixel art quality.
Strategy: AI reference determines color palette and overall shape, 
but the actual pixel placement is done programmatically for precision.
"""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

# Standard green palette (6 shades)
G1 = (160, 215, 70)    # highlight
G2 = (130, 190, 40)    # light
G3 = (95, 155, 25)     # mid
G4 = (65, 115, 12)     # dark
G5 = (40, 75, 5)       # darkest
G_CALY = (50, 90, 10)  # calyx

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

def stem(a, cx, top, bot=31, curve=0):
    """Draw 4px gradient stem."""
    for y in range(top, bot + 1):
        t = (y - top) / max(1, bot - top)
        x = cx + int(t * curve)
        px(a, y, x - 1, G1)
        px(a, y, x, G3)
        px(a, y, x + 1, G3)
        px(a, y, x + 2, G4)
        if y >= bot - 3:
            px(a, y, x - 2, G4)
            px(a, y, x + 3, G5)

def leaf(a, cx, cy, side, size=4):
    """Lanceolate leaf with upper-light / lower-dark gradient."""
    for dy in range(-size, size + 1):
        w = max(1, size - abs(dy))
        for dx in range(1, w + 2):
            x = cx + dx * side
            y = cy + dy
            if dy < 0:
                px(a, y, x, G2 if dx <= w // 2 + 1 else G3)
            elif dy > 0:
                px(a, y, x, G4 if dx <= w // 2 + 1 else G3)
            else:
                px(a, y, x, G1)

def calyx(a, cx, y, w=4):
    """Dark green calyx band at flower base."""
    for dx in range(-w, w + 1):
        x = cx + dx
        if abs(dx) == w:
            px(a, y, x, G5)
        elif abs(dx) >= w - 1:
            px(a, y, x, G4)
        else:
            px(a, y, x, G_CALY)

def save(arr, name):
    Image.fromarray(arr, 'RGBA').save(f"{DST}\\{name}.png", 'PNG')
    n = int(np.sum(arr[:,:,3] > 0))
    c = len(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0))
    print(f"  {name:20s}: {n:4d}px, {c:2d}c")


# ===== 1. WAXFLOWER =====
# Dense cluster of 5-6 creamy white flowers with pink centers
# Based on AI ref: round cluster shape, small pink center per flower
a = np.zeros((T, T, 4), dtype=np.uint8)

# Petal colors: cream/white gradient
W_DK = (175, 165, 145)   # dark edge
W_MD = (210, 200, 175)   # mid cream
W_LT = (235, 225, 205)   # light cream
W_HL = (250, 245, 225)   # highlight

P_DK = (200, 60, 120)    # dark pink center
P_MD = (230, 90, 150)    # mid pink
P_LT = (245, 130, 180)   # light pink

# Flower positions within cluster
flowers = [
    (15, 5, 3),    # top center
    (9, 9, 3),     # top left
    (21, 9, 3),    # top right
    (12, 13, 3),   # mid left
    (18, 13, 3),   # mid right
    (15, 17, 3),   # bottom center
]

def waxflower_single(a, cx, cy, r):
    """Draw a single 5-petal waxflower."""
    # 5 petals in radial pattern: top, bottom-left, bottom-right, left, right
    # Simple approach: rounded blob shape with pink center
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            dist = dx*dx + dy*dy
            if dist <= r*r:
                x = cx + dx
                y = cy + dy
                # Color by distance from center
                if dist <= 1:
                    px(a, y, x, P_LT)  # pink center
                elif dist <= 2:
                    px(a, y, x, P_MD)
                elif dist <= r * r * 0.3:
                    px(a, y, x, W_HL)
                elif dist <= r * r * 0.6:
                    px(a, y, x, W_LT)
                elif dist <= r * r * 0.85:
                    px(a, y, x, W_MD)
                else:
                    px(a, y, x, W_DK)

for fx, fy, r in flowers:
    waxflower_single(a, fx, fy, r)

# Small green leaves peeking from cluster
leaf(a, 5, 10, -1, 2)
leaf(a, 26, 10, 1, 2)

# Calyx and stem
calyx(a, 15, 19, w=5)
stem(a, 15, 20, 31)
leaf(a, 14, 26, -1, 3)
leaf(a, 16, 28, 1, 3)

save(a, "waxflower")


# ===== 2. ASTER =====
# Purple daisy with yellow center
# AI ref: 12-14 purple petals radiating from yellow disc
a = np.zeros((T, T, 4), dtype=np.uint8)
import math

# Purple petal colors
P_DK = (70, 35, 120)
P_MD = (105, 65, 165)
P_LT = (145, 100, 200)
P_HL = (180, 140, 225)

# Yellow center colors
Y_DK = (200, 150, 10)
Y_MD = (230, 180, 30)
Y_LT = (250, 215, 60)

cx, cy = 15, 8
n_petals = 12
petal_len = 7

for i in range(n_petals):
    angle = i * 360 / n_petals * math.pi / 180
    for r in range(2, petal_len + 1):
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        # Petal gradient: darker at base, lighter at tip
        t = r / petal_len
        if t < 0.3:
            c = P_DK
        elif t < 0.6:
            c = P_MD
        elif t < 0.85:
            c = P_LT
        else:
            c = P_HL
        px(a, y, x, c)
        # Slight petal width (add perpendicular pixel)
        perp_angle = angle + math.pi / 2
        px(a, y + int(round(0.5 * math.sin(perp_angle))),
           x + int(round(0.5 * math.cos(perp_angle))), c)

# Yellow center disc (3-layer gradient)
for dy in range(-2, 3):
    for dx in range(-2, 3):
        dist = dx*dx + dy*dy
        if dist <= 5:
            if dist <= 2:
                c = Y_LT
            elif dist <= 4:
                c = Y_MD
            else:
                c = Y_DK
            px(a, cy + dy, cx + dx, c)

calyx(a, 15, 15, w=4)
stem(a, 15, 16, 31)
leaf(a, 14, 22, -1, 3)
leaf(a, 16, 26, 1, 3)

save(a, "aster")


# ===== 3. DANCING LADY ORCHID =====
# Arching stem with yellow orchid flowers
# AI ref: curved green stem, 3 yellow flowers cascading down right side
a = np.zeros((T, T, 4), dtype=np.uint8)

# Yellow colors
Y_DK = (190, 130, 5)
Y_MD = (225, 170, 25)
Y_LT = (250, 210, 55)
Y_HL = (255, 235, 110)

R_SPOT = (170, 60, 40)  # red-brown spots

def dancing_flower(a, fx, fy):
    """Single dancing lady orchid: large lip + small upper petals."""
    # Large lower lip (main feature)
    for dy in range(-1, 3):
        w = 3 - abs(dy - 1)
        if w < 1:
            continue
        for dx in range(-w, w + 1):
            x = fx + dx
            y = fy + dy
            if dy == 2 and abs(dx) <= 1:
                px(a, y, x, Y_DK)
            elif abs(dx) <= 1:
                px(a, y, x, Y_HL if dy <= 0 else Y_LT)
            else:
                px(a, y, x, Y_LT if dy <= 0 else Y_MD)
    
    # Upper petals (smaller)
    px(a, fy - 2, fx, Y_MD)
    px(a, fy - 2, fx - 1, Y_LT)
    px(a, fy - 2, fx + 1, Y_LT)
    px(a, fy - 3, fx, Y_LT)
    
    # Side petals
    px(a, fy - 1, fx - 2, Y_MD)
    px(a, fy - 1, fx + 2, Y_MD)
    
    # Reddish-brown center spot
    px(a, fy, fx, R_SPOT)
    px(a, fy + 1, fx, R_SPOT)

# 3 flowers along a curve going right-down
dancing_flower(a, 22, 3)   # top right
dancing_flower(a, 24, 9)   # middle right
dancing_flower(a, 22, 15)  # bottom right

# Curved stem from bottom-left to top-right flowers
# Draw arched stem
stem_pts = []
for i in range(17):
    t = i / 16
    # Curve: starts at (10, 31), arcs to (22, 3)
    # Quadratic bezier-like curve
    sx, sy = 10, 31  # start
    mx, my = 5, 18   # control point (left arc)
    ex, ey = 21, 4   # end
    x = int((1-t)*(1-t)*sx + 2*(1-t)*t*mx + t*t*ex)
    y = int((1-t)*(1-t)*sy + 2*(1-t)*t*my + t*t*ey)
    stem_pts.append((x, y))

for sx, sy in stem_pts:
    px(a, sy, sx - 1, G1)
    px(a, sy, sx, G3)
    px(a, sy, sx + 1, G3)
    px(a, sy, sx + 2, G4)

# Side leaf
leaf(a, 9, 26, -1, 3)

save(a, "dancing_lady")


# ===== 4. CHAMOMILE =====
# White daisy with yellow center
a = np.zeros((T, T, 4), dtype=np.uint8)

# White petal colors
W_DK = (190, 190, 195)
W_MD = (220, 220, 225)
W_LT = (240, 240, 245)

# Yellow center
Y_DK = (210, 160, 10)
Y_MD = (240, 190, 30)
Y_LT = (255, 220, 70)

cx, cy = 15, 9
n_petals = 14
petal_len = 7

for i in range(n_petals):
    angle = i * 360 / n_petals * math.pi / 180
    for r in range(2, petal_len + 1):
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        t = r / petal_len
        if t < 0.4:
            c = W_DK
        elif t < 0.75:
            c = W_MD
        else:
            c = W_LT
        px(a, y, x, c)

# Yellow center
for dy in range(-3, 4):
    for dx in range(-3, 4):
        dist = dx*dx + dy*dy
        if dist <= 8:
            if dist <= 3:
                c = Y_LT
            elif dist <= 6:
                c = Y_MD
            else:
                c = Y_DK
            px(a, cy + dy, cx + dx, c)

calyx(a, 15, 17, w=4)
stem(a, 15, 18, 31)
leaf(a, 14, 24, -1, 3)
leaf(a, 16, 27, 1, 3)

save(a, "chamomile")


# ===== 5. ONCIDIUM =====
# Vertical spike of yellow orchids
# AI ref: 4-5 yellow flowers on upright stem
a = np.zeros((T, T, 4), dtype=np.uint8)

Y_DK = (195, 135, 5)
Y_MD = (225, 170, 25)
Y_LT = (250, 205, 55)
Y_HL = (255, 230, 110)
R_CTR = (160, 55, 35)

def oncidium_flower(a, fx, fy, size=2):
    """Small oncidium flower on a spike."""
    # Lower lip (larger)
    for dy in range(size):
        w = size + 1 - dy
        for dx in range(-w, w + 1):
            y = fy + dy
            x = fx + dx
            if abs(dx) <= 1:
                px(a, y, x, Y_HL if dy == 0 else Y_LT)
            else:
                px(a, y, x, Y_LT if dy == 0 else Y_MD)
    
    # Upper petals
    px(a, fy - 1, fx, Y_MD)
    px(a, fy - 1, fx - 1, Y_LT)
    px(a, fy - 1, fx + 1, Y_LT)
    px(a, fy - 2, fx, Y_LT)
    
    # Side petals
    px(a, fy, fx - size - 1, Y_MD)
    px(a, fy, fx + size + 1, Y_MD)
    
    # Center
    px(a, fy, fx, R_CTR)

# Flowers alternating left/right on stem
oncidium_flower(a, 12, 5, 2)
oncidium_flower(a, 19, 8, 2)
oncidium_flower(a, 11, 12, 2)
oncidium_flower(a, 20, 15, 2)
oncidium_flower(a, 12, 18, 2)

# Top bud
px(a, 2, 15, Y_DK)
px(a, 3, 14, Y_MD)
px(a, 3, 15, Y_LT)
px(a, 3, 16, Y_MD)
px(a, 4, 15, Y_LT)

calyx(a, 15, 20, w=3)
stem(a, 15, 21, 31)
leaf(a, 14, 26, -1, 3)
leaf(a, 16, 28, 1, 3)

save(a, "oncidium")


# ===== 6. ANEMONE =====
# Large purple cup flower with dark center
# AI ref: 6-7 broad petals, dark near-black center
a = np.zeros((T, T, 4), dtype=np.uint8)

P_DK = (55, 25, 100)
P_MD = (90, 50, 150)
P_LT = (130, 85, 190)
P_HL = (170, 130, 220)

C_DK = (25, 10, 40)     # dark center
C_MD = (45, 20, 70)
C_LT = (120, 70, 140)

cx, cy = 15, 10
n_petals = 7
petal_len = 9

for i in range(n_petals):
    angle = i * 360 / n_petals * math.pi / 180
    for r in range(2, petal_len + 1):
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        # Add width
        perp = angle + math.pi / 2
        for w in range(2):
            wx = x + int(round(w * math.cos(perp)))
            wy = y + int(round(w * math.sin(perp)))
        
        t = r / petal_len
        if t < 0.25:
            c = P_DK
        elif t < 0.55:
            c = P_MD
        elif t < 0.8:
            c = P_LT
        else:
            c = P_HL
        px(a, y, x, c)
        # Thicker petals
        perp_x = x + int(round(0.7 * math.cos(perp)))
        perp_y = y + int(round(0.7 * math.sin(perp)))
        px(a, perp_y, perp_x, c)

# Dark center
for dy in range(-2, 3):
    for dx in range(-2, 3):
        dist = dx*dx + dy*dy
        if dist <= 5:
            if dist <= 2:
                c = C_DK
            elif dist <= 4:
                c = C_MD
            else:
                c = C_LT
            px(a, cy + dy, cx + dx, c)

calyx(a, 15, 19, w=5)
stem(a, 15, 20, 31)
leaf(a, 14, 25, -1, 3)
leaf(a, 16, 27, 1, 3)

save(a, "anemone")


# ===== 7. ASTILBE =====
# Feathery pink plume
# AI ref: tall conical plume, light pink gradient
a = np.zeros((T, T, 4), dtype=np.uint8)

P1 = (255, 200, 220)   # lightest
P2 = (255, 160, 195)
P3 = (240, 120, 170)
P4 = (215, 85, 145)
P5 = (185, 55, 120)    # darkest

cx = 15

# Feather plume: tapered shape with feathery edges
# Each row has a width, with some random-looking "feather" pixels
plume_top = 2
plume_bot = 20

for y in range(plume_top, plume_bot + 1):
    t = (y - plume_top) / max(1, plume_bot - plume_top)
    # Width: narrow top -> wider middle -> narrow bottom
    if t < 0.3:
        w = int(1 + t * 20)
    elif t < 0.7:
        w = 7
    else:
        w = int(7 - (t - 0.7) * 15)
    w = max(1, w)
    
    # Main plume body
    for dx in range(-w, w + 1):
        x = cx + dx
        # Color gradient: light top -> dark bottom
        abs_d = abs(dx)
        if t < 0.25:
            c = P1 if abs_d <= 1 else P2
        elif t < 0.5:
            c = P2 if abs_d <= 2 else P3
        elif t < 0.75:
            c = P3 if abs_d <= 2 else P4
        else:
            c = P4 if abs_d <= 2 else P5
        px(a, y, x, c)
    
    # Feathery side extensions (every few rows)
    if y % 2 == 0:
        px(a, y, cx - w - 1, P3 if t < 0.5 else P4)
        px(a, y, cx + w + 1, P3 if t < 0.5 else P4)
    if y % 3 == 0:
        px(a, y, cx - w - 2, P4)
        px(a, y, cx + w + 2, P4)

calyx(a, 15, 21, w=4)
stem(a, 15, 22, 31)
leaf(a, 14, 27, -1, 3)
leaf(a, 16, 29, 1, 3)

save(a, "astilbe")


# ===== 8. HYDRANGEA =====
# Round blue mophead cluster
# AI ref: dense spherical cluster of small 4-petal flowers
a = np.zeros((T, T, 4), dtype=np.uint8)

B_DK = (30, 70, 160)
B_MD = (60, 110, 200)
B_LT = (100, 155, 230)
B_HL = (150, 195, 245)
B_PALE = (200, 225, 250)

cx, cy = 15, 11
cluster_r = 9

# Fill cluster shape with flower texture
for dy in range(-cluster_r, cluster_r + 1):
    for dx in range(-cluster_r, cluster_r + 1):
        dist = dx*dx + dy*dy
        if dist <= cluster_r * cluster_r:
            x = cx + dx
            y = cy + dy
            
            # Edge darkening
            edge_t = dist / (cluster_r * cluster_r)
            if edge_t > 0.85:
                c = B_DK
            elif edge_t > 0.6:
                c = B_MD
            else:
                # Inner: pattern of small flower centers (lighter dots)
                # Create a grid of lighter dots representing individual floret centers
                grid_x = (dx + 100) % 3
                grid_y = (dy + 100) % 3
                if grid_x == 1 and grid_y == 1:
                    c = B_PALE
                elif grid_x == 0 and grid_y == 0:
                    c = B_HL
                elif (dx + dy) % 2 == 0:
                    c = B_LT
                else:
                    c = B_MD
            
            px(a, y, x, c)

calyx(a, 15, 20, w=5)
stem(a, 15, 21, 31)
leaf(a, 14, 26, -1, 4)
leaf(a, 16, 28, 1, 4)

save(a, "hydrangea")


# ===== 9. BELLS OF IRELAND =====
# Already drawn well in previous step, just reuse that style
a = np.zeros((T, T, 4), dtype=np.uint8)

B_HL1 = (175, 225, 85)
B_HL2 = (155, 210, 65)
B_LT = (130, 190, 40)
B_MD = (105, 165, 20)
B_DK = (75, 125, 12)
B_DP = (50, 90, 5)
B_EDGE = (35, 65, 3)

WHITE_IN = (250, 245, 220)
YELLOW_ST = (245, 210, 60)

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
            if abs_d == w:
                px(a, y, x, B_EDGE)
            elif abs_d == w - 1:
                px(a, y, x, B_DP)
            elif abs_d == 0:
                px(a, y, x, B_HL1)
            elif abs_d == 1:
                px(a, y, x, B_HL2)
            elif abs_d == 2:
                px(a, y, x, B_LT)
            else:
                px(a, y, x, B_MD)
    
    mid = (top + bot) // 2
    px(a, mid, cx, WHITE_IN)
    px(a, mid, cx + 1, YELLOW_ST)
    px(a, mid - 1, cx, YELLOW_ST)

draw_bell(a, 15, 13, 17, 5)
draw_bell(a, 15, 9, 12, 4)
draw_bell(a, 15, 5, 8, 3)
draw_bell(a, 15, 2, 4, 2)
draw_bell(a, 15, 0, 1, 1)

for y in range(1, 13):
    px(a, y, 14, G2)
    px(a, y, 15, G3)
    px(a, y, 16, G3)
    px(a, y, 17, G4)

for by, bx, s in [(4, 11, -1), (4, 19, 1),
                   (8, 10, -1), (8, 20, 1),
                   (12, 9, -1), (12, 21, 1)]:
    for dy in range(-1, 2):
        for dx in range(1, 3):
            x = bx + dx * s
            px(a, by + dy, x, B_LT if dy == 0 else B_MD)

calyx(a, 15, 18, w=5)
stem(a, 15, 19, 31)
leaf(a, 14, 25, -1, 4)
leaf(a, 16, 28, 1, 3)

save(a, "bells_of_ireland")


# ===== 10. HYPERICUM =====
# Red berry cluster with yellow stamens
# AI ref: cluster of round red berries, yellow filaments
a = np.zeros((T, T, 4), dtype=np.uint8)

R_DK = (160, 15, 20)
R_MD = (210, 35, 30)
R_LT = (240, 70, 60)
R_HL = (255, 130, 120)
R_GLOSS = (255, 180, 175)  # glossy highlight

Y_ST = (250, 210, 40)
Y_ST_DK = (220, 175, 15)

def berry(a, cx, cy, r):
    """Round red berry with highlight."""
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            dist = dx*dx + dy*dy
            if dist <= r*r:
                x = cx + dx
                y = cy + dy
                # Color: outer dark, inner light
                edge = dist / (r * r)
                if edge > 0.8:
                    c = R_DK
                elif edge > 0.5:
                    c = R_MD
                elif edge > 0.25:
                    c = R_LT
                else:
                    c = R_HL
                px(a, y, x, c)
    
    # Glossy highlight dot (upper-left)
    hl_x = cx - r // 2
    hl_y = cy - r // 2
    px(a, hl_y, hl_x, R_GLOSS)
    px(a, hl_y, hl_x + 1, R_GLOSS)
    px(a, hl_y + 1, hl_x, R_GLOSS)

# 5 berries in a cluster
berry(a, 12, 9, 3)
berry(a, 19, 9, 3)
berry(a, 15, 12, 3)
berry(a, 10, 14, 3)
berry(a, 20, 14, 3)

# Yellow stamen filaments between berries
stamen_positions = [
    (15, 7, 0, -1),   # top center up
    (15, 7, 1, -1),
    (15, 7, -1, -1),
    (8, 11, -1, 0),   # left
    (22, 11, 1, 0),   # right
    (15, 16, 0, 1),   # bottom center
    (15, 16, 1, 1),
    (15, 16, -1, 1),
]

for sx, sy, dx_dir, dy_dir in stamen_positions:
    for i in range(3):
        x = sx + dx_dir * i
        y = sy + dy_dir * i
        if i == 2:
            px(a, y, x, Y_ST_DK)
        else:
            px(a, y, x, Y_ST)

calyx(a, 15, 18, w=5)
stem(a, 15, 19, 31)
leaf(a, 14, 24, -1, 3)
leaf(a, 16, 27, 1, 3)

save(a, "hypericum")


# ===== 11. LUPINE =====
# Purple cone-shaped spike
# AI ref: tall tapering spike, purple gradient dark->light
a = np.zeros((T, T, 4), dtype=np.uint8)

P_DK = (60, 20, 100)
P_MD = (95, 45, 155)
P_LT = (135, 80, 195)
P_HL = (175, 125, 225)
P_PALE = (210, 170, 245)

cx = 15

# Lupine spike: layers of small flowers, wider at bottom
spike_top = 3
spike_bot = 19

for y in range(spike_top, spike_bot + 1):
    t = (y - spike_top) / max(1, spike_bot - spike_top)
    # Width: narrow at top, wide at bottom (cone shape)
    w = int(1 + t * 5)  # 1 to 6 pixels wide per side
    
    # Color gradient: pale at top, dark at bottom
    if t < 0.2:
        c_light = P_PALE
        c_dark = P_HL
    elif t < 0.4:
        c_light = P_HL
        c_dark = P_LT
    elif t < 0.65:
        c_light = P_LT
        c_dark = P_MD
    else:
        c_light = P_MD
        c_dark = P_DK
    
    # Flower layer (rounded shape)
    for dx in range(-w - 1, w + 2):
        x = cx + dx
        abs_d = abs(dx)
        if abs_d > w + 1:
            continue
        if abs_d == w + 1:
            px(a, y, x, c_dark)
        elif abs_d == w:
            px(a, y, x, c_dark if (dx + y) % 3 == 0 else c_light)
        elif abs_d <= 1:
            px(a, y, x, c_light)
        else:
            px(a, y, x, c_light if (dx + y) % 2 == 0 else c_dark)
    
    # Side petal extensions (every other row)
    if y % 2 == 0:
        px(a, y, cx - w - 2, c_dark)
        px(a, y, cx + w + 2, c_dark)

calyx(a, 15, 20, w=4)
stem(a, 15, 21, 31)
leaf(a, 13, 26, -1, 4)
leaf(a, 17, 28, 1, 4)

save(a, "lupine")


# ===== 12. WINTERSWEET =====
# Cluster of waxy yellow flowers with red centers
# AI ref: 3-5 yellow cup flowers, red/purple center, green leaves
a = np.zeros((T, T, 4), dtype=np.uint8)

Y_DK = (195, 145, 10)
Y_MD = (225, 175, 30)
Y_LT = (250, 210, 55)
Y_HL = (255, 235, 120)

R_CTR = (155, 55, 75)
RC_DK = (110, 35, 55)

def wintersweet_flower(a, fx, fy, size=3):
    """Cup-shaped wintersweet flower: 6 petals + red center."""
    # Petals in radial pattern
    n_petals = 6
    for i in range(n_petals):
        angle = i * 60 * math.pi / 180
        for r in range(1, size + 1):
            x = fx + int(round(r * math.cos(angle)))
            y = fy + int(round(r * math.sin(angle)))
            t = r / size
            if t < 0.5:
                c = Y_LT
            elif t < 0.8:
                c = Y_MD
            else:
                c = Y_DK
            px(a, y, x, c)
    
    # Fill center area
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx*dx + dy*dy <= 2:
                px(a, fy + dy, fx + dx, Y_HL)
    
    # Red center
    px(a, fy, fx, R_CTR)
    px(a, fy, fx + 1, RC_DK)
    px(a, fy + 1, fx, RC_DK)

# 4-5 flowers in cluster
wintersweet_flower(a, 12, 6, 3)    # top left
wintersweet_flower(a, 20, 8, 3)    # top right
wintersweet_flower(a, 9, 14, 3)    # mid left
wintersweet_flower(a, 22, 16, 3)   # mid right
wintersweet_flower(a, 15, 11, 3)   # center

calyx(a, 15, 19, w=5)
stem(a, 15, 20, 31)
leaf(a, 13, 25, -1, 4)
leaf(a, 17, 26, 1, 3)
leaf(a, 13, 28, -1, 3)
leaf(a, 17, 29, 1, 2)

save(a, "wintersweet")


print("\nAll 12 flowers drawn!")
