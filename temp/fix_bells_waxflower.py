"""Fix bells_of_ireland (all green) and do final color cleanup."""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

# Green system (6 shades for BoP style)
G1 = (170, 220, 80)   # brightest highlight
G2 = (140, 195, 50)   # light
G3 = (110, 170, 30)   # mid-light
G4 = (80, 140, 20)    # mid
G5 = (55, 105, 12)    # dark
G6 = (35, 70, 5)      # darkest

# Bell flower greens (slightly different, more vibrant)
B1 = (165, 215, 75)   # bell highlight
B2 = (135, 190, 45)   # bell light
B3 = (105, 165, 25)   # bell mid
B4 = (75, 125, 15)    # bell dark
B5 = (50, 90, 8)      # bell darkest

WHITE_INNER = (248, 242, 215)
YELLOW_STAMEN = (240, 205, 55)

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

# ===== Redraw bells_of_ireland from scratch, based on AI reference =====
# Reference: 5 bell-shaped green calyxes stacked vertically, getting smaller toward top
# Small white flower inside each bell, green stem with 2 leaves at bottom
a = np.zeros((T, T, 4), dtype=np.uint8)

# Draw 5 bells stacked, from bottom (largest) to top (smallest)
# Each bell: wider at bottom, narrower at top (bell shape)
def draw_bell(a, cx, top, bot, max_w):
    rows = bot - top + 1
    for i in range(rows):
        y = top + i
        t = i / max(1, rows - 1)
        # Bell curve: narrow top -> wide middle -> slightly narrow bottom rim
        if t < 0.2:
            w = max(1, int(max_w * 0.4))
        elif t < 0.6:
            w = max_w
        else:
            w = max(1, int(max_w * 0.7))
        
        for dx in range(-w, w + 1):
            x = cx + dx
            abs_d = abs(dx)
            # 5-layer green gradient: center bright -> edges dark
            if abs_d == w:
                px(a, y, x, B5)
            elif abs_d == w - 1:
                px(a, y, x, B4)
            elif abs_d <= 1:
                px(a, y, x, B1)
            elif abs_d <= 2:
                px(a, y, x, B2)
            else:
                px(a, y, x, B3)
    
    # Inner white flower + yellow stamen
    mid_y = (top + bot) // 2
    px(a, mid_y, cx, WHITE_INNER)
    px(a, mid_y, cx + 1, YELLOW_STAMEN)
    px(a, mid_y - 1, cx, YELLOW_STAMEN)

# 5 bells: bottom largest, top smallest
draw_bell(a, 15, 13, 17, 5)   # bottom (largest)
draw_bell(a, 15, 9, 12, 4)
draw_bell(a, 15, 5, 8, 3)
draw_bell(a, 15, 2, 4, 2)
draw_bell(a, 15, 0, 1, 1)   # top (tiny)

# Connecting stem between bells
for y in range(1, 13):
    px(a, y, 14, G2)
    px(a, y, 15, G4)
    px(a, y, 16, G4)
    px(a, y, 17, G5)

# Small bracts between bells
for by, bx, s in [(4, 11, -1), (4, 19, 1),
                   (8, 10, -1), (8, 20, 1),
                   (12, 9, -1), (12, 21, 1)]:
    # tiny bract leaf
    for dy in range(-1, 2):
        for dx in range(1, 3):
            x = bx + dx * s
            px(a, by + dy, x, G3 if dy == 0 else G4)

# Calyx at base of spike
for x in range(11, 20):
    dx = abs(x - 15)
    if dx >= 3:
        px(a, 17, x, G6)
    elif dx >= 2:
        px(a, 17, x, G5)
    else:
        px(a, 17, x, G4)

# Main stem below (4px gradient)
for y in range(18, 32):
    px(a, y, 14, G1)  # highlight
    px(a, y, 15, G3)  # mid
    px(a, y, 16, G4)  # mid-dark
    px(a, y, 17, G5)  # shadow
    if y >= 28:
        px(a, y, 13, G5)
        px(a, y, 18, G6)

# Leaves at bottom
# Left leaf at y=27
for dy in range(-3, 4):
    w = 3 - abs(dy)
    for dx in range(1, w + 2):
        x = 13 - dx
        y = 27 + dy
        if dy < 0:
            px(a, y, x, G2 if dx <= 1 else G3)
        elif dy > 0:
            px(a, y, x, G5 if dx <= 1 else G4)
        else:
            px(a, y, x, G1)

# Right leaf at y=29
for dy in range(-3, 4):
    w = 3 - abs(dy)
    for dx in range(1, w + 2):
        x = 17 + dx
        y = 29 + dy
        if dy < 0:
            px(a, y, x, G2 if dx <= 1 else G3)
        elif dy > 0:
            px(a, y, x, G5 if dx <= 1 else G4)
        else:
            px(a, y, x, G1)

Image.fromarray(a, 'RGBA').save(f"{DST}\\bells_of_ireland.png", 'PNG')
n = int(np.sum(a[:,:,3] > 0))
c = len(set(tuple(a[y,x,:3]) for y in range(T) for x in range(T) if a[y,x,3] > 0))
print(f"bells_of_ireland: {n}px, {c}c")


# ===== Also fix waxflower: reduce color count =====
arr = np.array(Image.open(f"{DST}\\waxflower.png").convert('RGBA'))

# The waxflower has many colors from the AI reduction + stem rebuild
# Quantize flower (non-green) to 6 colors
flower_pixels = set()
green_pixels = set()
for y in range(T):
    for x in range(T):
        if arr[y, x, 3] == 0:
            continue
        r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
        if g > r + 10 and g > b + 10 and g > 50:
            green_pixels.add((r, g, b))
        else:
            flower_pixels.add((r, g, b))

# Reduce flower colors to 6
flower_list = sorted(flower_pixels, key=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2])
if len(flower_list) > 6:
    indices = np.linspace(0, len(flower_list)-1, 6, dtype=int)
    flower_palette = [flower_list[i] for i in indices]
else:
    flower_palette = flower_list

# Reduce green colors to 6
green_list = sorted(green_pixels, key=lambda c: c[1])  # sort by green channel
if len(green_list) > 6:
    indices = np.linspace(0, len(green_list)-1, 6, dtype=int)
    green_palette = [green_list[i] for i in indices]
else:
    green_palette = green_list

# Apply
result = arr.copy()
for y in range(T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        c = (r, g, b)
        if g > r + 10 and g > b + 10 and g > 50:
            palette = green_palette
        else:
            palette = flower_palette
        
        dists = [sum((a-b)**2 for a,b in zip(c, p)) for p in palette]
        nearest = palette[dists.index(min(dists))]
        result[y, x] = [nearest[0], nearest[1], nearest[2], 255]

Image.fromarray(result, 'RGBA').save(f"{DST}\\waxflower.png", 'PNG')
n = int(np.sum(result[:,:,3] > 0))
c = len(set(tuple(result[y,x,:3]) for y in range(T) for x in range(T) if result[y,x,3] > 0))
print(f"waxflower: {n}px, {c}c")

print("\nDone!")
