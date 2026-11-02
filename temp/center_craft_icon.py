"""Fix: crafting table icon shift up-left by 1 pixel to center properly.
Count sort icon stays as green down arrow (already correct in v6).
"""
import numpy as np
from PIL import Image

tex = Image.open(r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\gui\flower_bag.png")
tex_arr = np.array(tex.convert('RGBA'))
TEX_W, TEX_H = 256, 256

C_DARK = (55, 55, 55, 255)
C_MID = (139, 139, 139, 255)
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
# Crafting table icon at (176, 0), 12x12
# Shift the grid up-left by 1 pixel
# Old grid offset: (1, 1) -> New grid offset: (0, 0)
# Grid is 10x10 (4 lines at 0,3,6,9 = 9 pixels wide... wait 0 to 9 is 10 pixels)
# =========================================

X0 = 176
Y0 = 0
clear_area(tex_arr, X0, Y0, 12, 12)

# Fill background
for y in range(12):
    for x in range(12):
        px(tex_arr, Y0 + y, X0 + x, C_BG)

# Grid at offset (0,0) - 10x10 grid in 12x12 icon
# Wait, that leaves 2px on right and 2px on bottom. Not centered.
# User said "向左上平移一格" so let's do exactly that.
# But let me think about what "centered" means visually.
# 
# Actually the issue might be that the grid was 10px but visually the rightmost cell
# looked cut off. Let me try grid offset (1, 1) with 11px grid... no.
#
# Let's just do what user asked: shift up-left by 1.
# Previous was gox=1, goy=1. New is gox=0, goy=0.

gox, goy = 0, 0

# 4 vertical lines
for i in range(4):
    vx = gox + i * 3
    if 0 <= vx < 12:
        for y in range(10):
            yy = goy + y
            if 0 <= yy < 12:
                px(tex_arr, Y0 + yy, X0 + vx, C_DARK)

# 4 horizontal lines
for i in range(4):
    hy = goy + i * 3
    if 0 <= hy < 12:
        for x in range(10):
            xx = gox + x
            if 0 <= xx < 12:
                px(tex_arr, Y0 + hy, X0 + xx, C_DARK)

# Fill cell interiors (2x2)
for cy in range(3):
    for cx in range(3):
        ix = gox + cx * 3 + 1
        iy = goy + cy * 3 + 1
        for dy in range(2):
            for dx in range(2):
                if 0 <= iy+dy < 12 and 0 <= ix+dx < 12:
                    px(tex_arr, Y0 + iy + dy, X0 + ix + dx, C_MID)

print("Crafting table icon: shifted up-left by 1 pixel (grid at 0,0)")

# Verify the grid bounds
leftmost = 999
rightmost = -1
topmost = 999
bottommost = -1
for y in range(12):
    for x in range(12):
        r, g, b, a = tex_arr[Y0 + y, X0 + x]
        if (r, g, b) == (55, 55, 55):  # dark border
            leftmost = min(leftmost, x)
            rightmost = max(rightmost, x)
            topmost = min(topmost, y)
            bottommost = max(bottommost, y)

grid_w = rightmost - leftmost + 1
grid_h = bottommost - topmost + 1
print(f"  Grid bounds: x=[{leftmost},{rightmost}] y=[{topmost},{bottommost}]")
print(f"  Grid size: {grid_w}x{grid_h}")
print(f"  Left margin: {leftmost}px, Right margin: {11 - rightmost}px")
print(f"  Top margin: {topmost}px, Bottom margin: {11 - bottommost}px")

# Save
out = Image.fromarray(tex_arr, 'RGBA')
out.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v7.png")
print(f"\nSaved: {out.size}")

zoom = out.resize((TEX_W*4, TEX_H*4), Image.NEAREST)
zoom.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v7_4x.png")
print("Saved 4x preview")
