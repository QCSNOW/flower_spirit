"""Fix icons:
1. Crafting table: keep original 3x3 pattern but center it properly in 12x12
2. Sort count mode: restore down arrow icon (was at 240,16 before we changed it to beacon)
3. Sort name: keep A letter
4. Sort type: keep ID letters
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
# 1. Crafting table icon - centered properly
# Original was 9 slots in a 3x3 grid.
# In 12x12 icon: slot size = 3px each (2px interior + 1px border)? 
# Let's make it 3x3 cells, each cell is 3px wide (1 border + 1 interior + 1 border)
# Total width of grid: 3 + 3 + 3 = 9px, leaving 1.5px margin on each side
# Use 10px wide grid with 1px margin on left, 1px on right = centered in 12x12
# 
# Actually: 3 cells, each cell interior is 2px, borders between are 1px
# Outer borders 1px, inner borders 1px, cell interiors 2px
# Total: 1 + 2 + 1 + 2 + 1 + 2 + 1 = 10px wide
# In 12x12 icon: offset by 1px on each side -> perfectly centered
# =========================================

X0 = 176
Y0 = 0
clear_area(tex_arr, X0, Y0, 12, 12)

# Fill background
for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

# Grid offset: 1px from all sides
gox, goy = 1, 1

# Draw the 3x3 crafting grid (10x10 area)
# Vertical lines: 0, 3, 6, 9 (relative to grid origin)
# Horizontal lines: 0, 3, 6, 9
for i in range(4):  # 4 vertical lines
    vx = gox + i * 3
    for y in range(10):
        px(tex_arr, Y0 + goy + y, X0 + vx, C_DARK)

for i in range(4):  # 4 horizontal lines
    hy = goy + i * 3
    for x in range(10):
        px(tex_arr, Y0 + hy, X0 + gox + x, C_DARK)

# Fill cell interiors (2x2 each) with mid gray
for cy in range(3):
    for cx in range(3):
        ix = gox + cx * 3 + 1  # 1px inside border
        iy = goy + cy * 3 + 1
        for dy in range(2):
            for dx in range(2):
                px(tex_arr, Y0 + iy + dy, X0 + ix + dx, C_MID)

print("Crafting table icon: centered 3x3 grid (10px grid in 12x12 icon)")

# =========================================
# 2. Sort count icon - restore down arrow (green arrow pointing down)
# at (240, 16) - 12x12
# =========================================

X0 = 240
Y0 = 16
clear_area(tex_arr, X0, Y0, 12, 12)

# Fill background
for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

# Green down arrow - centered in 12x12, about 8x10 size
GREEN_DARK = (30, 130, 30, 255)
GREEN_MID = (50, 180, 50, 255)
GREEN_LIGHT = (85, 220, 85, 255)

# Down arrow shape: shaft + arrowhead
# 8 wide, 10 tall, centered in 12x12 (offset 2, 1)
aox, aoy = 2, 1

down_arrow = [
    # 0   1   2   3   4   5   6   7
    [None, None, 'D', 'D', 'D', 'D', None, None],  # 0: top of shaft
    [None, None, 'D', 'M', 'M', 'D', None, None],  # 1
    [None, None, 'D', 'M', 'M', 'D', None, None],  # 2
    [None, None, 'D', 'M', 'M', 'D', None, None],  # 3
    [None, None, 'D', 'M', 'M', 'D', None, None],  # 4: shaft bottom
    [None, 'D', 'D', 'M', 'M', 'D', 'D', None],    # 5: arrowhead widening
    ['D', 'D', 'M', 'M', 'M', 'M', 'D', 'D'],      # 6: widest
    ['D', 'M', 'M', 'L', 'L', 'M', 'M', 'D'],      # 7: highlight
    [None, 'D', 'D', 'M', 'M', 'D', 'D', None],    # 8: tapering
    [None, None, None, 'D', 'D', None, None, None], # 9: tip
]

color_map = {'D': GREEN_DARK, 'M': GREEN_MID, 'L': GREEN_LIGHT}

for row in range(len(down_arrow)):
    for col in range(len(down_arrow[row])):
        ch = down_arrow[row][col]
        if ch is not None:
            px(tex_arr, Y0 + aoy + row, X0 + aox + col, color_map[ch])

print("Sort count icon: restored green down arrow")

# Save
out = Image.fromarray(tex_arr, 'RGBA')
out.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v6.png")
print(f"\nSaved: {out.size}")

zoom = out.resize((TEX_W*3, TEX_H*3), Image.NEAREST)
zoom.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v6_3x.png")
print("Saved 3x preview")
