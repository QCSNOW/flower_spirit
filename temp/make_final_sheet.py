"""Final deliverable: generate clean comparison sheet with scores."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

SRC = r"D:\mcmod\mytestmod\temp"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
OUT = r"D:\mcmod\mytestmod\temp\final_deliverable.png"
T = 32

flowers = [
    ("ref_waxflower.jpg", "waxflower.png", "蜡花 Waxflower"),
    ("ref_aster.jpg", "aster.png", "紫苑 Aster"),
    ("ref_dancing_lady.jpg", "dancing_lady.png", "跳舞兰 Dancing Lady"),
    ("ref_chamomile.jpg", "chamomile.png", "洋甘菊 Chamomile"),
    ("ref_oncidium.jpg", "oncidium.png", "文心兰 Oncidium"),
    ("ref_anemone.jpg", "anemone.png", "银莲花 Anemone"),
    ("ref_astilbe.jpg", "astilbe.png", "落新妇 Astilbe"),
    ("ref_hydrangea.jpg", "hydrangea.png", "绣球 Hydrangea"),
    ("ref_bells_of_ireland.jpg", "bells_of_ireland.png", "贝壳花 Bells of Ireland"),
    ("ref_hypericum.jpg", "hypericum.png", "火龙珠 Hypericum"),
    ("ref_lupine.jpg", "lupine.png", "鲁冰花 Lupine"),
    ("ref_wintersweet.jpg", "wintersweet.png", "腊梅 Wintersweet"),
]

MAG = 10  # 32*10 = 320px
CELL_W = 360
CELL_H = 380
COLS = 4
ROWS = 3

W = CELL_W * COLS
H = CELL_H * ROWS + 60  # extra space for header

canvas = Image.new('RGB', (W, H), (230, 230, 230))
draw = ImageDraw.Draw(canvas)

# Header
draw.text((20, 15), "12 Flowers - AI Reference vs MC Pixel Texture (32x32)", fill=(0, 0, 0))
draw.text((20, 35), "Generated from AI reference images, pixel-by-pixel redrawn for clean MC style", fill=(80, 80, 80))

for i, (ref_name, tex_name, label) in enumerate(flowers):
    col = i % COLS
    row = i // COLS
    x0 = col * CELL_W
    y0 = row * CELL_H + 60
    
    # Label
    draw.text((x0 + 10, y0 + 5), f"{i+1}. {label}", fill=(0, 0, 0))
    
    # AI Reference (resized to 128x128)
    ref = Image.open(os.path.join(SRC, ref_name)).convert('RGB')
    ref = ref.resize((128, 128), Image.BILINEAR)
    # White border
    draw.rectangle([x0 + 14, y0 + 29, x0 + 145, y0 + 160], outline=(180, 180, 180))
    canvas.paste(ref, (x0 + 15, y0 + 30))
    draw.text((x0 + 15, y0 + 165), "AI Reference", fill=(100, 100, 100))
    
    # MC Texture (magnified 10x on checkerboard)
    tex = Image.open(os.path.join(DST, tex_name)).convert('RGBA')
    tex_mag = tex.resize((32 * MAG, 32 * MAG), Image.NEAREST)
    
    # Checker background
    checker = Image.new('RGB', (32*MAG, 32*MAG), (248, 248, 248))
    for cy in range(32):
        for cx in range(32):
            if (cx + cy) % 2 == 0:
                for dy in range(MAG):
                    for dx in range(MAG):
                        checker.putpixel((cx*MAG+dx, cy*MAG+dy), (228, 228, 228))
    checker.paste(tex_mag, (0, 0), tex_mag)
    
    draw.rectangle([x0 + 164, y0 + 29, x0 + 165 + 32*MAG, y0 + 30 + 32*MAG], outline=(180, 180, 180))
    canvas.paste(checker, (x0 + 165, y0 + 30))
    draw.text((x0 + 165, y0 + 32 + 32*MAG), "MC 32x32 (10x zoom)", fill=(100, 100, 100))
    
    # Stats below
    tex_arr = np.array(tex)
    n_px = int(np.sum(tex_arr[:,:,3] > 0))
    n_c = len(set(tuple(tex_arr[y,x,:3]) for y in range(T) for x in range(T) if tex_arr[y,x,3] > 0))
    
    # Check stem gradient
    has_grad = False
    for y in range(26, 31):
        greens = []
        for x in range(T):
            if tex_arr[y, x, 3] > 0:
                r, g, b = int(tex_arr[y,x,0]), int(tex_arr[y,x,1]), int(tex_arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    greens.append((x, g))
        if len(greens) >= 3:
            greens.sort()
            if greens[0][1] > greens[-1][1] + 15:
                has_grad = True
    
    stat_y = y0 + 32*MAG + 55
    draw.text((x0 + 15, stat_y), f"Pixels: {n_px}", fill=(50, 50, 50))
    draw.text((x0 + 15, stat_y + 15), f"Colors: {n_c}", fill=(50, 50, 50))
    grad_text = "Stem Gradient: YES" if has_grad else "Stem Gradient: -"
    grad_color = (0, 130, 0) if has_grad else (150, 100, 0)
    draw.text((x0 + 15, stat_y + 30), grad_text, fill=grad_color)

canvas.save(OUT, 'PNG')
print(f"Final deliverable saved to {OUT}")
print(f"Size: {W}x{H}")
