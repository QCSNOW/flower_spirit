"""Create flower bag GUI texture: 176x166, MC style.
- 2 rows of 9 flower bag slots (top area)
- 3 rows of 9 player inventory slots
- 1 row of 9 hotbar slots
- Clean pixel-art beveled style
"""
import numpy as np
from PIL import Image

W, H = 176, 166

# Colors - standard MC GUI palette
BG = (198, 198, 198, 255)       # main background gray
BORDER_DARK = (55, 55, 55, 255)  # dark border (top/left of raised, bottom/right of recessed)
BORDER_LIGHT = (255, 255, 255, 255)  # light border (bottom/right of raised, top/left of recessed)
BORDER_MID = (139, 139, 139, 255)    # mid gray for inner details
SLOT_BG = (139, 139, 139, 255)       # slot interior
TRANSPARENT = (0, 0, 0, 0)

def px(arr, y, x, color):
    if 0 <= y < H and 0 <= x < W:
        arr[y, x] = color

def draw_raised_panel(arr, x, y, w, h):
    """Draw a raised beveled panel (like GUI background).
    Top/left = light, bottom/right = dark"""
    # Fill background
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(arr, yy, xx, BG)
    # Top border (light)
    for xx in range(x, x + w):
        px(arr, y, xx, BORDER_LIGHT)
    # Left border (light)
    for yy in range(y, y + h):
        px(arr, yy, x, BORDER_LIGHT)
    # Bottom border (dark)
    for xx in range(x, x + w):
        px(arr, y + h - 1, xx, BORDER_DARK)
    # Right border (dark)
    for yy in range(y, y + h):
        px(arr, yy, x + w - 1, BORDER_DARK)
    # Inner dark line (just inside light border) - creates the bevel
    for xx in range(x + 1, x + w - 1):
        px(arr, y + 1, xx, BORDER_MID)
    for yy in range(y + 1, y + h - 1):
        px(arr, yy, x + 1, BORDER_MID)
    # Inner light line (just inside dark border)
    for xx in range(x + 1, x + w - 1):
        px(arr, y + h - 2, xx, BORDER_MID)
    for yy in range(y + 1, y + h - 1):
        px(arr, yy, x + w - 2, BORDER_MID)


def draw_slot(arr, x, y):
    """Draw a single 18x18 item slot (recessed bevel).
    Standard MC slot: dark top/left border, light bottom/right highlight, gray interior."""
    # Fill interior
    for yy in range(y + 1, y + 17):
        for xx in range(x + 1, x + 17):
            px(arr, yy, xx, SLOT_BG)
    # Top border (dark - recessed shadow)
    for xx in range(x, x + 18):
        px(arr, y, xx, BORDER_DARK)
    # Left border (dark)
    for yy in range(y, y + 18):
        px(arr, yy, x, BORDER_DARK)
    # Bottom highlight (light - recessed bottom edge)
    for xx in range(x, x + 18):
        px(arr, y + 17, xx, BORDER_LIGHT)
    # Right highlight (light)
    for yy in range(y, y + 18):
        px(arr, yy, x + 17, BORDER_LIGHT)
    # Inner bevel - bottom/right interior has mid-gray shadow edge
    # (the interior has a darker pixel at bottom-right corner for depth)
    px(arr, y + 16, x + 16, BORDER_MID)
    # Bottom row interior (one pixel above bottom border) has slight darkening on right
    px(arr, y + 16, x + 15, (120, 120, 120, 255))
    # Right column interior has slight darkening on bottom
    px(arr, y + 15, x + 16, (120, 120, 120, 255))


def draw_slot_row(arr, start_x, y, count=9):
    for i in range(count):
        draw_slot(arr, start_x + i * 18, y)


# Create canvas
gui = np.zeros((H, W, 4), dtype=np.uint8)

# Draw main GUI panel
draw_raised_panel(gui, 0, 0, W, H)

# Layout calculations (standard MC proportions)
# Slot size: 18x18, 9 slots per row, first slot at x=8
SLOT_X = 8
SLOT_W = 18
COLS = 9

# Flower bag slots: 2 rows at top
# Leave some top margin, then 2 rows of flower slots
FLOWER_TOP_Y = 18    # top of first flower slot row
draw_slot_row(gui, SLOT_X, FLOWER_TOP_Y, COLS)
draw_slot_row(gui, SLOT_X, FLOWER_TOP_Y + SLOT_W, COLS)

# Player inventory: 3 rows
# Standard MC: inventory starts at y=84 in 166-tall GUI
INV_TOP_Y = 84
for i in range(3):
    draw_slot_row(gui, SLOT_X, INV_TOP_Y + i * SLOT_W, COLS)

# Hotbar: 1 row, 4px gap from inventory
HOTBAR_Y = INV_TOP_Y + 3 * SLOT_W + 4  # 84 + 54 + 4 = 142
draw_slot_row(gui, SLOT_X, HOTBAR_Y, COLS)

# Save
out = Image.fromarray(gui, 'RGBA')
out.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui.png")
print(f"Saved flower_bag_gui.png: {out.size}")

# Count unique colors
pixels = gui.reshape(-1, 4)
unique = np.unique(pixels, axis=0)
print(f"Unique colors: {len(unique)}")
for c in unique:
    print(f"  RGBA({c[0]},{c[1]},{c[2]},{c[3]})")

# Count slot pixels
slot_pixels = 0
for y in range(H):
    for x in range(W):
        if gui[y, x, 3] > 0:
            slot_pixels += 1
print(f"Total visible pixels: {slot_pixels}")

# Create a 4x zoomed preview for easy viewing
zoom = out.resize((W*4, H*4), Image.NEAREST)
zoom.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_4x.png")
print("Saved 4x zoomed preview")
