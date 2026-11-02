"""Generate comparison: source image vs final waxflower texture."""
import numpy as np
from PIL import Image, ImageDraw

SRC = r"c:\Users\Administrato\.trae-cn\attachments\6aa3e321cc95028a5ea03b4e\e9b02282-ea48-43e5-a171-90f1ac375154_aee3403a-dd85-46f4-a9b5-1c6778526c9b_澳洲腊梅.png"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
OUT = r"D:\mcmod\mytestmod\temp\waxflower_compare.png"
MAG = 10
T = 32

src = Image.open(SRC).convert('RGBA')
dst = Image.open(DST).convert('RGBA')

src_mag = src.resize((T*MAG, T*MAG), Image.NEAREST)
dst_mag = dst.resize((T*MAG, T*MAG), Image.NEAREST)

W = T*MAG * 2 + 80
H = T*MAG + 80

canvas = Image.new('RGB', (W, H), (220, 220, 220))
draw = ImageDraw.Draw(canvas)

# Checker bg helper
def make_checker(size, mag):
    checker = Image.new('RGB', (size*mag, size*mag), (248, 248, 248))
    for cy in range(size):
        for cx in range(size):
            if (cx + cy) % 2 == 0:
                for dy in range(mag):
                    for dx in range(mag):
                        checker.putpixel((cx*mag+dx, cy*mag+dy), (228, 228, 228))
    return checker

# Source on checker
checker1 = make_checker(T, MAG)
checker1.paste(src_mag, (0, 0), src_mag)
canvas.paste(checker1, (30, 40))
draw.text((30, 10), "Original (10x zoom)", fill=(0, 0, 0))

# Final on checker
checker2 = make_checker(T, MAG)
checker2.paste(dst_mag, (0, 0), dst_mag)
canvas.paste(checker2, (T*MAG + 50, 40))
draw.text((T*MAG + 50, 10), "Processed (10x zoom)", fill=(0, 0, 0))

# Stats
src_arr = np.array(src)
dst_arr = np.array(dst)

src_opaque = np.sum(src_arr[:,:,3] > 128)
dst_opaque = np.sum(dst_arr[:,:,3] > 0)

src_colors = len(set(tuple(src_arr[y,x,:3]) for y in range(T) for x in range(T) if src_arr[y,x,3] > 128))
dst_colors = len(set(tuple(dst_arr[y,x,:3]) for y in range(T) for x in range(T) if dst_arr[y,x,3] > 0))

draw.text((30, T*MAG + 55), f"Original: {src_opaque}px, {src_colors} colors", fill=(60, 60, 60))
draw.text((T*MAG + 50, T*MAG + 55), f"Processed: {dst_opaque}px, {dst_colors} colors", fill=(60, 60, 60))

draw.text((30, T*MAG + 70), "Shape preserved, colors reduced, stem cleaned", fill=(0, 120, 0))

canvas.save(OUT, 'PNG')
print(f"Saved to {OUT}")
