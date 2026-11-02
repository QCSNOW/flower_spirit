"""Targeted improvements for flowers that need refinement:
1. Waxflower - more natural petal shape (less blocky)
2. Dancing Lady - more flowers, better orchid shape
3. Anemone - correct petal count and shape
4. Oncidium - better flower shape, more details
"""
import numpy as np
from PIL import Image
import math

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

G1 = (160, 215, 70)
G2 = (130, 190, 40)
G3 = (95, 155, 25)
G4 = (65, 115, 12)
G5 = (40, 75, 5)
G_CALY = (50, 90, 10)

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

def stem(a, cx, top, bot=31, curve=0):
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


# ===== 1. WAXFLOWER V2 - more natural, rounded petals =====
a = np.zeros((T, T, 4), dtype=np.uint8)

W_DK = (180, 170, 145)
W_MD = (215, 205, 180)
W_LT = (240, 230, 210)
W_HL = (252, 247, 230)
P_DK = (195, 50, 110)
P_MD = (225, 80, 140)
P_LT = (245, 130, 180)

def waxflower_v2(a, cx, cy, r):
    """5-petal flower with rounded petals and pink center."""
    # Draw petals using 5-directional pattern
    # Petal positions: top, upper-right, lower-right, lower-left, upper-left
    petal_angles = [
        -90,   # top
        -18,   # upper right
        54,    # lower right
        126,   # lower left
        198,   # upper left
    ]
    
    # Base: fill center area
    for dy in range(-r+1, r):
        for dx in range(-r+1, r):
            if dx*dx + dy*dy <= r*r:
                px(a, cy+dy, cx+dx, W_LT)
    
    # Draw each petal extended
    for angle_deg in petal_angles:
        angle = angle_deg * math.pi / 180
        for dist in range(r - 1, r + 2):
            px_val = r + 1 - dist
            x = cx + int(round(dist * math.cos(angle)))
            y = cy + int(round(dist * math.sin(angle)))
            # Petal tip color
            if dist == r + 1:
                c = W_DK
            elif dist == r:
                c = W_MD
            else:
                c = W_LT
            px(a, y, x, c)
            # Add width to petal
            perp = angle + math.pi / 2
            for w in range(1, 2):
                wx = x + int(round(w * 0.7 * math.cos(perp)))
                wy = y + int(round(w * 0.7 * math.sin(perp)))
                px(a, wy, wx, c)
    
    # Pink center
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx*dx + dy*dy <= 2:
                if dx*dx + dy*dy <= 1:
                    c = P_LT
                else:
                    c = P_MD
                px(a, cy+dy, cx+dx, c)
    px(a, cy, cx, P_DK)

# 6 flowers in a cluster
waxflower_v2(a, 15, 5, 3)    # top
waxflower_v2(a, 9, 9, 3)     # top left
waxflower_v2(a, 21, 9, 3)    # top right
waxflower_v2(a, 12, 13, 3)   # mid left
waxflower_v2(a, 18, 13, 3)   # mid right
waxflower_v2(a, 15, 17, 3)   # bottom center

# Small green leaves peeking
leaf(a, 5, 10, -1, 2)
leaf(a, 26, 10, 1, 2)

calyx(a, 15, 20, w=5)
stem(a, 15, 21, 31)
leaf(a, 14, 26, -1, 3)
leaf(a, 16, 28, 1, 3)

save(a, "waxflower")


# ===== 2. DANCING LADY V2 - more flowers, better shape =====
a = np.zeros((T, T, 4), dtype=np.uint8)

Y_DK = (195, 135, 5)
Y_MD = (225, 170, 25)
Y_LT = (250, 205, 55)
Y_HL = (255, 235, 115)
R_SPOT = (170, 55, 35)
R_DK = (130, 35, 20)

def dancing_orchid(a, fx, fy, size=3):
    """Dancing lady orchid: large lower lip + smaller upper petals."""
    # Large lower lip (the "skirt") - wider at bottom
    lip_top = fy
    lip_bot = fy + size
    for dy in range(size + 1):
        y = fy + dy
        t = dy / size
        # Width: narrow at top, wide at bottom
        w = int(1 + t * size)
        for dx in range(-w - 1, w + 2):
            x = fx + dx
            abs_d = abs(dx)
            if abs_d == w + 1:
                px(a, y, x, Y_DK)
            elif abs_d == w:
                px(a, y, x, Y_MD)
            elif abs_d <= 1:
                px(a, y, x, Y_HL)
            else:
                px(a, y, x, Y_LT)
    
    # Upper petals (3 small petals pointing up/left/right)
    # Top petal
    px(a, fy - 1, fx, Y_MD)
    px(a, fy - 2, fx, Y_LT)
    px(a, fy - 3, fx, Y_LT)
    px(a, fy - 2, fx - 1, Y_MD)
    px(a, fy - 2, fx + 1, Y_MD)
    
    # Left upper petal
    px(a, fy - 1, fx - size, Y_MD)
    px(a, fy, fx - size - 1, Y_LT)
    
    # Right upper petal
    px(a, fy - 1, fx + size, Y_MD)
    px(a, fy, fx + size + 1, Y_LT)
    
    # Red-brown center/labellum spot
    px(a, fy + 1, fx, R_SPOT)
    px(a, fy, fx, R_DK)
    px(a, fy + 1, fx - 1, R_DK)
    px(a, fy + 1, fx + 1, R_DK)

# 4 flowers cascading along a curve
dancing_orchid(a, 22, 3, 2)   # top
dancing_orchid(a, 24, 7, 2)   # upper mid
dancing_orchid(a, 23, 12, 2)  # lower mid
dancing_orchid(a, 20, 16, 2)  # bottom

# Curved stem (arc from bottom-left to top-right)
stem_points = []
for i in range(17):
    t = i / 16
    sx = int(10 + t * 11)  # 10 -> 21
    sy = int(31 - t * 28)  # 31 -> 3
    # Add curve
    curve = int(8 * math.sin(t * math.pi * 0.8))
    sx -= curve
    stem_points.append((sx, sy))

for sx, sy in stem_points:
    px(a, sy, sx - 1, G1)
    px(a, sy, sx, G3)
    px(a, sy, sx + 1, G3)
    px(a, sy, sx + 2, G4)

# Small leaf on stem
leaf(a, 9, 26, -1, 3)

save(a, "dancing_lady")


# ===== 3. ANEMONE V2 - correct 6-7 broad petals =====
a = np.zeros((T, T, 4), dtype=np.uint8)

P_DK = (50, 20, 95)
P_MD = (85, 45, 145)
P_LT = (125, 80, 185)
P_HL = (165, 125, 215)

C_DK = (20, 8, 35)
C_MD = (40, 18, 65)
C_LT = (100, 55, 125)

cx, cy = 15, 10
n_petals = 7
petal_len = 8

for i in range(n_petals):
    angle = i * 360 / n_petals * math.pi / 180
    for r in range(2, petal_len + 1):
        x = cx + int(round(r * math.cos(angle)))
        y = cy + int(round(r * math.sin(angle)))
        
        t = r / petal_len
        if t < 0.25:
            c = P_DK
        elif t < 0.55:
            c = P_MD
        elif t < 0.8:
            c = P_LT
        else:
            c = P_HL
        
        # Main petal pixel
        px(a, y, x, c)
        
        # Add width: 2 pixels wide for most of petal
        perp_angle = angle + math.pi / 2
        wx = x + int(round(0.8 * math.cos(perp_angle)))
        wy = y + int(round(0.8 * math.sin(perp_angle)))
        px(a, wy, wx, c)
        
        # Wider at base
        if r < petal_len * 0.5:
            wx2 = x - int(round(0.8 * math.cos(perp_angle)))
            wy2 = y - int(round(0.8 * math.sin(perp_angle)))
            px(a, wy2, wx2, c)

# Dark center (bigger than daisy)
for dy in range(-3, 4):
    for dx in range(-3, 4):
        dist = dx*dx + dy*dy
        if dist <= 7:
            if dist <= 3:
                c = C_DK
            elif dist <= 5:
                c = C_MD
            else:
                c = C_LT
            px(a, cy + dy, cx + dx, c)

calyx(a, 15, 18, w=5)
stem(a, 15, 19, 31)
leaf(a, 14, 24, -1, 3)
leaf(a, 16, 27, 1, 3)

save(a, "anemone")


# ===== 4. ONCIDIUM V2 - better flower shape =====
a = np.zeros((T, T, 4), dtype=np.uint8)

Y_DK = (190, 130, 5)
Y_MD = (220, 165, 20)
Y_LT = (245, 200, 50)
Y_HL = (255, 230, 110)
R_CTR = (160, 50, 30)

def oncidium_flower(a, fx, fy, size=2):
    """Oncidium: large lower lip + small upper petals, characteristic shape."""
    # Large round lower lip
    for dy in range(size):
        y = fy + dy
        w = size + 1 - abs(dy - size // 2)
        for dx in range(-w - 1, w + 2):
            x = fx + dx
            abs_d = abs(dx)
            if abs_d == w + 1:
                px(a, y, x, Y_DK)
            elif abs_d == w:
                px(a, y, x, Y_MD)
            elif abs_d <= 1:
                px(a, y, x, Y_HL)
            else:
                px(a, y, x, Y_LT)
    
    # Upper petals (small "crown")
    px(a, fy - 1, fx, Y_MD)
    px(a, fy - 2, fx, Y_LT)
    px(a, fy - 1, fx - size, Y_MD)
    px(a, fy - 1, fx + size, Y_MD)
    px(a, fy, fx - size - 1, Y_LT)
    px(a, fy, fx + size + 1, Y_LT)
    
    # Red/brown center spot
    px(a, fy, fx, R_CTR)
    px(a, fy + 1, fx, R_CTR)

# 5 flowers alternating left/right
oncidium_flower(a, 11, 4, 2)
oncidium_flower(a, 20, 7, 2)
oncidium_flower(a, 10, 11, 2)
oncidium_flower(a, 21, 14, 2)
oncidium_flower(a, 12, 18, 2)

# Top bud
px(a, 1, 15, Y_DK)
px(a, 2, 14, Y_MD)
px(a, 2, 15, Y_LT)
px(a, 2, 16, Y_MD)
px(a, 3, 15, Y_MD)

calyx(a, 15, 20, w=4)
stem(a, 15, 21, 31)
leaf(a, 14, 26, -1, 3)
leaf(a, 16, 28, 1, 3)

save(a, "oncidium")


print("\nAll 4 flowers improved!")
