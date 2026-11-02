"""Fix:
1. Crafting table icon: revert to centered version (1px margin on all sides)
2. Sort count icon: beacon base (3 tiers, light gray pixels)
"""
import numpy as np
from PIL import Image

tex = Image.open(r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\gui\flower_bag.png")
tex_arr = np.array(tex.convert('RGBA'))
TEX_W, TEX_H = 256, 256

C_DARK = (55, 55, 55, 255)
C_MID = (139, 139, 139, 255)
C_LIGHT = (198, 198, 198, 255)
C_BG = (85, 85, 85, 255)
TRANSPARENT = (0, 0, 0, 0)

def px(arr, y, x, color):
    if 0 <= y < TEX_H and 0 <= x < TEX_W:
        arr[y, x] = color

def clear_area(arr, x0, y0, w, h):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            px(arr, y, x, TRANSPARENT)

# =========================================
# 1. Crafting table icon - centered with 1px margin on all sides
# 10x10 grid in 12x12 icon, offset (1,1) -> 1px left, 1px right, 1px top, 1px bottom
# =========================================
X0 = 176
Y0 = 0
clear_area(tex_arr, X0, Y0, 12, 12)

for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

gox, goy = 1, 1  # 1px margin on all sides -> centered

# 4 vertical lines
for i in range(4):
    vx = gox + i * 3
    for y in range(10):
        px(tex_arr, Y0 + goy + y, X0 + vx, C_DARK)

# 4 horizontal lines
for i in range(4):
    hy = goy + i * 3
    for x in range(10):
        px(tex_arr, Y0 + hy, X0 + gox + x, C_DARK)

# Fill cell interiors
for cy in range(3):
    for cx in range(3):
        ix = gox + cx * 3 + 1
        iy = goy + cy * 3 + 1
        for dy in range(2):
            for dx in range(2):
                px(tex_arr, Y0 + iy + dy, X0 + ix + dx, C_MID)

# Verify
leftmost = min([gox + i*3 for i in range(4)])
rightmost = max([gox + i*3 for i in range(4)])
topmost = min([goy + i*3 for i in range(4)])
bottommost = max([goy + i*3 for i in range(4)])
print(f"Crafting grid: x=[{leftmost},{rightmost}] y=[{topmost},{bottommost}]")
print(f"  Margins: L={leftmost} R={11-rightmost} T={topmost} B={11-bottommost}")

# =========================================
# 2. Sort count icon - beacon base, 3 tiers high, light gray
# at (240, 16), 12x12 icon
# =========================================
X0 = 240
Y0 = 16
clear_area(tex_arr, X0, Y0, 12, 12)

for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

# Beacon base - 3 tiers, light gray, front-facing with slight 3D
# "3排高" = 3 rows of tiers, each tier is about 3px tall
# Use light gray as primary (C_LIGHT), darker for side faces and edges
# 
# Layout (centered, 12x12):
# Tier 1 (top): smallest, 4 wide, at y=2
# Tier 2 (middle): medium, 8 wide, at y=5
# Tier 3 (bottom): largest, 12 wide, at y=8
# Each tier: 3px tall? No, 3 tiers total = "3排高"
# 
# Let me make it simple: 3 horizontal bars of decreasing size going up
# Light gray color scheme

# Bottom tier (largest) - full 12 wide, 3px tall
# Middle tier - 8 wide, 3px tall
# Top tier - 4 wide, 3px tall
# Total height: 9px, centered in 12x12 (top margin ~1.5 -> 1px, bottom ~2px)

tier_y = [2, 5, 8]  # top of each tier
tier_w = [4, 8, 12]  # width of each tier (smallest to largest going down)

for i in range(3):
    ty = tier_y[i]
    tw = tier_w[i]
    tx = (12 - tw) // 2  # center horizontally
    
    # Top face (lightest)
    for x in range(tw):
        px(tex_arr, Y0 + ty, X0 + tx + x, C_LIGHT)
    
    # Front face (mid light)
    for dy in range(1, 3):  # 2 more rows = 3 total
        for x in range(tw):
            px(tex_arr, Y0 + ty + dy, X0 + tx + x, C_MID)
    
    # Right side edge (darker) for 3D effect
    for dy in range(3):
        px(tex_arr, Y0 + ty + dy, X0 + tx + tw - 1, C_DARK)
    
    # Bottom edge of tier (darkest)
    if i < 2:  # not the bottom tier
        for x in range(tier_w[i+1]):
            bx = (12 - tier_w[i+1]) // 2
            # Only draw where the bottom tier top is visible
            pass  # actually the next tier covers it
    
    # Left edge highlight (slightly lighter than front)
    for dy in range(1, 3):
        px(tex_arr, Y0 + ty + dy, X0 + tx, C_LIGHT)

# Bottom tier bottom edge (dark)
for x in range(12):
    px(tex_arr, Y0 + 10, X0 + x, C_DARK)

print("Beacon base icon: 3 tiers, light gray, 3D effect")

# Save
out = Image.fromarray(tex_arr, 'RGBA')
out.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v8.png")
print(f"\nSaved: {out.size}")

zoom = out.resize((TEX_W*4, TEX_H*4), Image.NEAREST)
zoom.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v8_4x.png")
print("Saved 4x preview")
