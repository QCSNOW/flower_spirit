from PIL import Image
import numpy as np

img = Image.open(r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\66984541-2e3f-4aa4-b69b-6eacc4c0528a_ef14eb16-530d-4368-8bf5-63c8dff87309_QQ_1790053414316.png")
arr = np.array(img.convert('RGBA'))
h, w = arr.shape[:2]
print(f"Image size: {w}x{h}")

# Find the GUI panel boundaries
# Look for the left edge of the GUI (white/light border)
left_edge = -1
for x in range(w):
    col = arr[:, x]
    # Find white-ish pixels (border)
    white_count = np.sum((col[:, 0] > 240) & (col[:, 1] > 240) & (col[:, 2] > 240) & (col[:, 3] > 200))
    if white_count > h * 0.5:
        left_edge = x
        break

right_edge = -1
for x in range(w-1, -1, -1):
    col = arr[:, x]
    white_count = np.sum((col[:, 0] > 240) & (col[:, 1] > 240) & (col[:, 2] > 240) & (col[:, 3] > 200))
    if white_count > h * 0.5:
        right_edge = x
        break

top_edge = -1
for y in range(h):
    row = arr[y, :]
    white_count = np.sum((row[:, 0] > 240) & (row[:, 1] > 240) & (row[:, 2] > 240) & (row[:, 3] > 200))
    if white_count > w * 0.3:
        top_edge = y
        break

bottom_edge = -1
for y in range(h-1, -1, -1):
    row = arr[y, :]
    white_count = np.sum((row[:, 0] > 240) & (row[:, 1] > 240) & (row[:, 2] > 240) & (row[:, 3] > 200))
    if white_count > w * 0.3:
        bottom_edge = y
        break

print(f"GUI boundaries: left={left_edge}, right={right_edge}, top={top_edge}, bottom={bottom_edge}")
print(f"GUI size: {right_edge - left_edge + 1} x {bottom_edge - top_edge + 1}")

# Measure slot sizes
# Find vertical positions of slot rows by looking for dark slot borders
gui_left = left_edge
gui_right = right_edge
gui_top = top_edge
gui_bottom = bottom_edge

# Find slot rows by scanning horizontally for dark borders
slot_rows = []
for y in range(gui_top, gui_bottom):
    row = arr[y, gui_left:gui_right]
    # Count dark pixels (slot borders)
    dark_count = np.sum((row[:, 0] < 60) & (row[:, 1] < 60) & (row[:, 2] < 60) & (row[:, 3] > 200))
    total = gui_right - gui_left
    if dark_count > total * 0.3:
        slot_rows.append((y, dark_count))

print(f"\nSlot border rows (y, dark_count):")
prev_y = -10
for y, dc in slot_rows:
    if y - prev_y > 3:  # group nearby rows
        print(f"  y={y} (rel y={y-gui_top}): {dc} dark pixels")
    prev_y = y

# Find slot columns similarly
print(f"\nSlot border columns (sample at mid-GUI):")
mid_y = gui_top + (gui_bottom - gui_top) // 2
slot_cols = []
# Actually, let's look at a row that has slot borders
sample_y = -1
for y, dc in slot_rows[:1]:
    sample_y = y

if sample_y > 0:
    row = arr[sample_y, gui_left:gui_right]
    in_border = False
    start_x = 0
    for x in range(len(row)):
        r, g, b, a = row[x]
        is_dark = r < 60 and g < 60 and b < 60 and a > 200
        if is_dark and not in_border:
            in_border = True
            start_x = x
        elif not is_dark and in_border:
            in_border = False
            if x - start_x <= 3:  # thin border
                slot_cols.append(gui_left + start_x)
    
    # Print first 10 slot column positions
    print(f"  Found {len(slot_cols)} border columns at sample y={sample_y}")
    for i, x in enumerate(slot_cols[:12]):
        print(f"    col {i}: x={x} (rel={x-gui_left})")
    
    # Measure slot width (distance between consecutive left borders)
    if len(slot_cols) >= 3:
        for i in range(min(5, len(slot_cols)-1)):
            dist = slot_cols[i+1] - slot_cols[i]
            print(f"  Slot {i} width (col{i+1} - col{i}): {dist}px")

# Measure item size by looking at the first row of actual items
# Items are in the player inventory area
# Let's find an item and measure it
# Look for non-gray pixels in the inventory area
inv_start_y = gui_top + 80  # approximate
for y in range(gui_top + 60, gui_bottom):
    row = arr[y, gui_left:gui_right]
    # Find colorful pixels (not gray)
    colorful = 0
    for x in range(len(row)):
        r, g, b, a = row[x]
        if a > 200 and abs(int(r)-int(g)) > 15 or abs(int(g)-int(b)) > 15:
            colorful += 1
    if colorful > 5:
        print(f"\nFirst item row approx at y={y} (rel={y-gui_top})")
        break
