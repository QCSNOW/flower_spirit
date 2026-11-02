"""Process aster v3 - separately handle flower head and stem."""
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, r"D:\mcmod\mytestmod\temp")
from process_v3 import process_flower, boost_saturation, flood_fill_background, fill_holes, crop_to_content, quantize_colors, cleanup_pixels

SRC = r"D:\mcmod\mytestmod\temp\aster_v3.jpg"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\aster.png"
TARGET_SIZE = 32

# Step 1: Load and remove background
img = Image.open(SRC).convert('RGBA')
arr = np.array(img).astype(np.uint8)
bg_mask = flood_fill_background(arr)
arr[bg_mask, 3] = 0
img = Image.fromarray(arr, 'RGBA')

# Step 2: Crop to content
img = crop_to_content(img, 0.02)
w, h = img.size
print(f"After crop: {w}x{h}")

# Step 3: The image is tall. We want flower head at top, stem at bottom.
# Crop the flower head (top 45% of image) and resize separately
flower_h = int(h * 0.45)
flower_img = img.crop((0, 0, w, flower_h))
stem_img = img.crop((0, flower_h, w, h))

# Process flower head - resize to fill top 20px of 32x32 canvas
fw, fh = flower_img.size
flower_scale = min(20 / fw, 20 / fh) * 1.0
new_fw = max(1, int(fw * flower_scale))
new_fh = max(1, int(fh * flower_scale))
flower_resized = flower_img.resize((new_fw, new_fh), Image.LANCZOS)

# Process stem - resize to bottom 10px
sw, sh = stem_img.size
stem_scale = min(10 / sw, 12 / sh) * 0.8
new_sw = max(1, int(sw * stem_scale))
new_sh = max(1, int(sh * stem_scale))
stem_resized = stem_img.resize((new_sw, new_sh), Image.LANCZOS)

# Combine on 32x32 canvas
canvas = Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))
# Place flower centered horizontally, at top
ox_flower = (TARGET_SIZE - new_fw) // 2
oy_flower = 1
canvas.paste(flower_resized, (ox_flower, oy_flower), flower_resized)

# Place stem centered, below flower
ox_stem = (TARGET_SIZE - new_sw) // 2
oy_stem = 20
canvas.paste(stem_resized, (ox_stem, oy_stem), stem_resized)

# Boost saturation
canvas = boost_saturation(canvas)

# Fill holes
alpha = np.array(canvas)[:, :, 3]
alpha_filled = fill_holes(alpha)
arr = np.array(canvas)
arr[:, :, 3] = alpha_filled
canvas = Image.fromarray(arr, 'RGBA')

# Quantize
canvas = quantize_colors(canvas, 10)

# Cleanup
canvas = cleanup_pixels(canvas)

# Manual stem enhancement - ensure stem is visible and green
arr = np.array(canvas)
# Add green stem pixels if stem area is too sparse
stem_green = (100, 155, 12)
stem_dark = (73, 125, 7)
for y in range(21, 32):
    for x in range(14, 18):
        if arr[y, x, 3] == 0:
            # Fill in stem
            if x == 15 or x == 16:
                arr[y, x, 0] = stem_green[0]
                arr[y, x, 1] = stem_green[1]
                arr[y, x, 2] = stem_green[2]
                arr[y, x, 3] = 255
            elif x == 14 or x == 17:
                arr[y, x, 0] = stem_dark[0]
                arr[y, x, 1] = stem_dark[1]
                arr[y, x, 2] = stem_dark[2]
                arr[y, x, 3] = 255

canvas = Image.fromarray(arr, 'RGBA')
canvas.save(DST, 'PNG')

# Verify
varr = np.array(canvas)
n_vis = int(np.sum(varr[:, :, 3] > 0))
n_colors = len(set(tuple(varr[y, x, :3]) for y in range(32) for x in range(32) if varr[y, x, 3] > 0))
print(f"Result: {n_vis} pixels, {n_colors} colors")
