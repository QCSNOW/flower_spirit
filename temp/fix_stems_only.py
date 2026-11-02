"""
Targeted fixes only - don't touch flower shapes, only fix stems.

Category A: Crop flower to top, add gradient stem at bottom
  - waxflower, anemone, hydrangea, astilbe

Category B: Replace green column stem with gradient stem + leaves  
  - aster, dancing_lady, chamomile, oncidium, hypericum

Category C: Redesign column into cluster + stem
  - bells_of_ireland
"""
import numpy as np
from PIL import Image

TARGET = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

# Stem gradient colors
G_VL = (145, 195, 55)   # brightest
G_L  = (115, 170, 35)   # light
G_M  = (85, 145, 20)    # mid
G_D  = (55, 100, 10)    # dark
G_DEEP = (35, 75, 5)    # deepest

def px(arr, y, x, c):
    if 0 <= y < TARGET and 0 <= x < TARGET:
        r, g, b = c
        arr[y, x] = [r, g, b, 255]

def draw_gradient_stem(arr, cx, top, bot, curve=0):
    """Natural tapered stem with gradient + slight curve."""
    for y in range(top, bot + 1):
        t = (y - top) / max(1, bot - top)
        x = cx + int(t * curve)
        # Center 2px
        px(arr, y, x, G_M)
        px(arr, y, x + 1, G_M)
        # Left highlight
        px(arr, y, x - 1, G_L)
        # Right shadow
        px(arr, y, x + 2, G_D)
        # Base thickening
        if y > bot - 4:
            px(arr, y, x - 2, G_D)
            px(arr, y, x + 3, G_DEEP)

def draw_leaf(arr, cx, cy, direction, size=3):
    """Draw a leaf pointing left or right."""
    for dy in range(-size, size + 1):
        w = max(1, size - abs(dy))
        for dx in range(1, w + 2):
            x = cx + dx * direction
            y = cy + dy
            if dy < 0:
                px(arr, y, x, G_L)
            elif dy > 0:
                px(arr, y, x, G_D)
            else:
                px(arr, y, x, G_VL if dx < w else G_M)

def add_stem_to_flower(name, flower_end_y, stem_cx=15, curve=0, leaf_ys=None):
    """Add gradient stem below flower without touching flower pixels."""
    path = f"{DST}\\{name}.png"
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    
    # Clear area below flower (remove any existing stem pixels)
    for y in range(flower_end_y, TARGET):
        for x in range(TARGET):
            arr[y, x, 3] = 0
    
    # Add transition pixels (dark green at flower base)
    for x in range(stem_cx - 1, stem_cx + 3):
        px(arr, flower_end_y, x, G_D)
    
    # Draw gradient stem
    draw_gradient_stem(arr, stem_cx, flower_end_y + 1, 31, curve)
    
    # Add leaves
    if leaf_ys:
        for i, ly in enumerate(leaf_ys):
            if i % 2 == 0:
                draw_leaf(arr, stem_cx - 1, ly, -1, size=3)
            else:
                draw_leaf(arr, stem_cx + 2, ly, 1, size=3)
    
    img = Image.fromarray(arr, 'RGBA')
    img.save(path, 'PNG')
    n = int(np.sum(arr[:,:,3] > 0))
    colors = set()
    for y in range(TARGET):
        for x in range(TARGET):
            if arr[y, x, 3] > 0:
                colors.add(tuple(arr[y, x, :3]))
    print(f"  {name}: {n}px, {len(colors)} colors")

def replace_column_stem(name, stem_start_y, stem_cx=15, stem_width=4, curve=0, leaf_ys=None):
    """Replace existing column stem with gradient stem."""
    path = f"{DST}\\{name}.png"
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    
    # Find the stem region and clear it
    for y in range(stem_start_y, TARGET):
        for x in range(TARGET):
            r, g, b, a = arr[y, x]
            if a > 0 and g > r + 10 and g > b + 10:
                # This is a green stem pixel, clear it
                arr[y, x, 3] = 0
    
    # Add transition
    for x in range(stem_cx - 1, stem_cx + 3):
        px(arr, stem_start_y, x, G_D)
    
    # Draw gradient stem
    draw_gradient_stem(arr, stem_cx, stem_start_y + 1, 31, curve)
    
    # Add leaves
    if leaf_ys:
        for i, ly in enumerate(leaf_ys):
            if i % 2 == 0:
                draw_leaf(arr, stem_cx - 1, ly, -1, size=3)
            else:
                draw_leaf(arr, stem_cx + 2, ly, 1, size=3)
    
    img = Image.fromarray(arr, 'RGBA')
    img.save(path, 'PNG')
    n = int(np.sum(arr[:,:,3] > 0))
    colors = set()
    for y in range(TARGET):
        for x in range(TARGET):
            if arr[y, x, 3] > 0:
                colors.add(tuple(arr[y, x, :3]))
    print(f"  {name}: {n}px, {len(colors)} colors")

def crop_and_add_stem(name, crop_y, stem_cx=15, curve=0, leaf_ys=None):
    """Crop flower to top portion, add stem below."""
    path = f"{DST}\\{name}.png"
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    
    # Clear everything below crop_y
    for y in range(crop_y, TARGET):
        for x in range(TARGET):
            arr[y, x, 3] = 0
    
    # Add transition
    for x in range(stem_cx - 1, stem_cx + 3):
        px(arr, crop_y, x, G_D)
    
    # Draw gradient stem
    draw_gradient_stem(arr, stem_cx, crop_y + 1, 31, curve)
    
    # Add leaves
    if leaf_ys:
        for i, ly in enumerate(leaf_ys):
            if i % 2 == 0:
                draw_leaf(arr, stem_cx - 1, ly, -1, size=3)
            else:
                draw_leaf(arr, stem_cx + 2, ly, 1, size=3)
    
    img = Image.fromarray(arr, 'RGBA')
    img.save(path, 'PNG')
    n = int(np.sum(arr[:,:,3] > 0))
    colors = set()
    for y in range(TARGET):
        for x in range(TARGET):
            if arr[y, x, 3] > 0:
                colors.add(tuple(arr[y, x, :3]))
    print(f"  {name}: {n}px, {len(colors)} colors")


print("=== Category A: Crop flower + add stem ===")
# Waxflower: flower ends ~y=29, crop at y=22, add stem
crop_and_add_stem('waxflower', crop_y=22, stem_cx=15, curve=1, leaf_ys=[25, 29])

# Anemone: flower fills to y=30, crop at y=20, add stem
crop_and_add_stem('anemone', crop_y=20, stem_cx=15, curve=-1, leaf_ys=[24, 28])

# Hydrangea: flower fills to y=29, crop at y=20, add stem
crop_and_add_stem('hydrangea', crop_y=20, stem_cx=15, curve=1, leaf_ys=[24, 28])

# Astilbe: plume ends ~y=19, just add stem below
add_stem_to_flower('astilbe', flower_end_y=19, stem_cx=15, curve=0, leaf_ys=[23, 28])

print("\n=== Category B: Replace column stem ===")
# Aster: stem starts y=21, cx=15
replace_column_stem('aster', stem_start_y=21, stem_cx=15, curve=-1, leaf_ys=[24, 28])

# Dancing lady: stem starts y=17, cx=15
replace_column_stem('dancing_lady', stem_start_y=17, stem_cx=15, curve=2, leaf_ys=[21, 26])

# Chamomile: stem starts y=17, cx=15
replace_column_stem('chamomile', stem_start_y=17, stem_cx=15, curve=-1, leaf_ys=[21, 26])

# Oncidium: stem starts y=19, cx=15
replace_column_stem('oncidium', stem_start_y=19, stem_cx=15, curve=1, leaf_ys=[23, 28])

# Hypericum: stem starts y=17, cx=14
replace_column_stem('hypericum', stem_start_y=17, stem_cx=15, curve=-1, leaf_ys=[21, 26])

print("\n=== Category C: Bells of Ireland redesign ===")
# Bells of Ireland: all green column, needs distinct bell shapes + stem
path = f"{DST}\\bells_of_ireland.png"
arr = np.zeros((TARGET, TARGET, 4), dtype=np.uint8)

# 4 distinct bell calyces with gaps between them
def draw_bell(arr, cx, top, bot, width):
    rows = bot - top + 1
    for i in range(rows):
        y = top + i
        t = i / max(1, rows - 1)
        if t < 0.2:
            w = max(1, int(width * 0.4))
        elif t < 0.8:
            w = width
        else:
            w = max(1, int(width * 0.6))
        for dx in range(-w, w + 1):
            x = cx + dx
            if abs(dx) == w:
                px(arr, y, x, G_DEEP)
            elif abs(dx) >= w - 1:
                px(arr, y, x, G_D)
            elif abs(dx) <= 1:
                px(arr, y, x, G_VL)
            elif abs(dx) <= 2:
                px(arr, y, x, G_L)
            else:
                px(arr, y, x, G_M)
    # Tiny white flower inside
    mid = (top + bot) // 2
    px(arr, mid, cx, (240, 235, 200))

# 4 bells with gaps
draw_bell(arr, 15, 2, 6, 3)
draw_bell(arr, 15, 8, 12, 4)
draw_bell(arr, 15, 14, 18, 4)
draw_bell(arr, 15, 20, 23, 3)

# Stem below
draw_gradient_stem(arr, 15, 24, 31, curve=0)
draw_leaf(arr, 14, 27, -1, size=2)
draw_leaf(arr, 16, 30, 1, size=2)

img = Image.fromarray(arr, 'RGBA')
img.save(path, 'PNG')
n = int(np.sum(arr[:,:,3] > 0))
colors = set()
for y in range(TARGET):
    for x in range(TARGET):
        if arr[y, x, 3] > 0:
            colors.add(tuple(arr[y, x, :3]))
print(f"  bells_of_ireland: {n}px, {len(colors)} colors")

print("\n=== Lupine & Wintersweet: check ===")
# Lupine: check if has column stem
path = f"{DST}\\lupine.png"
img = Image.open(path).convert('RGBA')
arr = np.array(img)
# Check rows 20-31 for green column
stem_count = 0
for y in range(20, 32):
    for x in range(32):
        r, g, b, a = arr[y, x]
        if a > 0 and g > r + 10 and g > b + 10:
            stem_count += 1
if stem_count > 20:
    print(f"  lupine: has {stem_count} green stem pixels, fixing...")
    replace_column_stem('lupine', stem_start_y=20, stem_cx=15, curve=0, leaf_ys=[24, 28])
else:
    print(f"  lupine: only {stem_count} green pixels, OK")

# Wintersweet: branch shape, probably OK
path = f"{DST}\\wintersweet.png"
img = Image.open(path).convert('RGBA')
arr = np.array(img)
stem_count = 0
for y in range(20, 32):
    for x in range(32):
        r, g, b, a = arr[y, x]
        if a > 0 and g > r + 10 and g > b + 10:
            stem_count += 1
print(f"  wintersweet: {stem_count} green pixels in bottom area, leaving as-is")

print("\n=== DONE ===")
