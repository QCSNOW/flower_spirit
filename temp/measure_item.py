from PIL import Image
import numpy as np

img = Image.open(r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\66984541-2e3f-4aa4-b69b-6eacc4c0528a_ef14eb16-530d-4368-8bf5-63c8dff87309_QQ_1790053414316.png")
arr = np.array(img.convert('RGBA'))
h, w = arr.shape[:2]

# Strategy: find the brown leather item in inventory and measure it precisely
# Brown leather: high red, medium green, low blue (orangey-brown)
# Find it by scanning for distinctive color

# Let's look in the upper inventory area (first row of player inv)
# Based on visual: items start around 40% from top
search_y_start = int(h * 0.45)
search_y_end = int(h * 0.55)

# Find the brown leather item (2nd item in first inv row)
# Sample at multiple y levels
for test_y in range(search_y_start, search_y_end, 5):
    # Scan for brown pixels
    brown_xs = []
    for x in range(w//4, 3*w//4):
        r, g, b, a = arr[test_y, x]
        if a > 200 and r > 100 and g > 60 and g < r*0.7 and b < r*0.4:
            brown_xs.append(x)
    
    if len(brown_xs) > 20:
        # Found a brown item
        item_left = brown_xs[0]
        item_right = brown_xs[-1]
        width = item_right - item_left + 1
        print(f"Brown item at y={test_y}: x={item_left} to {item_right}, width={width}px")
        
        # Now find the exact top and bottom of this item
        center_x = (item_left + item_right) // 2
        item_top = test_y
        item_bottom = test_y
        
        # Scan up
        for y in range(test_y, 0, -1):
            r, g, b, a = arr[y, center_x]
            if a < 50 or (r < 100 and g < 100 and b < 100):
                item_top = y + 1
                break
            item_top = y
        
        # Scan down
        for y in range(test_y, h):
            r, g, b, a = arr[y, center_x]
            if a < 50 or (r < 100 and g < 100 and b < 100):
                item_bottom = y - 1
                break
            item_bottom = y
        
        height = item_bottom - item_top + 1
        print(f"  Top: {item_top}, Bottom: {item_bottom}, Height: {height}px")
        
        # MC item = 16x16 px
        scale_w = width / 16
        scale_h = height / 16
        print(f"  Scale (from width): {scale_w:.2f}x")
        print(f"  Scale (from height): {scale_h:.2f}x")
        
        # Use the more reliable one (usually height for leather item)
        scale = (scale_w + scale_h) / 2
        print(f"  Average scale: {scale:.2f}x")
        
        # Find slot borders around this item
        # Slot left border should be to the left of item
        slot_left = -1
        for x in range(item_left - 1, 0, -1):
            r, g, b, a = arr[test_y, x]
            if r < 80 and g < 80 and b < 80 and a > 200:
                slot_left = x
                break
        
        slot_right = -1
        for x in range(item_right + 1, w):
            r, g, b, a = arr[test_y, x]
            if r < 80 and g < 80 and b < 80 and a > 200:
                slot_right = x
                break
        
        print(f"\n  Slot left border: x={slot_left}")
        print(f"  Slot right border: x={slot_right}")
        if slot_left > 0 and slot_right > 0:
            slot_w = slot_right - slot_left + 1
            print(f"  Slot width: {slot_w}px (MC: {slot_w/scale:.1f}px)")
            item_offset_left = item_left - slot_left
            print(f"  Item offset from slot left: {item_offset_left}px (MC: {item_offset_left/scale:.1f}px)")
            item_offset_right = slot_right - item_right
            print(f"  Item offset from slot right: {item_offset_right}px (MC: {item_offset_right/scale:.1f}px)")
        
        break
