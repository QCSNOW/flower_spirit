"""Add button icons and other elements to the flower_bag GUI texture.

Texture layout (256x256):
- Top-left 176x166: GUI background
- Right side (x=176+) and bottom (y=166+): icon sprites

Icons to add (each 12x12, placed in the unused area):
  1. crafting_table_icon: 3x3 crafting grid (top-down view) - at (176, 0)
  2. flower_bag_icon: desaturated flower bag - at (192, 0)
  3. flower_bag_up: flower bag + green up arrow - at (208, 0)
  4. flower_bag_down: flower bag + green down arrow - at (224, 0)
  5. sort_icon: A/Z sort symbol - at (240, 0)
  6. red_x: red X overlay (for disabled state) - at (176, 16)
  7. arrow_up_green: green up arrow (small) - at (192, 16)
  8. arrow_down_green: green down arrow (small) - at (208, 16)
  9. sort_number: 123 sort icon - at (224, 16)
  10. sort_down: down arrow sort icon - at (240, 16)
"""
import numpy as np
from PIL import Image

# Load existing GUI texture
gui = Image.open(r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\gui\flower_bag.png")
gui_arr = np.array(gui.convert('RGBA'))
TEX_W, TEX_H = 256, 256

# Load flower bag item texture for desaturation
bag = Image.open(r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\flower_bag.png")
bag_arr = np.array(bag.convert('RGBA'))

def px(arr, y, x, color):
    if 0 <= y < TEX_H and 0 <= x < TEX_W:
        arr[y, x] = color

def draw_icon(arr, icon_data, x0, y0):
    """Draw icon from 2D list of RGBA tuples/None (transparent)."""
    for y, row in enumerate(icon_data):
        for x, c in enumerate(row):
            if c is not None:
                px(arr, y0 + y, x0 + x, c)

# =========================================
# 1. Crafting table icon (12x12) - top-down 3x3 grid
# =========================================
C_DARK = (55, 55, 55, 255)     # slot border
C_MID = (139, 139, 139, 255)   # slot interior / mid gray
C_LIGHT = (198, 198, 198, 255) # background gray

crafting_icon = [
    [C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT],
    [C_LIGHT, C_DARK,  C_DARK,  C_DARK,  C_MID,   C_DARK,  C_DARK,  C_DARK,  C_MID,   C_DARK,  C_DARK,  C_LIGHT],
    [C_LIGHT, C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_LIGHT],
    [C_LIGHT, C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_LIGHT],
    [C_LIGHT, C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_LIGHT],
    [C_LIGHT, C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_LIGHT],
    [C_LIGHT, C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_LIGHT],
    [C_LIGHT, C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_LIGHT],
    [C_LIGHT, C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_LIGHT],
    [C_LIGHT, C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_MID,   C_MID,   C_DARK,  C_MID,   C_LIGHT],
    [C_LIGHT, C_DARK,  C_DARK,  C_DARK,  C_MID,   C_DARK,  C_DARK,  C_DARK,  C_MID,   C_DARK,  C_DARK,  C_LIGHT],
    [C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT, C_LIGHT],
]
draw_icon(gui_arr, crafting_icon, 176, 0)
print("Added crafting table icon")

# =========================================
# 2. Desaturated flower bag icon (12x12)
# =========================================
# The flower bag item is 16x16, we need to scale it down to 12x12 and desaturate
from PIL import Image as PILImage
bag_small = bag.resize((12, 12), PILImage.NEAREST)
bag_small_arr = np.array(bag_small.convert('RGBA'))

# Desaturate: convert to grayscale but keep in gray family matching GUI palette
# Map colors to the 4 GUI gray levels
for y in range(12):
    for x in range(12):
        r, g, b, a = bag_small_arr[y, x]
        if a < 50:
            continue
        # Calculate luminance
        lum = int(0.299 * r + 0.587 * g + 0.114 * b)
        # Map to nearest GUI gray
        if lum > 210:
            new_color = (255, 255, 255, 255)
        elif lum > 165:
            new_color = (198, 198, 198, 255)
        elif lum > 100:
            new_color = (139, 139, 139, 255)
        else:
            new_color = (55, 55, 55, 255)
        px(gui_arr, y, 192 + x, new_color)
print("Added desaturated flower bag icon")

# =========================================
# 3. Flower bag + green up arrow (12x12)
# =========================================
# Copy desaturated bag first
for y in range(12):
    for x in range(12):
        px(gui_arr, y, 208 + x, gui_arr[y, 192 + x])

# Add green up arrow in bottom-right corner
# Small 5x5 arrow, positioned at bottom-right of 12x12 icon
GREEN_LIGHT = (85, 220, 85, 255)
GREEN_DARK = (30, 130, 30, 255)
GREEN_MID = (50, 180, 50, 255)

# Up arrow (pointing up, small 5px wide, 6px tall)
# Position: x=7 to 11, y=6 to 11 (bottom-right area of 12x12 icon)
arrow_up = [
    # col 0  1  2  3  4
    [None, None, GREEN_DARK,  None, None],       # row 0: tip
    [None, GREEN_DARK, GREEN_MID, GREEN_DARK, None],  # row 1
    [GREEN_DARK, GREEN_MID, GREEN_LIGHT, GREEN_MID, GREEN_DARK], # row 2: widest
    [None, None, GREEN_MID, None, None],         # row 3: shaft
    [None, None, GREEN_MID, None, None],         # row 4: shaft
    [None, GREEN_DARK, GREEN_DARK, GREEN_DARK, None], # row 5: base
]
draw_icon(gui_arr, arrow_up, 208 + 6, 5)  # place at bottom-right
print("Added flower bag + up arrow icon")

# =========================================
# 4. Flower bag + green down arrow (12x12)
# =========================================
# Copy desaturated bag first
for y in range(12):
    for x in range(12):
        px(gui_arr, y, 224 + x, gui_arr[y, 192 + x])

# Down arrow (pointing down, 5x6)
arrow_down = [
    [None, GREEN_DARK, GREEN_DARK, GREEN_DARK, None],  # row 0: top base
    [None, None, GREEN_MID, None, None],               # row 1: shaft
    [None, None, GREEN_MID, None, None],               # row 2: shaft
    [GREEN_DARK, GREEN_MID, GREEN_LIGHT, GREEN_MID, GREEN_DARK], # row 3: widest
    [None, GREEN_DARK, GREEN_MID, GREEN_DARK, None],   # row 4
    [None, None, GREEN_DARK, None, None],              # row 5: tip
]
draw_icon(gui_arr, arrow_down, 224 + 6, 5)  # place at bottom-right
print("Added flower bag + down arrow icon")

# =========================================
# 5. Sort icon (A/Z style) (12x12)
# =========================================
# A to Z sort symbol - "A↓Z" style, simplified
sort_icon = []
# Build a 12x12 icon with "A" and a small down arrow, and "Z"
# Make it simple: A on left, down arrow in middle, 1 on right (for quantity sort)
# Actually let's make the default sort icon be "A↓" pattern
sort_icon_data = [
    [None, None, C_DARK,  None, None, None, None, None, None, None, None, None],
    [None, C_DARK,  C_MID, C_DARK,  None, None, None, None, None, None, None, None],
    [None, C_DARK,  C_LIGHT, C_DARK, None, None, GREEN_DARK, None, None, None, None, None],
    [C_DARK,  C_MID,   C_MID,   C_MID,  C_DARK, None, GREEN_MID, None, None, None, None, None],
    [C_DARK,  C_LIGHT, C_DARK,  C_LIGHT, C_DARK, GREEN_DARK, GREEN_LIGHT, GREEN_DARK, None, None, None, None],
    [C_DARK,  C_MID,   C_DARK,  C_MID,  C_DARK, None, GREEN_MID, None, None, None, None, None],
    [C_DARK,  C_MID,   C_DARK,  C_MID,  C_DARK, None, GREEN_DARK, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK, None, None, None, None, None, None, None],
    [None, None, None, C_DARK,  None, None, None, None, None, None, None, None],
    [None, None, C_DARK, None, None, None, None, None, None, None, None, None],
    [C_DARK,  C_DARK,  C_DARK,  C_DARK,  C_DARK, None, None, None, None, None, None, None],
]
draw_icon(gui_arr, sort_icon_data, 240, 0)
print("Added sort icon (A↓Z)")

# =========================================
# 6. Red X overlay (12x12) - for disabled state
# =========================================
RED_DARK = (170, 30, 30, 255)
RED_MID = (220, 50, 50, 255)
RED_LIGHT = (255, 80, 80, 255)

red_x = [
    [RED_DARK,  None, None, None, None, None, None, None, None, None, RED_DARK],
    [RED_MID,   RED_DARK, None, None, None, None, None, None, None, RED_DARK, RED_LIGHT],
    [None, RED_MID,   RED_DARK, None, None, None, None, None, RED_DARK, RED_LIGHT, None],
    [None, None, RED_MID,   RED_DARK, None, None, None, RED_DARK, RED_LIGHT, None, None],
    [None, None, None, RED_MID,   RED_DARK, None, RED_DARK, RED_LIGHT, None, None, None],
    [None, None, None, None, RED_MID,   RED_DARK, RED_LIGHT, None, None, None, None],
    [None, None, None, None, RED_MID,   RED_DARK, RED_LIGHT, None, None, None, None],
    [None, None, None, RED_MID,   RED_DARK, None, RED_DARK, RED_LIGHT, None, None, None],
    [None, None, RED_MID,   RED_DARK, None, None, None, RED_DARK, RED_LIGHT, None, None],
    [None, RED_MID,   RED_DARK, None, None, None, None, None, RED_DARK, RED_LIGHT, None],
    [RED_MID,   RED_DARK, None, None, None, None, None, None, None, RED_DARK, RED_LIGHT],
    [RED_DARK,  None, None, None, None, None, None, None, None, None, RED_DARK],
]
draw_icon(gui_arr, red_x, 176, 16)
print("Added red X overlay")

# =========================================
# 7. & 8. Standalone green arrows (already done inline)
# 9. Number sort icon (123 style) at (224, 16)
# =========================================
num_sort_icon = [
    [None, C_DARK,  C_DARK,  C_DARK,  None, None, C_DARK,  C_DARK,  C_DARK,  None, None, None],
    [None, None, C_DARK,  None, None, C_DARK,  None, C_DARK,  None, None, None, None],
    [None, None, C_DARK,  None, None, None, None, C_DARK,  None, None, None, None],
    [None, C_DARK,  C_DARK,  C_DARK,  None, None, C_DARK,  C_DARK,  None, None, None, None],
    [None, C_DARK,  None, None, None, None, None, C_DARK,  None, None, None, None],
    [None, C_DARK,  None, None, None, C_DARK,  None, C_DARK,  None, None, None, None],
    [None, C_DARK,  C_DARK,  C_DARK,  None, C_DARK,  C_DARK,  C_DARK,  C_DARK, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
]
draw_icon(gui_arr, num_sort_icon, 224, 16)
print("Added number sort icon")

# =========================================
# 10. Down arrow sort icon at (240, 16)
# =========================================
down_sort_icon = [
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, C_DARK, C_DARK, C_DARK, C_DARK, C_DARK, None, None, None, None, None],
    [None, None, None, None, C_MID, None, None, None, None, None, None, None],
    [None, None, None, None, C_MID, None, None, None, None, None, None, None],
    [C_DARK, C_DARK, C_DARK, C_DARK, C_MID, C_DARK, C_DARK, C_DARK, C_DARK, None, None, None],
    [None, C_DARK, C_MID, C_MID, C_LIGHT, C_MID, C_MID, C_DARK, None, None, None, None],
    [None, None, C_DARK, C_MID, C_MID, C_MID, C_DARK, None, None, None, None, None],
    [None, None, None, C_DARK, C_MID, C_DARK, None, None, None, None, None, None],
    [None, None, None, None, C_DARK, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
]
draw_icon(gui_arr, down_sort_icon, 240, 16)
print("Added down sort icon")

# =========================================
# Also add standalone desaturated bag icon at (192, 16) for reference
# =========================================
# (already have the bag at 192,0 so skip)

# Save
out = Image.fromarray(gui_arr, 'RGBA')
out.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v4.png")
print(f"\nSaved texture: {out.size}")

# 2x preview
zoom = out.resize((TEX_W*2, TEX_H*2), Image.NEAREST)
zoom.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v4_2x.png")
print("Saved 2x preview")
