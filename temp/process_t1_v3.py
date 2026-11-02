"""Process dancing_lady and chamomile - crop flower head only, draw stem manually."""
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, r"D:\mcmod\mytestmod\temp")
from process_v3 import boost_saturation, flood_fill_background, fill_holes, crop_to_content, quantize_colors, cleanup_pixels

TARGET = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

# Color palette for manual stem
STEM_MID = (100, 155, 12)
STEM_DARK = (73, 125, 7)
STEM_LIGHT = (130, 175, 40)

def add_manual_stem(arr, stem_x=15, stem_top=22, stem_bot=31, width=2):
    """Add a green stem to the bottom of the texture."""
    for y in range(stem_top, stem_bot + 1):
        for dx in range(-width, width + 1):
            x = stem_x + dx
            if 0 <= x < 32:
                if dx == 0:
                    arr[y, x] = [STEM_MID[0], STEM_MID[1], STEM_MID[2], 255]
                elif abs(dx) == 1:
                    arr[y, x] = [STEM_LIGHT[0], STEM_LIGHT[1], STEM_LIGHT[2], 255]
                elif abs(dx) == 2:
                    arr[y, x] = [STEM_DARK[0], STEM_DARK[1], STEM_DARK[2], 255]
    # Add two small leaves
    for y, x in [(25, 12), (25, 13), (26, 11), (26, 12), (28, 18), (28, 19), (29, 17), (29, 18)]:
        if 0 <= x < 32 and 0 <= y < 32:
            arr[y, x] = [STEM_MID[0], STEM_MID[1], STEM_MID[2], 255]
    return arr

def process_flower_head_only(name, src_path, dst_path, flower_ratio=0.55, fill=1.0):
    """Process only the flower head, manually add stem."""
    img = Image.open(src_path).convert('RGBA')
    arr = np.array(img).astype(np.uint8)
    
    # Remove background
    bg_mask = flood_fill_background(arr)
    arr[bg_mask, 3] = 0
    img = Image.fromarray(arr, 'RGBA')
    
    # Crop to content
    img = crop_to_content(img, 0.02)
    w, h = img.size
    print(f"  {name} after crop: {w}x{h}")
    
    # Take only top portion (flower head)
    fh = int(h * flower_ratio)
    flower_img = img.crop((0, 0, w, fh))
    flower_img = crop_to_content(flower_img, 0.02)
    fw2, fh2 = flower_img.size
    print(f"  {name} flower head: {fw2}x{fh2}")
    
    # Resize flower to fill ~20px height, centered
    scale = min(22 / fw2, 20 / fh2) * fill
    new_w = max(1, int(fw2 * scale))
    new_h = max(1, int(fh2 * scale))
    flower_resized = flower_img.resize((new_w, new_h), Image.LANCZOS)
    
    # Create canvas
    canvas = Image.new('RGBA', (TARGET, TARGET), (0, 0, 0, 0))
    ox = (TARGET - new_w) // 2
    oy = 1
    canvas.paste(flower_resized, (ox, oy), flower_resized)
    
    # Boost saturation
    canvas = boost_saturation(canvas)
    
    # Fill holes
    alpha = np.array(canvas)[:, :, 3]
    alpha_filled = fill_holes(alpha)
    arr_c = np.array(canvas)
    arr_c[:, :, 3] = alpha_filled
    canvas = Image.fromarray(arr_c, 'RGBA')
    
    # Quantize
    canvas = quantize_colors(canvas, 10)
    
    # Cleanup
    canvas = cleanup_pixels(canvas)
    
    # Clean black artifacts
    arr_f = np.array(canvas)
    for y in range(TARGET):
        for x in range(TARGET):
            r, g, b, a = arr_f[y, x]
            if a > 0 and r == 0 and g == 0 and b == 0:
                arr_f[y, x, 3] = 0
    
    # Add manual stem
    arr_f = add_manual_stem(arr_f)
    
    canvas = Image.fromarray(arr_f, 'RGBA')
    canvas.save(dst_path, 'PNG')
    
    n = int(np.sum(arr_f[:,:,3] > 0))
    colors = set()
    for y in range(TARGET):
        for x in range(TARGET):
            if arr_f[y, x, 3] > 0:
                colors.add(tuple(arr_f[y, x, :3]))
    print(f"  {name} result: {n} pixels, {len(colors)} colors")
    return n

# Dancing lady - arching spray of yellow flowers
print("Processing dancing_lady...")
process_flower_head_only('dancing_lady', 
    r'D:\mcmod\mytestmod\temp\dancing_lady_bop.jpg',
    f'{DST}\\dancing_lady.png',
    flower_ratio=0.65, fill=1.0)

# Chamomile - daisy with stem
print("\nProcessing chamomile...")
process_flower_head_only('chamomile',
    r'D:\mcmod\mytestmod\temp\chamomile_bop.jpg',
    f'{DST}\\chamomile.png',
    flower_ratio=0.35, fill=1.0)

# Oncidium - reprocess with flower head only
print("\nProcessing oncidium...")
process_flower_head_only('oncidium',
    r'D:\mcmod\mytestmod\temp\oncidium_bop.jpg',
    f'{DST}\\oncidium.png',
    flower_ratio=0.55, fill=1.0)
