"""Updated comparison sheet with refined textures."""
import numpy as np
from PIL import Image, ImageDraw
import os

SRC = r"D:\mcmod\mytestmod\temp"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
OUT = r"D:\mcmod\mytestmod\temp\comparison_refined.png"

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

MAG = 8
T = 32
CELL_W = 320
CELL_H = 300
COLS = 4
ROWS = 3

canvas = Image.new('RGB', (CELL_W * COLS, CELL_H * ROWS), (220, 220, 220))
draw = ImageDraw.Draw(canvas)

for i, (ref_name, tex_name, label) in enumerate(flowers):
    col = i % COLS
    row = i // COLS
    x0 = col * CELL_W
    y0 = row * CELL_H
    
    # Reference
    ref = Image.open(os.path.join(SRC, ref_name)).convert('RGB')
    ref = ref.resize((128, 128), Image.BILINEAR)
    canvas.paste(ref, (x0 + 16, y0 + 30))
    
    # Texture magnified on checker
    tex = Image.open(os.path.join(DST, tex_name)).convert('RGBA')
    tex_mag = tex.resize((256, 256), Image.NEAREST)
    checker = Image.new('RGB', (256, 256), (245, 245, 245))
    for cy in range(32):
        for cx in range(32):
            if (cx + cy) % 2 == 0:
                for dy in range(MAG):
                    for dx in range(MAG):
                        checker.putpixel((cx*MAG+dx, cy*MAG+dy), (225, 225, 225))
    checker.paste(tex_mag, (0, 0), tex_mag)
    canvas.paste(checker, (x0 + 160, y0 + 22))
    
    # Labels
    draw.text((x0 + 10, y0 + 5), f"{i+1}. {label}", fill=(0, 0, 0))
    
    # Stats
    tex_arr = np.array(tex)
    n_px = int(np.sum(tex_arr[:,:,3] > 0))
    colors = set()
    for y in range(32):
        for x in range(32):
            if tex_arr[y, x, 3] > 0:
                colors.add(tuple(tex_arr[y, x, :3]))
    
    # Self-check score (simple heuristic)
    # Score based on: pixel count range, color count, stem gradient presence
    score = 0
    if 150 <= n_px <= 350: score += 40
    elif 100 <= n_px <= 450: score += 25
    else: score += 10
    
    if 8 <= len(colors) <= 18: score += 30
    elif 5 <= len(colors) <= 22: score += 15
    else: score += 5
    
    # Check stem gradient
    has_grad = False
    for y in range(24, 31):
        l_g, r_g = 0, 0
        for x in range(T):
            if tex_arr[y, x, 3] > 0:
                r, g, b = int(tex_arr[y,x,0]), int(tex_arr[y,x,1]), int(tex_arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    if x < 15 and g > l_g: l_g = g
                    if x > 16 and g > r_g: r_g = g
        if l_g > 0 and r_g > 0 and abs(l_g - r_g) > 20:
            has_grad = True
    score += 30 if has_grad else 10
    
    draw.text((x0 + 16, y0 + 170), f"{n_px}px / {len(colors)}c", fill=(50, 50, 50))
    status = "PASS" if score >= 80 else "CHECK"
    color = (0, 150, 0) if score >= 80 else (200, 100, 0)
    draw.text((x0 + 16, y0 + 188), f"Score: {score}/100 [{status}]", fill=color)

canvas.save(OUT, 'PNG')
print(f"Saved to {OUT}")
