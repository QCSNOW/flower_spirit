from PIL import Image
import numpy as np

base = Image.open(r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\1d434076-e124-4c2c-8e76-ee165358a201_3b5ba457-6be3-484f-8f6e-e56da42288ee_flower_bag_base.png")
slots = Image.open(r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\0faf5b61-4be8-4b9f-939e-962a2815aee7_a9f36d54-656a-48fa-b93f-c9e378309d03_flower_bag_slots.png")

print(f"Base size: {base.size}, mode: {base.mode}")
print(f"Slots size: {slots.size}, mode: {slots.mode}")

# Analyze base image - find slot positions
b = np.array(base)
print(f"Base array shape: {b.shape}")

# Find slot rows in base
# Slots have dark borders (black/dark gray) and lighter interior
# Scan for horizontal slot borders
base_arr = np.array(base.convert('RGBA'))

# Print unique colors count
pixels = base_arr.reshape(-1, 4)
unique_colors = np.unique(pixels, axis=0)
print(f"Base unique colors: {len(unique_colors)}")
for c in unique_colors[:20]:
    print(f"  RGBA({c[0]},{c[1]},{c[2]},{c[3]})")

# Check slots image
slots_arr = np.array(slots.convert('RGBA'))
print(f"\nSlots array shape: {slots_arr.shape}")
pixels2 = slots_arr.reshape(-1, 4)
unique_colors2 = np.unique(pixels2, axis=0)
print(f"Slots unique colors: {len(unique_colors2)}")
for c in unique_colors2[:20]:
    print(f"  RGBA({c[0]},{c[1]},{c[2]},{c[3]})")

# Find slot positions in base - look for the slot grid pattern
# Find rows that have slot borders (dark pixels at regular intervals)
print("\n--- Base image slot analysis ---")
# Check the slot area - 4 rows of 9 slots at bottom
# Let's find the y-range of the slot area
h, w = base_arr.shape[:2]

# Find rows with slot content (non-background colors)
bg_color = base_arr[2, 2]  # assume top-left is background
print(f"Background color: {bg_color}")

# Scan rows
for y in range(0, h, 2):
    row = base_arr[y]
    non_bg = np.sum(np.any(row != bg_color, axis=1))
    if non_bg > 10:
        # Find columns where there are slot borders
        pass

# More precise: find the exact position of one slot
# Let's look at the bottom area
print(f"\nBase image height: {h}, width: {w}")
# Look at row patterns
# Minecraft slot is typically 18x18 with 1px border
# Inner is 16x16

# Find the first slot row from bottom
for y in range(h-1, -1, -1):
    row = base_arr[y]
    # Check if this row has slot borders
    dark_count = 0
    for x in range(w):
        r, g, b, a = row[x]
        if r < 80 and g < 80 and b < 80 and a > 200:
            dark_count += 1
    if dark_count > w * 0.3:
        print(f"Row {y}: dark pixels = {dark_count}")
        # Show first 30 pixels
        for x in range(min(50, w)):
            r, g, b, a = row[x]
            if a > 0:
                print(f"  [{x}] = ({r},{g},{b},{a})")
        break
