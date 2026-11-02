"""Process dancing_lady and chamomile with separate flower/stem handling."""
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, r"D:\mcmod\mytestmod\temp")
from process_v3 import boost_saturation, flood_fill_background, fill_holes, crop_to_content, quantize_colors, cleanup_pixels

TARGET = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

def process_vertical_flower(name, src_path, dst_path, flower_ratio=0.5, fill=1.0):
    """Process a vertical flower image by splitting flower head and stem."""
    img = Image.open(src_path).convert('RGBA')
    arr = np.array(img).astype(np.uint8)
    
    # Remove background
    bg_mask = flood_fill_background(arr)
    arr[bg_mask, 3] = 0
    img = Image.fromarray(arr, 'RGBA')
    
    # Crop
    img = crop_to_content(img, 0.02)
    w, h = img.size
    print(f"  {name} after crop: {w}x{h}")
    
    # Split into flower (top) and stem (bottom)
    flower_h = int(h * flower_ratio)
    flower_img = img.crop((0, 0, w, flower_h))
    stem_img = img.crop((0, flower_h, w, h))
    
    fw, fh = flower_img.size
    sw, sh = stem_img.size
    
    # Resize flower to fill ~20px height
    flower_scale = min(20 / fw, 20 / fh) * fill
    new_fw = max(1, int(fw * flower_scale))
    new_fh = max(1, int(fh * flower_scale))
    flower_resized = flower_img.resize((new_fw, new_fh), Image.LANCZOS)
    
    # Resize stem to fill ~10px height
    stem_scale = min(10 / sw, 12 / sh) * 0.7
    new_sw = max(1, int(sw * stem_scale))
    new_sh = max(1, int(sh * stem_scale))
    stem_resized = stem_img.resize((new_sw, new_sh), Image.LANCZOS)
    
    # Combine on canvas
    canvas = Image.new('RGBA', (TARGET, TARGET), (0, 0, 0, 0))
    
    # Flower at top center
    ox_f = (TARGET - new_fw) // 2
    oy_f = 1
    canvas.paste(flower_resized, (ox_f, oy_f), flower_resized)
    
    # Stem below
    ox_s = (TARGET - new_sw) // 2
    oy_s = 20
    canvas.paste(stem_resized, (ox_s, oy_s), stem_resized)
    
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
    canvas = Image.fromarray(arr_f, 'RGBA')
    
    canvas.save(dst_path, 'PNG')
    
    varr = np.array(canvas)
    n = int(np.sum(varr[:,:,3] > 0))
    colors = set()
    for y in range(TARGET):
        for x in range(TARGET):
            if varr[y, x, 3] > 0:
                colors.add(tuple(varr[y, x, :3]))
    
    print(f"  {name} result: {n} pixels, {len(colors)} colors")
    
    # Add manual stem if too sparse
    arr_m = np.array(canvas)
    stem_added = 0
    for y in range(22, 32):
        for x in range(14, 18):
            if arr_m[y, x, 3] == 0:
                if x == 15 or x == 16:
                    arr_m[y, x] = [100, 155, 12, 255]
                    stem_added += 1
                elif x == 14 or x == 17:
                    arr_m[y, x] = [73, 125, 7, 255]
                    stem_added += 1
    
    if stem_added > 0:
        canvas = Image.fromarray(arr_m, 'RGBA')
        canvas.save(dst_path, 'PNG')
        n_final = int(np.sum(arr_m[:,:,3] > 0))
        print(f"  {name} after stem fill: {n_final} pixels (+{stem_added} stem)")
    
    return n

# Dancing lady - arching spray of yellow flowers
n1 = process_vertical_flower('dancing_lady', 
    r'D:\mcmod\mytestmod\temp\dancing_lady_bop.jpg',
    f'{DST}\\dancing_lady.png',
    flower_ratio=0.6, fill=1.0)

# Chamomile - daisy with stem  
n2 = process_vertical_flower('chamomile',
    r'D:\mcmod\mytestmod\temp\chamomile_bop.jpg',
    f'{DST}\\chamomile.png',
    flower_ratio=0.4, fill=1.0)
