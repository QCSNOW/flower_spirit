from PIL import Image
import numpy as np

base = Image.open(r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\1d434076-e124-4c2c-8e76-ee165358a201_3b5ba457-6be3-484f-8f6e-e56da42288ee_flower_bag_base.png")
slots = Image.open(r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\0faf5b61-4be8-4b9f-939e-962a2815aee7_a9f36d54-656a-48fa-b93f-c9e378309d03_flower_bag_slots.png")

base_arr = np.array(base.convert('RGBA'))
slots_arr = np.array(slots.convert('RGBA'))

h, w = base_arr.shape[:2]

# Find exact slot positions in base image
# Look for the slot pattern - dark borders with lighter interior
# Let's find the y-coordinates of slot rows

# Find rows with dark borders (slot top/bottom edges)
border_rows = []
for y in range(h):
    row = base_arr[y]
    dark_count = 0
    for x in range(w):
        r, g, b, a = row[x]
        if r < 100 and g < 100 and b < 100 and a > 200:
            dark_count += 1
    if dark_count > w * 0.2:
        border_rows.append((y, dark_count))

print("Border rows (y, dark_pixel_count):")
for y, dc in border_rows:
    print(f"  y={y}: {dc} dark pixels")

# Find columns with slot borders
print("\nColumn analysis:")
# Sample a row in the middle of a slot
for x in range(0, w):
    col = base_arr[120, x]  # check row 120
    r, g, b, a = col
    if r < 100 and g < 100 and b < 100 and a > 200:
        pass  # this is a border column

# Let's find slot positions more carefully
# Check the slots image - it has clean pixel art slots
print(f"\nSlots image: {slots.size}")

# In the slots image, find the slot pattern
sh, sw = slots_arr.shape[:2]
# Find first non-transparent row
first_row = -1
for y in range(sh):
    if np.any(slots_arr[y, :, 3] > 0):
        first_row = y
        break
print(f"First non-transparent row in slots: {first_row}")

# Find slot dimensions in slots image
# The slot should be 18x18 (1px border + 16px interior + 1px border)
# Let's measure
slot_top = first_row
# Find the bottom of first slot row
slot_bottom = -1
for y in range(slot_top + 1, sh):
    # Check if this is a horizontal separator (mostly dark)
    row = slots_arr[y]
    dark_count = np.sum((row[:, 0] < 80) & (row[:, 3] > 200))
    total_visible = np.sum(row[:, 3] > 200)
    if total_visible > 0 and dark_count / total_visible > 0.8:
        slot_bottom = y
        break

print(f"Slot top={slot_top}, bottom={slot_bottom}, height={slot_bottom - slot_top + 1 if slot_bottom > 0 else '?'}")

# Find slot width
slot_left = -1
slot_right = -1
for x in range(sw):
    col = slots_arr[slot_top + 2, x]  # middle of slot
    if col[3] > 200 and slot_left == -1:
        slot_left = x
    if col[3] == 0 and slot_left > -1 and slot_right == -1:
        slot_right = x
        break

print(f"Slot left={slot_left}, right={slot_right}, width={slot_right - slot_left if slot_right > 0 else '?'}")

# Print first few rows of slots image pixel by pixel to understand the pattern
print("\nFirst 20 rows, first 30 cols of slots image:")
for y in range(min(25, sh)):
    line = f"y={y:2d}: "
    for x in range(min(30, sw)):
        r, g, b, a = slots_arr[y, x]
        if a == 0:
            line += "."
        elif r < 100:
            line += "#"
        elif r > 200:
            line += "W"
        else:
            line += "G"
    print(line)
