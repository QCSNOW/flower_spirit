"""Deep repair: rebuild stems and flower-stem connections for all 12 flowers.
Strategy: For each flower, find the bottom of the flower head, then draw a proper
gradient stem down to the bottom, with leaves.
"""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

G_HL = (150, 205, 65)
G_LT = (120, 180, 40)
G_MD = (90, 150, 25)
G_DK = (60, 110, 15)
G_DP = (38, 75, 8)
G_CALY = (50, 90, 12)

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

def load(name):
    return np.array(Image.open(f"{DST}\\{name}.png").convert('RGBA'))

def save(arr, name):
    Image.fromarray(arr, 'RGBA').save(f"{DST}\\{name}.png", 'PNG')

def find_flower_base(arr):
    """Find the bottom row of the flower (non-green part) and its center x."""
    flower_rows = []
    for y in range(T):
        has_flower = False
        xs = []
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
                # Flower = not predominantly green
                if not (g > r + 10 and g > b + 10):
                    has_flower = True
                    xs.append(x)
        if has_flower:
            flower_rows.append((y, xs))
    
    if not flower_rows:
        return None, None
    
    # Bottom-most flower row
    bottom_y = max(y for y, _ in flower_rows)
    bottom_xs = [xs for y, xs in flower_rows if y == bottom_y][0]
    center_x = sum(bottom_xs) // len(bottom_xs)
    
    return bottom_y, center_x

def draw_stem(arr, cx, top_y, bot_y=31, curve=0):
    """Draw a gradient stem from top_y to bot_y at column cx."""
    for y in range(top_y, bot_y + 1):
        t = (y - top_y) / max(1, bot_y - top_y)
        x_offset = int(t * curve)
        x = cx + x_offset
        
        # 4-pixel wide stem: highlight | mid | mid | shadow
        px(arr, y, x - 1, G_HL)
        px(arr, y, x, G_MD)
        px(arr, y, x + 1, G_MD)
        px(arr, y, x + 2, G_DK)
        
        # Base thickening
        if y >= bot_y - 3:
            px(arr, y, x - 2, G_DK)
            px(arr, y, x + 3, G_DP)

def draw_calyx(arr, cx, y, width=4):
    """Draw calyx band at flower base."""
    for dx in range(-width, width + 1):
        x = cx + dx
        if abs(dx) == width:
            px(arr, y, x, G_DP)
        elif abs(dx) >= width - 1:
            px(arr, y, x, G_DK)
        else:
            px(arr, y, x, G_CALY)

def draw_leaf(arr, cx, cy, side, size=4):
    """Draw a lanceolate leaf. side=-1 (left) or 1 (right)."""
    for dy in range(-size, size + 1):
        w = max(1, size - abs(dy))
        for dx in range(1, w + 2):
            x = cx + dx * side
            y = cy + dy
            if dy < 0:
                px(arr, y, x, G_LT if dx <= w // 2 + 1 else G_MD)
            elif dy > 0:
                px(arr, y, x, G_DK if dx <= w // 2 + 1 else G_MD)
            else:
                px(arr, y, x, G_HL)

def rebuild_flower(name, flower_cx=None, flower_top=None, 
                   stem_cx=None, stem_top_offset=1,
                   leaves=None, calyx_w=4, curve=0):
    """Complete stem rebuild for a flower."""
    arr = load(name)
    
    # Find flower base
    base_y, base_cx = find_flower_base(arr)
    if base_y is None:
        print(f"  {name}: no flower found, skipping")
        return
    
    if flower_cx is None:
        flower_cx = base_cx
    if stem_cx is None:
        stem_cx = base_cx
    
    # Clear old green pixels below flower (old messy stem)
    clear_top = base_y + 1
    for y in range(clear_top, T):
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
                if g > r + 5 and g > b + 5:
                    arr[y, x, 3] = 0
    
    # Also clear green pixels within flower area that are artifacts
    # (keep only non-green flower pixels above base_y)
    
    # Draw calyx at flower base
    calyx_y = base_y + stem_top_offset
    draw_calyx(arr, stem_cx, calyx_y, width=calyx_w)
    
    # Draw stem from calyx to bottom
    draw_stem(arr, stem_cx, calyx_y + 1, T - 1, curve=curve)
    
    # Draw leaves
    if leaves:
        for ly, side, size in leaves:
            draw_leaf(arr, stem_cx, ly, side, size)
    
    save(arr, name)
    
    n_px = int(np.sum(arr[:,:,3] > 0))
    n_colors = len(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0))
    print(f"  {name:20s}: {n_px:4d}px, {n_colors:2d}c")


# ===== Rebuild all 12 flowers =====
print("Rebuilding stems for all 12 flowers...")

# 1. Waxflower: cluster of white flowers, pink centers
rebuild_flower("waxflower",
    stem_cx=15, calyx_w=5,
    leaves=[(27, -1, 3), (29, 1, 3), (25, 1, 2)])

# 2. Aster: purple daisy with yellow center
rebuild_flower("aster",
    stem_cx=15, calyx_w=4,
    leaves=[(26, -1, 3), (28, 1, 3)])

# 3. Dancing Lady: arching yellow orchid stem
# This one has flowers on right side, stem should come from left-bottom
rebuild_flower("dancing_lady",
    stem_cx=11, calyx_w=3, curve=3,
    leaves=[(27, -1, 2), (29, 1, 2)])

# 4. Chamomile: white daisy with yellow center
rebuild_flower("chamomile",
    stem_cx=15, calyx_w=4,
    leaves=[(26, -1, 3), (28, 1, 3)])

# 5. Oncidium: vertical yellow orchid spike
rebuild_flower("oncidium",
    stem_cx=15, calyx_w=3,
    leaves=[(27, -1, 3), (29, 1, 3)])

# 6. Anemone: large purple flower
rebuild_flower("anemone",
    stem_cx=15, calyx_w=4,
    leaves=[(26, -1, 3), (28, 1, 3)])

# 7. Astilbe: pink feather plume
rebuild_flower("astilbe",
    stem_cx=15, calyx_w=3,
    leaves=[(28, -1, 2), (29, 1, 2)])

# 8. Hydrangea: blue round cluster
rebuild_flower("hydrangea",
    stem_cx=15, calyx_w=5,
    leaves=[(27, -1, 3), (29, 1, 3)])

# 9. Bells of Ireland: green bell spike
# This one is all green, need different approach
rebuild_flower("bells_of_ireland",
    stem_cx=15, calyx_w=3,
    leaves=[(28, -1, 3), (29, 1, 3)])

# 10. Hypericum: red berry cluster
rebuild_flower("hypericum",
    stem_cx=15, calyx_w=4,
    leaves=[(27, -1, 3), (29, 1, 3)])

# 11. Lupine: purple spike
rebuild_flower("lupine",
    stem_cx=14, calyx_w=3,
    leaves=[(27, -1, 4), (29, 1, 4)])

# 12. Wintersweet: yellow flower cluster
rebuild_flower("wintersweet",
    stem_cx=13, calyx_w=4,
    leaves=[(27, -1, 3), (28, 1, 3), (29, -1, 2)])

print("\nAll stems rebuilt!")
