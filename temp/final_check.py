"""Final comprehensive self-check comparison sheet."""
import numpy as np
from PIL import Image, ImageDraw
import os

SRC = r"D:\mcmod\mytestmod\temp"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
OUT = r"D:\mcmod\mytestmod\temp\comparison_v4.png"
T = 32

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
CELL_W = 340
CELL_H = 310
COLS = 4
ROWS = 3

canvas = Image.new('RGB', (CELL_W * COLS, CELL_H * ROWS), (200, 200, 200))
draw = ImageDraw.Draw(canvas)

for i, (ref_name, tex_name, label) in enumerate(flowers):
    col = i % COLS
    row = i // COLS
    x0 = col * CELL_W
    y0 = row * CELL_H
    
    ref = Image.open(os.path.join(SRC, ref_name)).convert('RGB')
    ref = ref.resize((128, 128), Image.BILINEAR)
    canvas.paste(ref, (x0 + 16, y0 + 30))
    
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
    canvas.paste(checker, (x0 + 170, y0 + 22))
    
    draw.text((x0 + 10, y0 + 5), f"{i+1}. {label}", fill=(0, 0, 0))
    
    tex_arr = np.array(tex)
    n_px = int(np.sum(tex_arr[:,:,3] > 0))
    colors = set()
    for y in range(32):
        for x in range(32):
            if tex_arr[y, x, 3] > 0:
                colors.add(tuple(tex_arr[y, x, :3]))
    nc = len(colors)
    
    # === Comprehensive Self-Assessment (100pts) ===
    score = 0
    issues = []
    
    # 1. Pixel count (20pts): optimal 180-320
    if 200 <= n_px <= 300: 
        score += 20
    elif 160 <= n_px <= 340: 
        score += 15
    elif 120 <= n_px <= 380: 
        score += 8
    else: 
        score += 2
        issues.append("size")
    
    # 2. Color count (20pts): optimal 10-14
    if 10 <= nc <= 14: 
        score += 20
    elif 8 <= nc <= 16: 
        score += 14
    elif 6 <= nc <= 18: 
        score += 8
    else: 
        score += 2
        issues.append("colors")
    
    # 3. Stem gradient (20pts): left highlight, right shadow
    has_grad = False
    grad_score = 0
    for y in range(25, 31):
        l_g, r_g = 255, 255
        l_x, r_x = -1, -1
        for x in range(T):
            if tex_arr[y, x, 3] > 0:
                r, g, b = int(tex_arr[y,x,0]), int(tex_arr[y,x,1]), int(tex_arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    if x < 16 and g < l_g:
                        l_g = g
                        l_x = x
                    if x > 15 and g < r_g:
                        r_g = g
                        r_x = x
        # Left side should be lighter (higher g value), right side darker
        # Let's check both sides
        all_g = []
        for x in range(T):
            if tex_arr[y, x, 3] > 0:
                r, g, b = int(tex_arr[y,x,0]), int(tex_arr[y,x,1]), int(tex_arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    all_g.append((x, g))
        if len(all_g) >= 3:
            all_g.sort()
            left_g = all_g[0][1]
            right_g = all_g[-1][1]
            if left_g > right_g + 15:
                grad_score += 1
    
    if grad_score >= 4:
        score += 20
    elif grad_score >= 2:
        score += 12
    elif grad_score >= 1:
        score += 5
    else:
        score += 2
        issues.append("stem")
    
    # 4. Clean edges / no noise (15pts)
    isolated = 0
    for y in range(T):
        for x in range(T):
            if tex_arr[y, x, 3] == 0:
                continue
            nbr = 0
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < T and 0 <= nx < T and tex_arr[ny, nx, 3] > 0:
                    nbr += 1
            if nbr <= 1:
                isolated += 1
    
    if isolated == 0: 
        score += 15
    elif isolated <= 3: 
        score += 10
    elif isolated <= 8: 
        score += 5
    else: 
        score += 1
        issues.append("noise")
    
    # 5. Leaves present (15pts)
    leaf_left = 0
    leaf_right = 0
    for y in range(22, 31):
        for x in range(5, 14):
            if tex_arr[y, x, 3] > 0:
                r, g, b = int(tex_arr[y,x,0]), int(tex_arr[y,x,1]), int(tex_arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    leaf_left += 1
        for x in range(18, 27):
            if tex_arr[y, x, 3] > 0:
                r, g, b = int(tex_arr[y,x,0]), int(tex_arr[y,x,1]), int(tex_arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    leaf_right += 1
    
    total_leaf = leaf_left + leaf_right
    has_both = leaf_left > 3 and leaf_right > 3
    if total_leaf >= 20 and has_both:
        score += 15
    elif total_leaf >= 12:
        score += 10
    elif total_leaf >= 5:
        score += 5
    else:
        score += 1
        issues.append("no leaves")
    
    # 6. Flower-stem connection (10pts)
    connected = False
    for y in range(10, 25):
        has_flower = False
        has_stem_below = False
        for x in range(T):
            if tex_arr[y, x, 3] > 0:
                r, g, b = int(tex_arr[y,x,0]), int(tex_arr[y,x,1]), int(tex_arr[y,x,2])
                if not (g > r + 10 and g > b + 10):
                    has_flower = True
        if has_flower:
            # Check if there's green below this row
            for y2 in range(y+1, min(y+5, T)):
                for x in range(T):
                    if tex_arr[y2, x, 3] > 0:
                        r, g, b = int(tex_arr[y2,x,0]), int(tex_arr[y2,x,1]), int(tex_arr[y2,x,2])
                        if g > r + 10 and g > b + 10:
                            has_stem_below = True
                            break
                if has_stem_below:
                    break
            if has_stem_below:
                connected = True
            break
    
    score += 10 if connected else 2
    if not connected:
        issues.append("disconnected")
    
    # Score display
    status = "PASS" if score >= 85 else "CHECK" if score >= 70 else "FAIL"
    if score >= 85:
        color = (0, 160, 0)
    elif score >= 70:
        color = (200, 140, 0)
    else:
        color = (200, 50, 0)
    
    draw.text((x0 + 16, y0 + 172), f"{n_px}px / {nc} colors", fill=(40, 40, 40))
    draw.text((x0 + 16, y0 + 190), f"Score: {score}/100 [{status}]", fill=color)
    if issues:
        draw.text((x0 + 16, y0 + 208), f"Issues: {', '.join(issues)}", fill=(150, 50, 50))

canvas.save(OUT, 'PNG')
print(f"Saved to {OUT}")

# Print summary
print("\n=== Final Assessment Summary ===")
for i, (_, tex_name, label) in enumerate(flowers):
    tex_arr = np.array(Image.open(os.path.join(DST, tex_name)).convert('RGBA'))
    n_px = int(np.sum(tex_arr[:,:,3] > 0))
    nc = len(set(tuple(tex_arr[y,x,:3]) for y in range(T) for x in range(T) if tex_arr[y,x,3] > 0))
    print(f"  {i+1:2d}. {label:20s}: {n_px:4d}px, {nc:2d}c")
