from PIL import Image
import numpy as np

img = Image.open(r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\66984541-2e3f-4aa4-b69b-6eacc4c0528a_ef14eb16-530d-4368-8bf5-63c8dff87309_QQ_1790053414316.png")
arr = np.array(img.convert('RGBA'))
h, w = arr.shape[:2]

# Find GUI left edge more precisely (the inner panel edge, not outer white border)
# The GUI has: outer white border -> dark bevel -> gray panel
# Let's find consecutive columns with different brightness profiles

# Scan from left to find the GUI panel structure
left_positions = []
prev_state = "outside"
current_run = 0
for x in range(w // 3):  # only scan left third
    col = arr[h//4, x]  # sample at 1/4 height
    r, g, b, a = col
    brightness = (r + g + b) / 3
    
    if a < 50:
        state = "transparent"
    elif brightness > 240:
        state = "white_border"
    elif brightness < 60:
        state = "dark_bevel"
    elif brightness < 150:
        state = "slot_interior"
    else:
        state = "gray_panel"
    
    if state != prev_state:
        left_positions.append((x, state, brightness))
        prev_state = state
        if len(left_positions) > 20:
            break

print("Left edge structure (x, state, brightness):")
for x, s, b in left_positions:
    print(f"  x={x}: {s} (brightness={b:.0f})")

# Now, let's find the actual slot size by measuring items
# Items in MC are 16x16 pixels (before GUI scaling)
# In the screenshot, find a known item and measure its size
# Let's look at the pink wool item in the first inventory slot

# Find the first inventory row (where items appear)
# From the screenshot, items are in the lower portion
# Let's find the pink item (pink wool) - high red, medium blue, low green
for y in range(h//2, h):
    for x in range(w//4, w//2):
        r, g, b, a = arr[y, x]
        if a > 200 and r > 200 and g < 180 and b > 180:  # pink-ish
            # Found pink item, measure its size
            # Scan right to find width
            x_right = x
            while x_right < w and arr[y, x_right, 3] > 200:
                x_right += 1
            # Scan down to find height
            y_bottom = y
            while y_bottom < h and arr[y_bottom, x, 3] > 200:
                y_bottom += 1
            print(f"\nPink item top-left approx at ({x}, {y})")
            print(f"  Rough width at row {y}: ~{x_right - x}px")
            print(f"  Rough height at col {x}: ~{y_bottom - y}px")
            break
    else:
        continue
    break

# Better approach: count slot columns in the hotbar area
# Hotbar has 9 slots. Find the hotbar row and measure.
# Hotbar is at the bottom of GUI
print("\n--- Measuring hotbar slots ---")

# Find bottom of GUI
gui_bottom_row = -1
for y in range(h-1, h//2, -1):
    row = arr[y, :]
    white_count = np.sum((row[:, 0] > 240) & (row[:, 1] > 240) & (row[:, 2] > 240) & (row[:, 3] > 200))
    if white_count > w * 0.3:
        gui_bottom_row = y
        break

print(f"GUI bottom row: {gui_bottom_row}")

# Look for horizontal slot borders near the bottom
hotbar_area_top = gui_bottom_row - 80
hotbar_border_rows = []
for y in range(gui_bottom_row - 100, gui_bottom_row):
    row = arr[y, :]
    dark_count = np.sum((row[:, 0] < 60) & (row[:, 1] < 60) & (row[:, 2] < 60) & (row[:, 3] > 200))
    if dark_count > 200:
        hotbar_border_rows.append((y, dark_count))

print(f"Hotbar area border rows: {hotbar_border_rows}")

# Measure slot width from a hotbar border row
if hotbar_border_rows:
    sample_y = hotbar_border_rows[0][0]
    row = arr[sample_y, :]
    # Find dark border segments
    segments = []
    in_seg = False
    seg_start = 0
    for x in range(w):
        r, g, b, a = row[x]
        is_dark = r < 60 and g < 60 and b < 60 and a > 200
        if is_dark and not in_seg:
            in_seg = True
            seg_start = x
        elif not is_dark and in_seg:
            in_seg = False
            segments.append((seg_start, x - 1))
    
    print(f"\nDark border segments at y={sample_y}: {len(segments)} segments")
    for i, (s, e) in enumerate(segments[:12]):
        print(f"  seg {i}: x={s} to {e} (width={e-s+1})")
    
    # Calculate slot pitch = distance between start of one left border and start of next left border
    if len(segments) >= 18:  # 9 slots have 10 vertical lines? No, vertical lines are per slot side
        # Actually vertical segments at this y position are the left and right borders of slots
        # For 9 slots, there should be 10 vertical lines (left of slot 0, between slots, right of last slot)
        # But we're scanning horizontally so we see vertical border segments
        # Each vertical border appears as a short horizontal segment in our row scan
        
        # Let's just take first 10 segments and measure pitch
        vert_lines = [s for s, e in segments[:20]]  # start x of each vertical border
        print(f"\nVertical border X positions (first 12): {vert_lines[:12]}")
        if len(vert_lines) >= 10:
            pitches = [vert_lines[i+1] - vert_lines[i] for i in range(9)]
            print(f"Slot pitches: {pitches}")
            avg_pitch = sum(pitches) / len(pitches)
            print(f"Average slot pitch: {avg_pitch:.1f}px")
            
            # MC slot = 18px, so scale factor = avg_pitch / 18
            scale = avg_pitch / 18
            print(f"GUI scale factor: {scale:.2f}x")
            
            # GUI width in MC pixels
            gui_left_mc = vert_lines[0] / scale
            gui_right_mc = vert_lines[9] / scale  # 10th line is right of 9th slot
            print(f"First slot left edge (MC px): ~{gui_left_mc:.1f}")
            print(f"Last slot right edge (MC px): ~{gui_right_mc:.1f}")
