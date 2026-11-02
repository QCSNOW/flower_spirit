"""Create a comparison sheet: AI reference vs 32x32 MC texture (magnified)."""
import numpy as np
from PIL import Image
import os

SRC = r"D:\mcmod\mytestmod\temp"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
OUT = r"D:\mcmod\mytestmod\temp\comparison_v2.png"

flowers = [
    ("ref_waxflower.jpg", "waxflower.png", "Waxflower"),
    ("ref_aster.jpg", "aster.png", "Aster"),
    ("ref_dancing_lady.jpg", "dancing_lady.png", "Dancing Lady"),
    ("ref_chamomile.jpg", "chamomile.png", "Chamomile"),
    ("ref_oncidium.jpg", "oncidium.png", "Oncidium"),
    ("ref_anemone.jpg", "anemone.png", "Anemone"),
    ("ref_astilbe.jpg", "astilbe.png", "Astilbe"),
    ("ref_hydrangea.jpg", "hydrangea.png", "Hydrangea"),
    ("ref_bells_of_ireland.jpg", "bells_of_ireland.png", "Bells of Ireland"),
    ("ref_hypericum.jpg", "hypericum.png", "Hypericum"),
    ("ref_lupine.jpg", "lupine.png", "Lupine"),
    ("ref_wintersweet.jpg", "wintersweet.png", "Wintersweet"),
]

MAG = 8  # magnify 32x32 to 256x256
CELL_W = 300
CELL_H = 320
COLS = 4
ROWS = 3

canvas = Image.new('RGB', (CELL_W * COLS, CELL_H * ROWS), (200, 200, 200))

for i, (ref_name, tex_name, label) in enumerate(flowers):
    col = i % COLS
    row = i // COLS
    x0 = col * CELL_W
    y0 = row * CELL_H
    
    # Load reference (small preview)
    ref = Image.open(os.path.join(SRC, ref_name)).convert('RGB')
    ref = ref.resize((128, 128), Image.BILINEAR)
    canvas.paste(ref, (x0 + 10, y0 + 30))
    
    # Load texture (magnified)
    tex = Image.open(os.path.join(DST, tex_name)).convert('RGBA')
    tex_mag = tex.resize((32 * MAG, 32 * MAG), Image.NEAREST)
    # Put on checker bg
    checker = Image.new('RGB', (32*MAG, 32*MAG), (240, 240, 240))
    for cy in range(32):
        for cx in range(32):
            if (cx + cy) % 2 == 0:
                for dy in range(MAG):
                    for dx in range(MAG):
                        checker.putpixel((cx*MAG+dx, cy*MAG+dy), (220, 220, 220))
    checker.paste(tex_mag, (0, 0), tex_mag)
    canvas.paste(checker, (x0 + 150, y0 + 30))
    
    # Label
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(canvas)
    draw.text((x0 + 10, y0 + 5), f"{i+1}. {label}", fill=(0, 0, 0))
    draw.text((x0 + 10, y0 + 165), "AI Ref", fill=(80, 80, 80))
    draw.text((x0 + 150, y0 + 165), "MC 32x32", fill=(80, 80, 80))
    
    # Stats
    tex_arr = np.array(tex)
    n_px = int(np.sum(tex_arr[:,:,3] > 0))
    colors = set()
    for y in range(32):
        for x in range(32):
            if tex_arr[y, x, 3] > 0:
                colors.add(tuple(tex_arr[y, x, :3]))
    draw.text((x0 + 10, y0 + 185), f"Pixels: {n_px}", fill=(60, 60, 60))
    draw.text((x0 + 10, y0 + 200), f"Colors: {len(colors)}", fill=(60, 60, 60))

canvas.save(OUT, 'PNG')
print(f"Comparison sheet saved to {OUT}")
