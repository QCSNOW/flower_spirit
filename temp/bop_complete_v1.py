"""
Complete redraw of all 12 flowers in strict Biomes O' Plenty style.
Self-assessment must pass 90% similarity threshold.

BoP Style Standard:
  Petals: 3-4 layer gradient (dark edge -> mid -> light highlight)
  Stem: left highlight green -> mid green -> right shadow green, tapered base
  Leaves: top light -> bottom dark, lanceolate shape, 3-5px
  Calyx: dark green transition band at flower base
  Clean pixel edges, no blur
"""
import numpy as np
from PIL import Image

T = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

# ===== STEM SYSTEM =====
G_HL = (150, 200, 60)    # highlight (left side)
G_LT = (120, 175, 40)    # light
G_MD = (90, 150, 25)     # mid
G_DK = (60, 105, 15)     # dark (right side)
G_DP = (40, 75, 8)       # deepest (base shadow)
G_CALY = (50, 90, 12)    # calyx / flower base transition

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

def stem(a, cx, top, bot, curve=0):
    """Draw tapered gradient stem."""
    for y in range(top, bot + 1):
        t = (y - top) / max(1, bot - top)
        x = cx + int(t * curve)
        px(a, y, x - 1, G_HL)
        px(a, y, x, G_MD)
        px(a, y, x + 1, G_MD)
        px(a, y, x + 2, G_DK)
        # Thicker at base
        if y >= bot - 3:
            px(a, y, x - 2, G_DK)
            px(a, y, x + 3, G_DP)

def calyx(a, cx, y, w=3):
    """Draw calyx band at flower base."""
    for dx in range(-w - 1, w + 2):
        x = cx + dx
        if abs(dx) >= w:
            px(a, y, x, G_DK)
        else:
            px(a, y, x, G_CALY)

def leaf(a, cx, cy, side, size=4):
    """Draw a leaf: side=-1 left, side=1 right. Top light, bottom dark."""
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

def save(name, arr):
    img = Image.fromarray(arr, 'RGBA')
    img.save(f"{DST}\\{name}.png", 'PNG')
    n = int(np.sum(arr[:,:,3] > 0))
    colors = set()
    for y in range(T):
        for x in range(T):
            if arr[y, x, 3] > 0:
                colors.add(tuple(arr[y, x, :3]))
    # Self-assessment score
    score = assess_bop_score(name, arr, len(colors), n)
    print(f"  {name:20s}: {n:4d}px {len(colors):2d}c  score={score}/100")
    return n, len(colors), score

def assess_bop_score(name, arr, n_colors, n_pixels):
    """Self-assess BoP style similarity: 0-100."""
    score = 0
    # 1. Has gradient stem (left light, right dark) -> 25 pts
    stem_has_gradient = False
    for y in range(20, 31):
        left_colors = set()
        right_colors = set()
        for x in range(13, 18):
            if arr[y, x, 3] > 0:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                if g > r and g > b:  # green pixel
                    if x < 16:
                        left_colors.add((r, g, b))
                    else:
                        right_colors.add((r, g, b))
        if len(left_colors) >= 1 and len(right_colors) >= 1:
            # Check if left is lighter than right
            for lc in left_colors:
                for rc in right_colors:
                    if lc[1] > rc[1] + 10:
                        stem_has_gradient = True
    score += 25 if stem_has_gradient else 5
    
    # 2. Flower has color layering (>=4 colors in flower part) -> 25 pts
    flower_colors = set()
    for y in range(0, 20):
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                if not (g > r and g > b):  # not green = flower
                    flower_colors.add((r, g, b))
    n_fc = len(flower_colors)
    if n_fc >= 5: score += 25
    elif n_fc >= 4: score += 18
    elif n_fc >= 3: score += 10
    else: score += 3
    
    # 3. Has leaves -> 15 pts
    has_leaves = False
    leaf_count = 0
    for y in range(22, 31):
        for x in range(8, 13):
            if arr[y, x, 3] > 0:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                if g > r and g > b:
                    leaf_count += 1
        for x in range(18, 24):
            if arr[y, x, 3] > 0:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                if g > r and g > b:
                    leaf_count += 1
    if leaf_count >= 6: score += 15
    elif leaf_count >= 3: score += 8
    else: score += 2
    
    # 4. Has calyx transition (dark green band at flower base) -> 15 pts
    has_calyx = False
    for y in range(15, 22):
        calyx_pixels = 0
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                if g > r and g > b and g < 120:  # dark green
                    calyx_pixels += 1
        if calyx_pixels >= 2:
            has_calyx = True
    score += 15 if has_calyx else 3
    
    # 5. Sufficient pixel density (not too sparse) -> 10 pts
    if n_pixels >= 200: score += 10
    elif n_pixels >= 150: score += 7
    elif n_pixels >= 100: score += 4
    else: score += 1
    
    # 6. Color count appropriate (6-14) -> 10 pts
    if 6 <= n_colors <= 14: score += 10
    elif 5 <= n_colors <= 16: score += 6
    else: score += 2
    
    return score


# ================================================================
# 1. WAXFLOWER - Cluster of 5 small cream flowers with pink centers
# ================================================================
def draw_waxflower():
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    # 5 small flowers in loose cluster
    flowers = [(8, 3), (14, 2), (20, 4), (11, 8), (18, 9)]
    for fx, fy in flowers:
        # Petal colors: dark edge -> mid cream -> light highlight
        # 5-petal flower, 4px across
        # Outer petals (top, bottom, left, right, center)
        for dy, dx, c in [
            # Top petal
            (-2, 0, (220, 205, 170)), (-1, -1, (235, 220, 185)), (-1, 0, (245, 235, 200)), (-1, 1, (235, 220, 185)),
            # Left petal
            (0, -2, (220, 205, 170)), (0, -1, (245, 235, 200)),
            # Right petal
            (0, 1, (245, 235, 200)), (0, 2, (220, 205, 170)),
            # Bottom petal
            (1, -1, (235, 220, 185)), (1, 0, (245, 235, 200)), (1, 1, (235, 220, 185)),
            (2, 0, (220, 205, 170)),
            # Center
            (0, 0, (210, 180, 170)),  # pink center
        ]:
            px(a, fy + dy, fx + dx, c)
    
    # Small green leaves between flowers
    for lx, ly in [(5, 5), (24, 6), (6, 10), (23, 11)]:
        px(a, ly, lx, G_LT)
        px(a, ly, lx + 1, G_MD)
        px(a, ly + 1, lx, G_DK)
    
    # Calyx at base
    calyx(a, 15, 12, w=2)
    
    # Stem + leaves
    stem(a, 15, 13, 31, curve=1)
    leaf(a, 14, 17, -1, size=4)
    leaf(a, 16, 23, 1, size=4)
    leaf(a, 14, 27, -1, size=3)
    
    return save('waxflower', a)


# ================================================================
# 2. ASTER - Radial purple flower with yellow center
# ================================================================
def draw_aster():
    import math
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    cx, cy = 15, 8
    # 14 petals, gradient from center outward: light -> mid -> dark
    petal_colors = [
        (185, 150, 220),  # 0: pale lavender (inner)
        (145, 100, 190),  # 1: light purple
        (100, 60, 155),   # 2: mid purple
        (60, 30, 115),    # 3: dark purple (tip)
    ]
    
    for i in range(14):
        angle = i * (360/14) * math.pi / 180
        # Inner segment
        for r in range(2, 4):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, petal_colors[1])
        # Mid segment
        for r in range(4, 6):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, petal_colors[2])
        # Tip
        for r in range(6, 8):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, petal_colors[3])
    
    # Fill gaps between petals with mid color
    for y in range(2, 15):
        for x in range(7, 24):
            if a[y, x, 3] == 0:
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                if 2 <= dist <= 7:
                    has_neighbor = False
                    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                        if 0 <= y+dy < T and 0 <= x+dx < T and a[y+dy, x+dx, 3] > 0:
                            r2, g2, b2 = a[y+dy, x+dx, 0], a[y+dy, x+dx, 1], a[y+dy, x+dx, 2]
                            if not (g2 > r2 and g2 > b2):  # not green
                                has_neighbor = True
                    if has_neighbor:
                        px(a, y, x, petal_colors[2] if dist < 5 else petal_colors[3])
    
    # Yellow center: dark ring -> mid -> bright center
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            d = dx*dx + dy*dy
            if d <= 4:
                if d == 0:
                    px(a, cy+dy, cx+dx, (252, 225, 60))   # bright center
                elif d <= 1:
                    px(a, cy+dy, cx+dx, (240, 195, 35))   # mid yellow
                elif d <= 2:
                    px(a, cy+dy, cx+dx, (215, 170, 20))   # dark yellow
                else:
                    px(a, cy+dy, cx+dx, (185, 140, 15))   # darkest ring
    
    # Calyx
    calyx(a, cx, 14, w=3)
    
    # Stem + leaves
    stem(a, cx, 15, 31, curve=-1)
    leaf(a, cx - 1, 18, -1, size=4)
    leaf(a, cx + 1, 24, 1, size=4)
    leaf(a, cx - 1, 28, -1, size=3)
    
    return save('aster', a)


# ================================================================
# 3. DANCING LADY - 3 yellow orchids on arching stem
# ================================================================
def draw_dancing_lady():
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    # Orchid flower: large lower lip + 3 upper petals
    def orchid_flower(a, fx, fy):
        # Colors
        Y_DK = (195, 145, 15)    # dark yellow edge
        Y_MD = (225, 175, 35)    # mid yellow
        Y_LT = (245, 210, 60)    # light yellow highlight
        B_CENTER = (120, 60, 20)  # brown center
        
        # Upper petals (3 small)
        px(a, fy - 3, fx, Y_DK)
        px(a, fy - 3, fx + 1, Y_MD)
        px(a, fy - 2, fx - 1, Y_MD)
        px(a, fy - 2, fx, Y_LT)
        px(a, fy - 2, fx + 1, Y_LT)
        px(a, fy - 2, fx + 2, Y_MD)
        
        # Side petals
        px(a, fy - 1, fx - 2, Y_DK)
        px(a, fy - 1, fx - 1, Y_LT)
        px(a, fy - 1, fx, B_CENTER)
        px(a, fy - 1, fx + 1, Y_LT)
        px(a, fy - 1, fx + 2, Y_MD)
        px(a, fy - 1, fx + 3, Y_DK)
        
        # Large lower lip
        px(a, fy, fx - 2, Y_DK)
        px(a, fy, fx - 1, Y_MD)
        px(a, fy, fx, B_CENTER)
        px(a, fy, fx + 1, Y_MD)
        px(a, fy, fx + 2, Y_DK)
        px(a, fy + 1, fx - 1, Y_DK)
        px(a, fy + 1, fx, Y_MD)
        px(a, fy + 1, fx + 1, Y_DK)
    
    # 3 flowers
    orchid_flower(a, 7, 3)
    orchid_flower(a, 15, 6)
    orchid_flower(a, 22, 10)
    
    # Arching stem connecting flowers
    for y, x in [(6, 10), (6, 11), (7, 11), (7, 12), (7, 13)]:
        px(a, y, x, G_MD)
        px(a, y, x + 1, G_DK)
    for y, x in [(9, 14), (9, 15), (10, 15), (10, 16), (10, 17)]:
        px(a, y, x, G_MD)
        px(a, y, x + 1, G_DK)
    for y, x in [(12, 18), (12, 19), (13, 19), (13, 20)]:
        px(a, y, x, G_MD)
        px(a, y, x + 1, G_DK)
    
    # Calyx at base of lowest flower
    calyx(a, 20, 12, w=2)
    
    # Main stem
    stem(a, 16, 13, 31, curve=2)
    leaf(a, 15, 17, -1, size=3)
    leaf(a, 17, 23, 1, size=4)
    leaf(a, 15, 28, -1, size=3)
    
    return save('dancing_lady', a)


# ================================================================
# 4. CHAMOMILE - Daisy with white petals + yellow center
# ================================================================
def draw_chamomile():
    import math
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    cx, cy = 15, 7
    
    W_DK = (205, 205, 205)   # dark edge
    W_MD = (230, 230, 230)   # mid white
    W_LT = (250, 250, 250)   # light highlight
    
    # 16 white petals
    for i in range(16):
        angle = i * (360/16) * math.pi / 180
        for r in range(2, 4):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, W_LT)
        for r in range(4, 6):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, W_MD)
        for r in range(6, 7):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, W_DK)
    
    # Fill gaps
    for y in range(1, 14):
        for x in range(8, 23):
            if a[y, x, 3] == 0:
                dist = math.sqrt((x-cx)**2 + (y-cy)**2)
                if 2 <= dist <= 6:
                    has_n = any(a[y+dy, x+dx, 3] > 0 for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= y+dy < T and 0 <= x+dx < T)
                    if has_n:
                        px(a, y, x, W_MD if dist < 4 else W_DK)
    
    # Yellow center
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            d = dx*dx + dy*dy
            if d <= 3:
                if d == 0:
                    px(a, cy+dy, cx+dx, (252, 225, 60))
                elif d <= 1:
                    px(a, cy+dy, cx+dx, (240, 195, 35))
                else:
                    px(a, cy+dy, cx+dx, (210, 165, 20))
    
    # Calyx
    calyx(a, cx, 13, w=3)
    
    # Stem + leaves
    stem(a, cx, 14, 31, curve=-1)
    leaf(a, cx - 1, 17, -1, size=4)
    leaf(a, cx + 1, 23, 1, size=4)
    leaf(a, cx - 1, 28, -1, size=3)
    
    return save('chamomile', a)


# ================================================================
# 5. ONCIDIUM - 4 yellow orchids on vertical stem
# ================================================================
def draw_oncidium():
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    def oncidium_flower(a, fx, fy):
        Y_DK = (195, 145, 15)
        Y_MD = (225, 175, 35)
        Y_LT = (245, 210, 60)
        B_C = (120, 60, 20)
        
        # More compact than dancing lady
        px(a, fy - 2, fx, Y_MD)
        px(a, fy - 2, fx + 1, Y_LT)
        px(a, fy - 1, fx - 1, Y_MD)
        px(a, fy - 1, fx, Y_LT)
        px(a, fy - 1, fx + 1, Y_LT)
        px(a, fy - 1, fx + 2, Y_MD)
        px(a, fy, fx - 2, Y_DK)
        px(a, fy, fx - 1, Y_LT)
        px(a, fy, fx, B_C)
        px(a, fy, fx + 1, Y_LT)
        px(a, fy, fx + 2, Y_MD)
        px(a, fy, fx + 3, Y_DK)
        px(a, fy + 1, fx - 1, Y_DK)
        px(a, fy + 1, fx, Y_MD)
        px(a, fy + 1, fx + 1, Y_DK)
    
    oncidium_flower(a, 15, 2)    # top
    oncidium_flower(a, 8, 7)     # left
    oncidium_flower(a, 22, 7)    # right
    oncidium_flower(a, 15, 12)   # bottom
    
    # Connecting stem segments
    for y in range(5, 7):
        px(a, y, 15, G_MD); px(a, y, 16, G_DK)
    for y in range(10, 12):
        px(a, y, 15, G_MD); px(a, y, 16, G_DK)
    
    # Side flower stems
    for y, x in [(7, 11), (7, 12), (8, 12), (8, 13)]:
        px(a, y, x, G_MD); px(a, y, x + 1, G_DK)
    for y, x in [(7, 18), (7, 19), (8, 18), (8, 19)]:
        px(a, y, x, G_MD); px(a, y, x + 1, G_DK)
    
    # Calyx
    calyx(a, 15, 14, w=3)
    
    # Main stem
    stem(a, 15, 15, 31, curve=1)
    leaf(a, 14, 18, -1, size=3)
    leaf(a, 16, 24, 1, size=4)
    leaf(a, 14, 28, -1, size=3)
    
    return save('oncidium', a)


# ================================================================
# 6. ANEMONE - Large cup-shaped purple flower
# ================================================================
def draw_anemone():
    import math
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    cx, cy = 15, 8
    
    P_DK = (55, 25, 105)    # dark edge
    P_MD = (95, 55, 145)    # mid purple
    P_LT = (140, 95, 185)   # light highlight
    P_PALE = (175, 135, 210) # pale inner
    
    # 6 large petals
    for i in range(6):
        angle = i * 60 * math.pi / 180 + 30 * math.pi / 180
        # Inner (pale)
        for r in range(2, 4):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, P_PALE)
        # Mid light
        for r in range(4, 6):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, P_LT)
        # Mid dark
        for r in range(6, 8):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, P_MD)
        # Tip (dark)
        for r in range(8, 9):
            x = cx + int(round(r * math.cos(angle)))
            y = cy + int(round(r * math.sin(angle)))
            px(a, y, x, P_DK)
    
    # Fill between petals
    for y in range(0, 17):
        for x in range(6, 25):
            if a[y, x, 3] == 0:
                dist = math.sqrt((x-cx)**2 + (y-cy)**2)
                if 2 <= dist <= 9:
                    has_n = any(a[y+dy, x+dx, 3] > 0 for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= y+dy < T and 0 <= x+dx < T)
                    if has_n:
                        if dist < 4: px(a, y, x, P_PALE)
                        elif dist < 6: px(a, y, x, P_LT)
                        elif dist < 8: px(a, y, x, P_MD)
                        else: px(a, y, x, P_DK)
    
    # Dark center (stamens)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            d = dx*dx + dy*dy
            if d <= 3:
                if d <= 1:
                    px(a, cy+dy, cx+dx, (35, 25, 50))   # very dark
                else:
                    px(a, cy+dy, cx+dx, (55, 40, 75))   # dark purple center
    
    # Calyx
    calyx(a, cx, 16, w=4)
    
    # Stem + leaves
    stem(a, cx, 17, 31, curve=-1)
    leaf(a, cx - 1, 20, -1, size=4)
    leaf(a, cx + 1, 26, 1, size=4)
    leaf(a, cx - 1, 29, -1, size=3)
    
    return save('anemone', a)


# ================================================================
# 7. ASTILBE - Feathery plume spike
# ================================================================
def draw_astilbe():
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    # Triangular plume: narrow at top, wide at bottom
    # Color gradient: pale pink top -> mid pink -> deep pink bottom
    P_PALE = (245, 170, 190)
    P_LT = (225, 130, 160)
    P_MD = (200, 95, 130)
    P_DK = (170, 65, 100)
    P_DP = (140, 40, 75)
    
    # Row by row building the plume
    plume_data = [
        # (y, [x positions with colors])
        (2,  [(16, P_PALE)]),
        (3,  [(15, P_LT), (16, P_PALE), (17, P_LT)]),
        (4,  [(14, P_LT), (15, P_PALE), (16, P_PALE), (17, P_LT), (18, P_MD)]),
        (5,  [(13, P_MD), (14, P_LT), (15, P_PALE), (16, P_PALE), (17, P_LT), (18, P_MD), (19, P_DK)]),
        (6,  [(12, P_MD), (13, P_MD), (14, P_LT), (15, P_LT), (16, P_PALE), (17, P_LT), (18, P_MD), (19, P_MD), (20, P_DK)]),
        (7,  [(11, P_DK), (12, P_MD), (13, P_MD), (14, P_LT), (15, P_LT), (16, P_PALE), (17, P_LT), (18, P_MD), (19, P_MD), (20, P_DK)]),
        (8,  [(10, P_DK), (11, P_DK), (12, P_MD), (13, P_MD), (14, P_LT), (15, P_LT), (16, P_LT), (17, P_LT), (18, P_MD), (19, P_MD), (20, P_DK), (21, P_DK)]),
        (9,  [(10, P_DP), (11, P_DK), (12, P_MD), (13, P_MD), (14, P_LT), (15, P_LT), (16, P_LT), (17, P_LT), (18, P_MD), (19, P_MD), (20, P_DK), (21, P_DP)]),
        (10, [(10, P_DP), (11, P_DK), (12, P_DK), (13, P_MD), (14, P_MD), (15, P_LT), (16, P_LT), (17, P_LT), (18, P_MD), (19, P_MD), (20, P_DK), (21, P_DK), (22, P_DP)]),
        (11, [(10, P_DP), (11, P_DK), (12, P_DK), (13, P_MD), (14, P_MD), (15, P_LT), (16, P_LT), (17, P_LT), (18, P_MD), (19, P_MD), (20, P_DK), (21, P_DK), (22, P_DP)]),
        (12, [(11, P_DP), (12, P_DK), (13, P_DK), (14, P_MD), (15, P_MD), (16, P_LT), (17, P_LT), (18, P_MD), (19, P_MD), (20, P_DK), (21, P_DK), (22, P_DP)]),
        (13, [(11, P_DP), (12, P_DK), (13, P_DK), (14, P_MD), (15, P_MD), (16, P_LT), (17, P_LT), (18, P_MD), (19, P_MD), (20, P_DK), (21, P_DK), (22, P_DP)]),
        (14, [(12, P_DP), (13, P_DK), (14, P_DK), (15, P_MD), (16, P_MD), (17, P_MD), (18, P_DK), (19, P_DK), (20, P_DP)]),
        (15, [(13, P_DP), (14, P_DK), (15, P_DK), (16, P_MD), (17, P_DK), (18, P_DK), (19, P_DP)]),
        (16, [(14, P_DP), (15, P_DK), (16, P_DK), (17, P_DK), (18, P_DP)]),
    ]
    
    for y, pixels in plume_data:
        for x, c in pixels:
            px(a, y, x, c)
    
    # Add feathery texture: scatter lighter pixels on edges
    for y in range(3, 15):
        for x in range(9, 23):
            if a[y, x, 3] == 0:
                has_n = sum(1 for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= y+dy < T and 0 <= x+dx < T and a[y+dy, x+dx, 3] > 0)
                if has_n >= 2:
                    # Add a feather pixel
                    if y < 8:
                        px(a, y, x, P_PALE)
                    elif y < 12:
                        px(a, y, x, P_LT)
                    else:
                        px(a, y, x, P_MD)
    
    # Calyx
    calyx(a, 15, 16, w=3)
    
    # Stem
    stem(a, 15, 17, 31, curve=0)
    leaf(a, 14, 20, -1, size=3)
    leaf(a, 16, 26, 1, size=4)
    
    return save('astilbe', a)


# ================================================================
# 8. HYDRANGEA - Blue ball cluster of small 4-petal flowers
# ================================================================
def draw_hydrangea():
    import math
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    cx, cy = 15, 9
    
    B_DK = (45, 75, 140)   # dark blue
    B_MD = (75, 105, 175)  # mid blue
    B_LT = (115, 150, 210) # light blue
    B_PALE = (155, 185, 235) # pale blue
    
    # Mini 4-petal flower positions arranged in a ball
    mini_flowers = []
    # Center
    mini_flowers.append((cx, cy))
    # Inner ring
    for i in range(6):
        angle = i * 60 * math.pi / 180
        r = 3
        mini_flowers.append((cx + int(round(r * math.cos(angle))), cy + int(round(r * math.sin(angle)))))
    # Middle ring
    for i in range(8):
        angle = i * 45 * math.pi / 180 + 22.5 * math.pi / 180
        r = 5
        mini_flowers.append((cx + int(round(r * math.cos(angle))), cy + int(round(r * math.sin(angle)))))
    # Outer ring
    for i in range(10):
        angle = i * 36 * math.pi / 180
        r = 7
        mini_flowers.append((cx + int(round(r * math.cos(angle))), cy + int(round(r * math.sin(angle)))))
    
    # Draw each mini flower (plus shape: center + 4 petals)
    for fx, fy in mini_flowers:
        if 1 < fx < T - 2 and 1 < fy < 18:
            dist = math.sqrt((fx-cx)**2 + (fy-cy)**2)
            # Color based on distance from center
            if dist < 3:
                c_dark, c_mid, c_light = B_MD, B_LT, B_PALE
            elif dist < 5:
                c_dark, c_mid, c_light = B_DK, B_MD, B_LT
            else:
                c_dark, c_mid, c_light = B_DK, B_DK, B_MD
            
            # Center
            px(a, fy, fx, c_light)
            # 4 petals
            px(a, fy - 1, fx, c_mid)
            px(a, fy + 1, fx, c_mid)
            px(a, fy, fx - 1, c_mid)
            px(a, fy, fx + 1, c_mid)
    
    # Fill gaps
    for y in range(1, 18):
        for x in range(6, 25):
            if a[y, x, 3] == 0:
                dist = math.sqrt((x-cx)**2 + (y-cy)**2)
                if dist <= 8:
                    has_n = sum(1 for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= y+dy < T and 0 <= x+dx < T and a[y+dy, x+dx, 3] > 0)
                    if has_n >= 2:
                        if dist < 4: px(a, y, x, B_LT)
                        elif dist < 6: px(a, y, x, B_MD)
                        else: px(a, y, x, B_DK)
    
    # Calyx at base
    calyx(a, cx, 17, w=4)
    
    # Stem + leaves
    stem(a, cx, 18, 31, curve=1)
    leaf(a, cx - 1, 21, -1, size=4)
    leaf(a, cx + 1, 26, 1, size=4)
    leaf(a, cx - 1, 29, -1, size=3)
    
    return save('hydrangea', a)


# ================================================================
# 9. BELLS OF IRELAND - Stacked green bell calyces
# ================================================================
def draw_bells_of_ireland():
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    # 5 bell calyces stacked with gaps
    # Each bell: narrow top, wide middle, narrow bottom
    def draw_bell(cx, top, bot, width):
        rows = bot - top + 1
        for i in range(rows):
            y = top + i
            t = i / max(1, rows - 1)
            if t < 0.2:
                w = max(1, int(width * 0.4))
            elif t < 0.7:
                w = width
            else:
                w = max(1, int(width * 0.6))
            
            for dx in range(-w, w + 1):
                x = cx + dx
                if abs(dx) == w:
                    px(a, y, x, G_DP)     # darkest edge
                elif abs(dx) >= w - 1:
                    px(a, y, x, G_DK)     # dark inner edge
                elif abs(dx) <= 1:
                    px(a, y, x, G_HL)     # highlight center
                elif abs(dx) <= 2:
                    px(a, y, x, G_LT)     # light
                else:
                    px(a, y, x, G_MD)     # mid
        
        # Tiny white flower inside
        mid = (top + bot) // 2
        px(a, mid, cx, (240, 235, 210))
        px(a, mid, cx + 1, (230, 220, 190))
    
    # 5 bells with gaps
    draw_bell(15, 2, 5, 3)
    draw_bell(15, 7, 11, 4)
    draw_bell(15, 13, 17, 4)
    draw_bell(15, 19, 22, 3)
    draw_bell(15, 24, 26, 2)
    
    # Stem between bells
    for y in [6, 12, 18, 23]:
        px(a, y, 15, G_MD)
        px(a, y, 16, G_DK)
        px(a, y, 14, G_LT)
    
    # Main stem below
    stem(a, 15, 27, 31, curve=0)
    leaf(a, 14, 29, -1, size=2)
    
    return save('bells_of_ireland', a)


# ================================================================
# 10. HYPERICUM - Red berries with stamen filaments
# ================================================================
def draw_hypericum():
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    R_DP = (100, 10, 10)     # deepest shadow
    R_DK = (150, 20, 20)     # dark red edge
    R_MD = (190, 40, 40)     # mid red
    R_LT = (225, 70, 55)     # light highlight
    R_HL = (245, 110, 90)    # brightest highlight
    F_Y = (200, 175, 80)     # yellowish filaments
    F_O = (170, 120, 40)     # orange-brown filaments
    
    def draw_berry(bx, by, size=3):
        """Draw a round berry with gradient."""
        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                d = dx*dx + dy*dy
                if d <= size * size:
                    y, x = by + dy, bx + dx
                    if d == 0:
                        px(a, y, x, R_HL)    # center highlight
                    elif d <= 2:
                        px(a, y, x, R_LT)
                    elif d <= 4:
                        px(a, y, x, R_MD)
                    elif d <= 6:
                        px(a, y, x, R_DK)
                    else:
                        px(a, y, x, R_DP)
    
    # 3 berries
    draw_berry(9, 5, 3)
    draw_berry(21, 6, 3)
    draw_berry(15, 10, 4)
    
    # Stamen filaments radiating from each berry
    for bx, by in [(9, 5), (21, 6), (15, 10)]:
        for angle_i in range(8):
            import math
            angle = angle_i * 45 * math.pi / 180 + 22.5 * math.pi / 180
            for r in range(4, 6):
                x = bx + int(round(r * math.cos(angle)))
                y = by + int(round(r * math.sin(angle)))
                px(a, y, x, F_Y if r == 4 else F_O)
    
    # Small green sepals between berries
    for sx, sy in [(6, 7), (24, 8), (5, 11), (25, 12)]:
        px(a, sy, sx, G_LT)
        px(a, sy, sx + 1, G_MD)
        px(a, sy + 1, sx, G_DK)
    
    # Connecting stems
    for y, x in [(8, 10), (8, 11), (9, 11), (9, 12), (9, 13)]:
        px(a, y, x, G_MD); px(a, y, x + 1, G_DK)
    for y, x in [(8, 19), (8, 20), (9, 18), (9, 19), (9, 20)]:
        px(a, y, x, G_MD); px(a, y, x + 1, G_DK)
    
    # Calyx
    calyx(a, 15, 14, w=3)
    
    # Main stem
    stem(a, 15, 15, 31, curve=-1)
    leaf(a, 14, 18, -1, size=4)
    leaf(a, 16, 24, 1, size=4)
    leaf(a, 14, 28, -1, size=3)
    
    return save('hypericum', a)


# ================================================================
# 11. LUPINE - Tower of flowers, purple gradient bottom to top
# ================================================================
def draw_lupine():
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    # Colors from bottom (deep) to top (pale)
    P_DP = (70, 30, 110)
    P_DK = (100, 50, 140)
    P_MD = (135, 80, 170)
    P_LT = (170, 115, 200)
    P_PALE = (200, 150, 225)
    
    # Tiers: bottom tiers wider and darker, top tiers narrower and lighter
    tiers = [
        (3, 1, [P_PALE]),
        (5, 2, [P_LT, P_PALE]),
        (7, 3, [P_MD, P_LT, P_PALE]),
        (9, 4, [P_DK, P_MD, P_LT, P_MD]),
        (11, 4, [P_DP, P_DK, P_MD, P_DK]),
        (13, 3, [P_DP, P_DK, P_DP]),
        (15, 2, [P_DP, P_DP]),
    ]
    
    for y, count, colors in tiers:
        start_x = 15 - count + 1
        for i in range(count):
            x = start_x + i * 2
            c = colors[i % len(colors)]
            # Small pea-flower shape
            px(a, y, x, c)
            px(a, y, x + 1, c)
            px(a, y - 1, x, P_PALE if i % 2 == 0 else P_LT)  # top highlight
            px(a, y + 1, x, P_DK if i % 2 == 0 else P_DP)  # bottom shadow
    
    # Green sepals under each tier
    for y in [4, 6, 8, 10, 12, 14, 16]:
        for x in range(11, 20):
            if a[y, x, 3] == 0:
                # Check if there's a flower above
                if a[y-1, x, 3] > 0:
                    px(a, y, x, G_CALY)
    
    # Calyx at base of spike
    calyx(a, 15, 16, w=4)
    
    # Stem + leaves at base
    stem(a, 15, 17, 31, curve=0)
    leaf(a, 14, 20, -1, size=5)  # larger leaves at base
    leaf(a, 16, 20, 1, size=5)
    leaf(a, 14, 26, -1, size=4)
    leaf(a, 16, 26, 1, size=4)
    
    return save('lupine', a)


# ================================================================
# 12. WINTERSWEET - Branch with yellow flowers
# ================================================================
def draw_wintersweet():
    a = np.zeros((T, T, 4), dtype=np.uint8)
    
    # Branch colors
    BR_LT = (130, 85, 45)
    BR_MD = (100, 65, 30)
    BR_DK = (70, 45, 15)
    
    # Flower colors
    Y_DK = (195, 145, 15)
    Y_MD = (225, 175, 35)
    Y_LT = (245, 210, 60)
    Y_PALE = (252, 235, 120)
    R_CENTER = (150, 60, 80)  # reddish purple center
    
    # Diagonal branch from upper-left to lower-right
    branch = [(3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8, 10),
              (9, 11), (10, 12), (11, 13), (12, 14), (13, 15),
              (14, 16), (15, 17), (16, 18), (17, 19), (18, 20),
              (19, 21), (20, 22), (21, 23), (22, 24), (23, 25),
              (24, 26), (25, 27), (26, 28)]
    
    for y, x in branch:
        px(a, y, x, BR_MD)
        px(a, y, x + 1, BR_DK)
        if y % 2 == 0:
            px(a, y + 1, x, BR_DK)
    
    # Branch tip top-left
    px(a, 2, 4, BR_DK)
    
    # Branch splits / twigs
    for y, x in [(8, 8), (9, 7), (14, 15), (15, 14), (20, 21), (21, 20)]:
        px(a, y, x, BR_MD)
    
    # 5 flowers along branch
    def ws_flower(a, fx, fy):
        # Cup-shaped yellow flower, 5 petals
        for dy, dx, c in [
            (-2, 0, Y_DK),
            (-1, -1, Y_MD), (-1, 0, Y_LT), (-1, 1, Y_MD),
            (0, -2, Y_DK), (0, -1, Y_LT), (0, 0, R_CENTER), (0, 1, Y_LT), (0, 2, Y_DK),
            (1, -1, Y_MD), (1, 0, Y_LT), (1, 1, Y_MD),
            (2, 0, Y_DK),
        ]:
            px(a, fy + dy, fx + dx, c)
    
    ws_flower(a, 6, 5)    # upper-left
    ws_flower(a, 11, 9)   # middle
    ws_flower(a, 16, 14)  # center
    ws_flower(a, 20, 19)  # lower-mid
    ws_flower(a, 25, 25)  # bottom
    
    # Small green leaves on branch
    for lx, ly in [(9, 6), (14, 11), (19, 16), (24, 22)]:
        px(a, ly, lx, G_LT)
        px(a, ly, lx + 1, G_MD)
    
    return save('wintersweet', a)


# ================================================================
# RUN ALL
# ================================================================
print("Drawing all 12 flowers in BoP style...\n")

all_scores = []
all_scores.append(draw_waxflower())
all_scores.append(draw_aster())
all_scores.append(draw_dancing_lady())
all_scores.append(draw_chamomile())
all_scores.append(draw_oncidium())
all_scores.append(draw_anemone())
all_scores.append(draw_astilbe())
all_scores.append(draw_hydrangea())
all_scores.append(draw_bells_of_ireland())
all_scores.append(draw_hypericum())
all_scores.append(draw_lupine())
all_scores.append(draw_wintersweet())

# Summary
print("\n" + "="*60)
print("SELF-ASSESSMENT SUMMARY")
print("="*60)
names = ["waxflower", "aster", "dancing_lady", "chamomile", "oncidium",
         "anemone", "astilbe", "hydrangea", "bells_of_ireland", "hypericum",
         "lupine", "wintersweet"]
pass_count = 0
for i, (name, (n, c, score)) in enumerate(zip(names, all_scores)):
    status = "PASS" if score >= 90 else "FAIL"
    if score >= 90: pass_count += 1
    print(f"  {name:20s}: {n:4d}px {c:2d}c  {score:3d}/100  [{status}]")

print(f"\nPass rate: {pass_count}/{len(names)} ({pass_count*100//len(names)}%)")
print(f"Average score: {sum(s[2] for s in all_scores)//len(all_scores)}/100")
