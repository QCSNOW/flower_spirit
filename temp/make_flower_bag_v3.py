"""Create flower bag GUI texture in standard 256x256 format.
MC expects GUI textures to be 256x256 (texture atlas convention).
The actual GUI content (176x166) goes in the top-left corner.

Layout (pixel-perfect):
- Button area: 5 recessed 14x14 buttons at y=6, x=[8,28,48,68,88]
- Flower bag slots: 2 rows x 9, y=26, x=8 (18px pitch)
- Player inventory: 3 rows x 9, y=84, x=8
- Hotbar: 1 row x 9, y=142, x=8
- Canvas: 256x256
"""
import numpy as np
from PIL import Image

TEX_W, TEX_H = 256, 256
GUI_W, GUI_H = 176, 166

# MC GUI color palette
BG = (198, 198, 198, 255)
BORDER_DARK = (55, 55, 55, 255)
BORDER_LIGHT = (255, 255, 255, 255)
BORDER_MID = (139, 139, 139, 255)
SLOT_BG = (139, 139, 139, 255)
TRANSPARENT = (0, 0, 0, 0)

def px(arr, y, x, color):
    if 0 <= y < TEX_H and 0 <= x < TEX_W:
        arr[y, x] = color

def draw_gui_panel(arr, x, y, w, h):
    """Standard MC raised GUI panel."""
    # Fill
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(arr, yy, xx, BG)
    # Outer light border (top/left)
    for xx in range(x, x + w):
        px(arr, y, xx, BORDER_LIGHT)
    for yy in range(y, y + h):
        px(arr, yy, x, BORDER_LIGHT)
    # Outer dark border (bottom/right)
    for xx in range(x, x + w):
        px(arr, y + h - 1, xx, BORDER_DARK)
    for yy in range(y, y + h):
        px(arr, yy, x + w - 1, BORDER_DARK)
    # Inner mid bevel (just inside light)
    for xx in range(x + 1, x + w - 1):
        px(arr, y + 1, xx, BORDER_MID)
    for yy in range(y + 1, y + h - 1):
        px(arr, yy, x + 1, BORDER_MID)
    # Inner mid bevel (just inside dark)
    for xx in range(x + 1, x + w - 1):
        px(arr, y + h - 2, xx, BORDER_MID)
    for yy in range(y + 1, y + h - 1):
        px(arr, yy, x + w - 2, BORDER_MID)


def draw_slot(arr, x, y):
    """Standard 18x18 recessed item slot."""
    # Interior 16x16
    for yy in range(y + 1, y + 17):
        for xx in range(x + 1, x + 17):
            px(arr, yy, xx, SLOT_BG)
    # Dark top/left (recessed shadow)
    for xx in range(x, x + 18):
        px(arr, y, xx, BORDER_DARK)
    for yy in range(y, y + 18):
        px(arr, yy, x, BORDER_DARK)
    # Light bottom/right (recessed highlight)
    for xx in range(x, x + 18):
        px(arr, y + 17, xx, BORDER_LIGHT)
    for yy in range(y, y + 18):
        px(arr, yy, x + 17, BORDER_LIGHT)
    # Bottom-right interior corner dark pixel
    px(arr, y + 16, x + 16, BORDER_DARK)


def draw_slot_row(arr, start_x, y, count=9):
    for i in range(count):
        draw_slot(arr, start_x + i * 18, y)


def draw_button(arr, x, y, size=14):
    """Draw a recessed button slot (14x14)."""
    # Darker interior
    for yy in range(y + 1, y + size - 1):
        for xx in range(x + 1, x + size - 1):
            px(arr, yy, xx, (85, 85, 85, 255))
    # Dark top/left
    for xx in range(x, x + size):
        px(arr, y, xx, BORDER_DARK)
    for yy in range(y, y + size):
        px(arr, yy, x, BORDER_DARK)
    # Light bottom/right
    for xx in range(x, x + size):
        px(arr, y + size - 1, xx, BORDER_LIGHT)
    for yy in range(y, y + size):
        px(arr, yy, x + size - 1, BORDER_LIGHT)
    # Bottom-right corner dark pixel
    px(arr, y + size - 2, x + size - 2, BORDER_DARK)


# ============ CREATE CANVAS ============
tex = np.zeros((TEX_H, TEX_W, 4), dtype=np.uint8)

# Draw GUI panel (top-left corner of 256x256 texture)
draw_gui_panel(tex, 0, 0, GUI_W, GUI_H)

# Buttons at top: 5 buttons, y=6, spaced 20px apart
BUTTON_Y = 6
for bx in [8, 28, 48, 68, 88]:
    draw_button(tex, bx, BUTTON_Y)

# Flower bag slots: 2 rows
FLOWER_Y = 26
draw_slot_row(tex, 8, FLOWER_Y, 9)
draw_slot_row(tex, 8, FLOWER_Y + 18, 9)

# Player inventory: 3 rows
INV_Y = 84
for i in range(3):
    draw_slot_row(tex, 8, INV_Y + i * 18, 9)

# Hotbar: 1 row
HOTBAR_Y = 142
draw_slot_row(tex, 8, HOTBAR_Y, 9)

# ============ SAVE ============
out = Image.fromarray(tex, 'RGBA')
out.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v3.png")
print(f"Saved texture: {out.size}")
print(f"GUI area: {GUI_W}x{GUI_H} (top-left)")

# Count unique colors
pixels = tex.reshape(-1, 4)
unique = np.unique(pixels, axis=0)
print(f"Unique colors: {len(unique)}")
for c in unique:
    print(f"  RGBA({c[0]},{c[1]},{c[2]},{c[3]})")

# 4x zoom for preview
zoom = out.resize((TEX_W*3, TEX_H*3), Image.NEAREST)
zoom.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v3_3x.png")
print("Saved 3x preview")

# Verify layout
print(f"\n=== Layout Verification ===")
print(f"Texture: {TEX_W}x{TEX_H} (standard MC GUI texture size)")
print(f"GUI panel: 0,0 to {GUI_W-1},{GUI_H-1}")
print(f"Buttons: y={BUTTON_Y}, x=[8,28,48,68,88], 14x14 each")
print(f"Flower bag row 0: y={FLOWER_Y}, slots 0-8 at x=8,26,...,152")
print(f"Flower bag row 1: y={FLOWER_Y+18}, slots 9-17")
print(f"Inv row 0: y={INV_Y}, slots 18-26")
print(f"Inv row 1: y={INV_Y+18}, slots 27-35")
print(f"Inv row 2: y={INV_Y+36}, slots 36-44")
print(f"Hotbar: y={HOTBAR_Y}, slots 45-53")
print(f"Slot size: 18x18 (interior 16x16)")
print(f"Slot pitch: 18px (exactly matches MC Slot rendering)")
