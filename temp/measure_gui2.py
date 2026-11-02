from PIL import Image
import numpy as np

img = Image.open(r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\66984541-2e3f-4aa4-b69b-6eacc4c0528a_ef14eb16-530d-4368-8bf5-63c8dff87309_QQ_1790053414316.png")
arr = np.array(img.convert('RGBA'))
h, w = arr.shape[:2]

# Find a distinct item and measure its actual pixel size in the screenshot
# The sword in hotbar - it has a blade (light/white) and a handle (brown)
# Let's find it in the hotbar area (bottom row of items)

# Scan from bottom up to find the hotbar item row
hotbar_items_y = -1
for y in range(h-50, h-5, -1):
    # Look for colorful pixels in a horizontal band
    colorful_count = 0
    for x in range(w//4, 3*w//4):
        r, g, b, a = arr[y, x]
        if a > 200:
            # Check if it's not gray
            maxc = max(r, g, b)
            minc = min(r, g, b)
            if maxc - minc > 20:
                colorful_count += 1
    if colorful_count > 50:
        hotbar_items_y = y
        print(f"Hotbar item row found at y={y}, colorful_pixels={colorful_count}")
        break

if hotbar_items_y > 0:
    # Find the sword - look for a combo of white/light and brown/orange pixels
    # Scan horizontally to find item boundaries
    in_item = False
    item_start = 0
    items = []
    
    for x in range(w):
        r, g, b, a = arr[hotbar_items_y, x]
        is_item_pixel = a > 200
        if is_item_pixel and not in_item:
            in_item = True
            item_start = x
        elif not is_item_pixel and in_item:
            in_item = False
            items.append((item_start, x - 1))
    
    print(f"\nItems found in hotbar row: {len(items)}")
    for i, (s, e) in enumerate(items[:10]):
        width = e - s + 1
        print(f"  Item {i}: x={s} to {e}, width={width}px")
    
    if len(items) >= 2:
        # Slot pitch = distance between start of item i and start of item i+1
        pitch = items[1][0] - items[0][0]
        print(f"\nSlot pitch (item start to item start): {pitch}px")
        # MC slot pitch = 18px
        scale = pitch / 18
        print(f"Scale factor: {scale:.2f}x")
        
        # Item width in MC pixels
        item_width_mc = (items[0][1] - items[0][0] + 1) / scale
        print(f"Item width (MC px): ~{item_width_mc:.1f}")
        
        # GUI width in MC pixels
        # The GUI left edge is where the white border starts
        # Let's find left edge of GUI panel
        gui_left = -1
        for x in range(w):
            r, g, b, a = arr[hotbar_items_y, x]
            if a > 200 and r > 200 and g > 200 and b > 200:  # white border
                gui_left = x
                break
        
        gui_right = -1
        for x in range(w-1, -1, -1):
            r, g, b, a = arr[hotbar_items_y, x]
            if a > 200 and r > 200 and g > 200 and b > 200:
                gui_right = x
                break
        
        gui_width = gui_right - gui_left + 1
        print(f"\nGUI width (screenshot): {gui_width}px")
        print(f"GUI width (MC px): {gui_width / scale:.1f}")
        
        # Now calculate positions in MC pixels
        # First item x position (screenshot) relative to GUI left
        first_item_rel = items[0][0] - gui_left
        first_item_mc_x = first_item_rel / scale
        print(f"\nFirst item x (MC px, relative to GUI left): {first_item_mc_x:.1f}")
        print(f"  -> Slot left edge (MC px): {first_item_mc_x - 1:.1f}")
        print(f"  -> Slot interior starts at x+1 = {first_item_mc_x:.1f} (correct!)")

# Now let's find the y positions of all slot rows
# by finding horizontal dark lines (slot top/bottom borders)
print("\n=== Slot Row Y Positions ===")

# Find GUI top
gui_top = -1
for y in range(h):
    row = arr[y, :]
    white_count = np.sum((row[:, 0] > 240) & (row[:, 1] > 240) & (row[:, 2] > 240) & (row[:, 3] > 200))
    if white_count > 200:
        gui_top = y
        break

gui_bottom = -1
for y in range(h-1, -1, -1):
    row = arr[y, :]
    white_count = np.sum((row[:, 0] > 240) & (row[:, 1] > 240) & (row[:, 2] > 240) & (row[:, 3] > 200))
    if white_count > 200:
        gui_bottom = y
        break

print(f"GUI top: {gui_top}, bottom: {gui_bottom}")
print(f"GUI height (screenshot): {gui_bottom - gui_top + 1}px")

# Find all horizontal dark lines (slot borders)
# Sample from middle of GUI width
mid_x = w // 2
dark_rows = []
prev_dark = False
dark_start = 0

for y in range(gui_top, gui_bottom):
    r, g, b, a = arr[y, mid_x]
    is_dark = r < 80 and g < 80 and b < 80 and a > 200
    
    if is_dark and not prev_dark:
        dark_start = y
        prev_dark = True
    elif not is_dark and prev_dark:
        dark_rows.append((dark_start, y - 1))
        prev_dark = False

print(f"\nHorizontal dark bands (slot borders) at mid-x:")
for i, (s, e) in enumerate(dark_rows[:15]):
    print(f"  Band {i}: y={s} to {e} (height={e-s+1})")

# Calculate y positions in MC pixels
if len(items) >= 2:
    scale = (items[1][0] - items[0][0]) / 18
    
    print(f"\n=== All Positions in MC Pixels (scale={scale:.2f}x) ===")
    print(f"GUI top: {gui_top/scale:.1f}")
    print(f"GUI height: {(gui_bottom-gui_top+1)/scale:.1f}")
    
    print(f"\nSlot top borders (MC y from GUI top):")
    for i, (s, e) in enumerate(dark_rows[:12]):
        y_mc = (s - gui_top) / scale
        height_mc = (e - s + 1) / scale
        print(f"  Band {i}: y={y_mc:.1f}, height={height_mc:.1f}px")
