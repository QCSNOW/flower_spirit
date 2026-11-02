"""Redo icons:
1. Crafting table icon - properly centered 3x3 grid in 12x12
2. Sort icons: A, ID, beacon base (3-tier pyramid)
"""
import numpy as np
from PIL import Image

# Load existing texture
tex = Image.open(r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\gui\flower_bag.png")
tex_arr = np.array(tex.convert('RGBA'))
TEX_W, TEX_H = 256, 256

C_DARK = (55, 55, 55, 255)
C_MID = (139, 139, 139, 255)
C_LIGHT = (198, 198, 198, 255)
C_BG = (85, 85, 85, 255)  # button interior bg
TRANSPARENT = (0, 0, 0, 0)

def px(arr, y, x, color):
    if 0 <= y < TEX_H and 0 <= x < TEX_W:
        arr[y, x] = color

def clear_area(arr, x0, y0, w, h):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            px(arr, y, x, TRANSPARENT)

# =========================================
# 1. Crafting table icon - centered symmetric 3x3 grid (12x12)
# Layout: 1px margin + 1px border + 2px inner + 1px border + 2px inner + 1px border + 2px inner + 1px border + 1px margin
# Total: 1 + 1+2+1+2+1+2+1 + 1 = 12 ✓
# =========================================
X0 = 176
Y0 = 0
clear_area(tex_arr, X0, Y0, 12, 12)

# Fill with button background first
for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

# Draw 3x3 grid
# Vertical lines at columns 1, 4, 7, 10 (0-indexed within icon)
# Horizontal lines at rows 1, 4, 7, 10
v_lines = [1, 4, 7, 10]  # 4 vertical lines = 3 cells
h_lines = [1, 4, 7, 10]  # 4 horizontal lines = 3 cells

for vl in v_lines:
    for y in range(1, 11):  # from row 1 to row 10 inclusive
        px(tex_arr, Y0 + y, X0 + vl, C_DARK)

for hl in h_lines:
    for x in range(1, 11):  # from col 1 to col 10 inclusive
        px(tex_arr, Y0 + hl, X0 + x, C_DARK)

# Fill cell interiors with mid gray
# Cells are at:
#   col 2-3, row 2-3  (top-left)
#   col 5-6, row 2-3  (top-mid)
#   col 8-9, row 2-3  (top-right)
#   col 2-3, row 5-6  (mid-left)
#   etc.
for cell_y in range(3):
    for cell_x in range(3):
        start_x = 2 + cell_x * 3  # 2, 5, 8
        start_y = 2 + cell_y * 3  # 2, 5, 8
        for iy in range(2):
            for ix in range(2):
                px(tex_arr, Y0 + start_y + iy, X0 + start_x + ix, C_MID)

print("Redone crafting table icon (centered 3x3)")

# =========================================
# 2. Sort icon "A" - for name sort (12x12)
# =========================================
X0 = 240
Y0 = 0
clear_area(tex_arr, X0, Y0, 12, 12)

# Fill background
for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

# Draw capital letter "A"
# A shape: two diagonal sides + horizontal bar
# Dark outline, light interior
# Let's make it 8px wide, 10px tall, centered in 12x12
# Offset: x=2, y=1
A_x = 2
A_y = 1

# A outline (dark)
# Left side: from bottom-left going up-right
# Row 9 (bottom): x=2 to x=3 (base left)
# Row 8: x=2 to x=3
# ...
# Row 1 (top): x=5 to x=6 (apex)
# Right side: from top going down-right
# Bottom bar: row 6, x=3 to x=7

# Simpler approach: draw A pixel by pixel
a_pixels = [
    # (row, col_start, col_end) for dark outline
    (0, 5, 6),   # top apex
    (1, 4, 7),   # widening
    (2, 4, 7),
    (3, 3, 8),
    (4, 3, 8),
    (5, 2, 9),   # widest - crossbar level
    (6, 2, 9),   # crossbar
    (7, 2, 9),
    (8, 2, 9),
    (9, 2, 9),   # bottom
]

# Draw dark outline
for row, cs, ce in a_pixels:
    for x in range(cs, ce + 1):
        px(tex_arr, Y0 + A_y + row, X0 + A_x + x, C_DARK)

# Fill interior with light gray
# Inside of A: everything inside the outline except the hole
# Top part (rows 1-4): triangular
# Middle (row 5-6): crossbar is full width
# Bottom (rows 7-9): two legs

# Let's just manually set the interior pixels
interior_pixels = [
    # (row, col) - mid gray interior
    (1, 5), (1, 6),
    (2, 5), (2, 6),
    (3, 4), (3, 5), (3, 6), (3, 7),
    (4, 4), (4, 5), (4, 6), (4, 7),
    # row 5-6: crossbar area - interior on left and right of crossbar? No, crossbar goes all the way across
    # Actually the crossbar IS the horizontal line in the A
    # Let me rethink - the A has a hole in the middle above the crossbar
]

# Actually simpler: draw the A properly
# Clear the area and redo
clear_area(tex_arr, X0 + A_x, Y0 + A_y, 9, 10)

# Letter A: 8 wide, 10 tall
# Dark outline, light fill, dark crossbar
for row in range(10):
    for col in range(9):
        px(tex_arr, Y0 + A_y + row, X0 + A_x + col, C_BG)

# Draw A shape
# Left edge column: starts at row 5, goes up to row 1, moving right
# Right edge column: starts at row 5, goes up to row 1, moving left
# Bottom: row 9, full width
# Crossbar: row 5/6

# Pixel by pixel A (dark = D, light interior = L, background = B)
# Using 8 wide, 10 tall:
A_shape = [
    "  DDDD  ",  # row 0: top (4px)
    " DDLLDD ",  # row 1
    " DDLLDD ",  # row 2
    "DDLLLLDD",  # row 3
    "DDLLLLDD",  # row 4
    "DDDDDDDD",  # row 5: crossbar
    "DDDLLDDD",  # row 6: below crossbar, two legs start
    "DDLLLLDD",  # wait no, the hole is ABOVE the crossbar
]

# Let me just do it clean and simple
# A: 7 wide, 9 tall, centered
A_chars = [
    "  DDD  ",   # 0: top
    " DLLLD ",   # 1
    " DLLLD ",   # 2
    "DLLLLLD",   # 3
    "DLLLLLD",   # 4
    "DDDDDDD",   # 5: crossbar
    "DLLLLLD",   # 6: legs
    "DLLLLLD",   # 7
    "DLLLLLD",   # 8
]

aox, aoy = 2, 1  # offset within 12x12 icon
for row, line in enumerate(A_chars):
    for col, ch in enumerate(line):
        if ch == 'D':
            px(tex_arr, Y0 + aoy + row, X0 + aox + col, C_DARK)
        elif ch == 'L':
            px(tex_arr, Y0 + aoy + row, X0 + aox + col, C_LIGHT)

print("Redone sort icon: A (name sort)")

# =========================================
# 3. Sort icon "ID" - for type/category sort (12x12)
# =========================================
# at UV (224, 16)
X0 = 224
Y0 = 16
clear_area(tex_arr, X0, Y0, 12, 12)

# Fill background
for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

# Draw "ID" letters, dark outline, light interior
# "I": simple vertical bar
# "D": left straight + right curve

# I (4 wide, 9 tall)
I_chars = [
    "DDDD",
    "DLLD",
    "DLLD",
    "DLLD",
    "DLLD",
    "DLLD",
    "DLLD",
    "DLLD",
    "DDDD",
]

iox, ioy = 1, 1
for row, line in enumerate(I_chars):
    for col, ch in enumerate(line):
        if ch == 'D':
            px(tex_arr, Y0 + ioy + row, X0 + iox + col, C_DARK)
        elif ch == 'L':
            px(tex_arr, Y0 + ioy + row, X0 + iox + col, C_LIGHT)

# D (6 wide, 9 tall)
D_chars = [
    "DDDDD ",
    "DLLLD ",
    "DLLLD ",
    "DLLLD ",
    "DLLLD ",
    "DLLLD ",
    "DLLLD ",
    "DLLLD ",
    "DDDDD ",
]

dox, doy = 6, 1
for row, line in enumerate(D_chars):
    for col, ch in enumerate(line):
        if ch == 'D':
            px(tex_arr, Y0 + doy + row, X0 + dox + col, C_DARK)
        elif ch == 'L':
            px(tex_arr, Y0 + doy + row, X0 + dox + col, C_LIGHT)

print("Redone sort icon: ID (type sort)")

# =========================================
# 4. Sort icon - beacon/pyramid base for count sort (12x12)
# 3 tiers, light gray, pixel art style
# =========================================
# at UV (240, 16)
X0 = 240
Y0 = 16
clear_area(tex_arr, X0, Y0, 12, 12)

# Fill background
for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

# Beacon base - 3-tier pyramid (like a mini pyramid, 3 rows tall total for the tiers)
# Actually "3排高" means 3 rows of height
# Light gray colors - use the GUI palette
# Top tier: smallest (4 wide, 2 tall)
# Middle tier: medium (8 wide, 2 tall)
# Bottom tier: largest (12 wide, 2 tall)
# Total: 6 tall, centered vertically

# Use 3 shades for 3D effect
PY_DARK = C_DARK     # dark gray edges
PY_MID = C_MID       # mid gray sides
PY_LIGHT = C_LIGHT   # light gray tops

# Beacon base pyramid (front view with 3D perspective)
# 3 tiers, each 2px tall
# Bottom tier (rows 7-8): full width 12
# Middle tier (rows 5-6): 8 wide, centered
# Top tier (rows 3-4): 4 wide, centered
# Actually let's make it more 3D with highlights on top-left and shadows on bottom-right

beacon = [
    # col: 0  1  2  3  4  5  6  7  8  9  10 11
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 0
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 1
    [ 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],  # row 2 - top tier top (light)
    [ 0, 0, 0, 2, 1, 1, 1, 3, 2, 0, 0, 0],  # row 3 - top tier side (mid/dark)
    [ 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],  # row 4 - mid tier top (light)
    [ 0, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 0],  # row 5 - mid tier side
    [ 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2],  # row 6 - bottom tier top
    [ 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2],  # row 7 - bottom tier side
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 8
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 9
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 10
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 11
]

# 0 = transparent/bg, 1 = PY_LIGHT (top highlight), 2 = PY_MID (side), 3 = PY_DARK (shadow edge)
color_map = {0: None, 1: PY_LIGHT, 2: PY_MID, 3: PY_DARK}

for row in range(12):
    for col in range(12):
        c = beacon[row][col]
        if c != 0:
            px(tex_arr, Y0 + row, X0 + col, color_map[c])

print("Redone sort icon: beacon base (count sort)")

# =========================================
# Save
# =========================================
out = Image.fromarray(tex_arr, 'RGBA')
out.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v5.png")
print(f"\nSaved: {out.size}")

# 3x preview
zoom = out.resize((TEX_W*3, TEX_H*3), Image.NEAREST)
zoom.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v5_3x.png")
print("Saved 3x preview")
