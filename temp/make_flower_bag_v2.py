"""Create precise flower bag GUI texture: 176x166, MC style.
Layout (pixel-perfect matching slot positions):
- Button area top: 5 buttons at y=6, x=8,28,48,68,88
- Flower bag slots: 2 rows x 9 cols, starting y=26
- Player inventory: 3 rows x 9 cols, starting y=84
- Hotbar: 1 row x 9 cols, starting y=142

IMPORTANT: Slots in the texture must align exactly with the slot positions
in ScreenHandler (Slot is drawn with its top-left at the given x,y).
Slot visual size: 18x18 (border + interior)
The item renders at slot_x+1, slot_y+1 (16x16 item inside 18x18 slot).
"""
import numpy as np
from PIL import Image

W, H = 176, 166

# MC GUI color palette
BG = (198, 198, 198, 255)        # main background gray
BORDER_DARK = (55, 55, 55, 255)   # dark border (top-left of raised, bottom-right of recessed)
BORDER_LIGHT = (255, 255, 255, 255) # light border (bottom-right of raised, top-left of recessed)
BORDER_MID = (139, 139, 139, 255)  # mid gray
SLOT_BG = (139, 139, 139, 255)    # slot interior gray
TRANSPARENT = (0, 0, 0, 0)

def px(arr, y, x, color):
    if 0 <= y < H and 0 <= x < W:
        arr[y, x] = color

def draw_gui_background(arr, x, y, w, h):
    """Standard MC GUI background panel with beveled border."""
    # Fill background
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(arr, yy, xx, BG)
    # Outer border: top/left = light, bottom/right = dark
    for xx in range(x, x + w):
        px(arr, y, xx, BORDER_LIGHT)          # top light
        px(arr, y + h - 1, xx, BORDER_DARK)    # bottom dark
    for yy in range(y, y + h):
        px(arr, yy, x, BORDER_LIGHT)           # left light
        px(arr, yy, x + w - 1, BORDER_DARK)    # right dark
    # Inner bevel: just inside the light border
    for xx in range(x + 1, x + w - 1):
        px(arr, y + 1, xx, BORDER_MID)
    for yy in range(y + 1, y + h - 1):
        px(arr, yy, x + 1, BORDER_MID)
    # Inner bevel: just inside the dark border
    for xx in range(x + 1, x + w - 1):
        px(arr, y + h - 2, xx, BORDER_MID)
    for yy in range(y + 1, y + h - 1):
        px(arr, yy, x + w - 2, BORDER_MID)


def draw_slot(arr, x, y):
    """Draw a single 18x18 recessed item slot.
    This is the standard MC item slot:
    - 1px dark top/left border (recessed shadow)
    - 1px light bottom/right border (recessed highlight)
    - 16x16 gray interior
    - 1 extra dark pixel at bottom-right interior corner
    """
    # Interior (16x16)
    for yy in range(y + 1, y + 17):
        for xx in range(x + 1, x + 17):
            px(arr, yy, xx, SLOT_BG)
    # Top border (dark)
    for xx in range(x, x + 18):
        px(arr, y, xx, BORDER_DARK)
    # Left border (dark)
    for yy in range(y, y + 18):
        px(arr, yy, x, BORDER_DARK)
    # Bottom border (light)
    for xx in range(x, x + 18):
        px(arr, y + 17, xx, BORDER_LIGHT)
    # Right border (light)
    for yy in range(y, y + 18):
        px(arr, yy, x + 17, BORDER_LIGHT)
    # Bottom-right interior corner - extra dark pixel for depth
    px(arr, y + 16, x + 16, BORDER_DARK)


def draw_slot_row(arr, start_x, y, count=9):
    for i in range(count):
        draw_slot(arr, start_x + i * 18, y)


# ============ CREATE CANVAS ============
gui = np.zeros((H, W, 4), dtype=np.uint8)

# Main background panel (full 176x166)
draw_gui_background(gui, 0, 0, W, H)

# ============ SLOT LAYOUT ============
# Standard MC slot positions for 176-wide GUI:
# First slot x = 8, each slot 18px apart, 9 slots = 8 + 8*18 + 18 = 8 + 144 + 18 = 170. Last slot ends at x=170.
# Right margin: 176 - 170 = 6px. Actually standard is 7px right margin.
# Let me recalculate: 9 slots * 18 = 162. 176 - 162 = 14 total margin = 7 left + 7 right.
# But vanilla uses x=8, so left margin 8, right margin 176-(8+162)=6. Close enough.

SLOT_X = 8  # Standard MC first slot x

# Flower bag slots: 2 rows at top
# Place them below the button area
# Buttons are at y=6 (14px tall), so flower slots start at y=26 (button bottom + gap)
FLOWER_TOP_Y = 26
draw_slot_row(gui, SLOT_X, FLOWER_TOP_Y, 9)       # row 0
draw_slot_row(gui, SLOT_X, FLOWER_TOP_Y + 18, 9)  # row 1

# Player inventory: 3 rows
# Standard: y = 84
INV_TOP_Y = 84
for i in range(3):
    draw_slot_row(gui, SLOT_X, INV_TOP_Y + i * 18, 9)

# Hotbar: 1 row
# Standard: y = 142 (84 + 54 + 4 = 142)
HOTBAR_Y = 142
draw_slot_row(gui, SLOT_X, HOTBAR_Y, 9)

# ============ BUTTON AREA ============
# 5 recessed button slots at top (dark background, beveled)
# Buttons are 14x14, at y=6
# Positions: x=8, 28, 48, 68, 88 (20px spacing)
BUTTON_Y = 6
BUTTON_SIZE = 14
button_xs = [8, 28, 48, 68, 88]

for bx in button_xs:
    # Button recessed background (darker than main bg)
    for yy in range(BUTTON_Y + 1, BUTTON_Y + BUTTON_SIZE - 1):
        for xx in range(bx + 1, bx + BUTTON_SIZE - 1):
            px(gui, yy, xx, (85, 85, 85, 255))
    # Dark top/left border (recessed)
    for xx in range(bx, bx + BUTTON_SIZE):
        px(gui, BUTTON_Y, xx, BORDER_DARK)
    for yy in range(BUTTON_Y, BUTTON_Y + BUTTON_SIZE):
        px(gui, yy, bx, BORDER_DARK)
    # Light bottom/right border (recessed)
    for xx in range(bx, bx + BUTTON_SIZE):
        px(gui, BUTTON_Y + BUTTON_SIZE - 1, xx, BORDER_LIGHT)
    for yy in range(BUTTON_Y, BUTTON_Y + BUTTON_SIZE):
        px(gui, yy, bx + BUTTON_SIZE - 1, BORDER_LIGHT)
    # Bottom-right interior corner dark pixel
    px(gui, BUTTON_Y + BUTTON_SIZE - 2, bx + BUTTON_SIZE - 2, BORDER_DARK)

# ============ SAVE ============
out = Image.fromarray(gui, 'RGBA')
out.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v2.png")
print(f"Saved: {out.size}")

# Count unique colors
pixels = gui.reshape(-1, 4)
unique = np.unique(pixels, axis=0)
print(f"Unique colors: {len(unique)}")

# Verify slot positions
print(f"\nSlot layout verification:")
print(f"  Flower bag row 0: y={FLOWER_TOP_Y} (slots 0-8)")
print(f"  Flower bag row 1: y={FLOWER_TOP_Y+18} (slots 9-17)")
print(f"  Player inv row 0: y={INV_TOP_Y} (slots 18-26)")
print(f"  Player inv row 1: y={INV_TOP_Y+18} (slots 27-35)")
print(f"  Player inv row 2: y={INV_TOP_Y+36} (slots 36-44)")
print(f"  Hotbar: y={HOTBAR_Y} (slots 45-53)")
print(f"  Buttons: y={BUTTON_Y}, sizes 14x14 at x={button_xs}")

# 4x zoom preview
zoom = out.resize((W*4, H*4), Image.NEAREST)
zoom.save(r"D:\mcmod\mytestmod\temp\flower_bag_gui_v2_4x.png")
print("Saved 4x preview")
