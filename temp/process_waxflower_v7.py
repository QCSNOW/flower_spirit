"""Waxflower v7: final polish - fix white pixel in stem, ensure clean stem gradient.
Shape 100% preserved.
"""
import numpy as np
from PIL import Image

DST_BLOCK = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
DST_ITEM = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\waxflower.png"
T = 32

arr = np.array(Image.open(DST_BLOCK).convert('RGBA'))
result = arr.copy()

# Get green palette
greens = []
for y in range(T):
    for x in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if g > r + 10 and g > b + 5:
                c = (r, g, b)
                if c not in greens:
                    greens.append(c)

def lum(c):
    return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
greens.sort(key=lum)

# Fix light/cream pixels surrounded by green (in stem area)
fixed = 0
for y in range(10, T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        
        # Is it a cream/light pixel in the middle of green?
        is_cream = r > 180 and g > 180 and b > 160
        if not is_cream:
            continue
        
        # Count green neighbors
        green_nbrs = 0
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < T and 0 <= nx < T and result[ny, nx, 3] > 0:
                nr, ng, nb = int(result[ny,nx,0]), int(result[ny,nx,1]), int(result[ny,nx,2])
                if ng > nr + 10 and ng > nb + 5:
                    green_nbrs += 1
        
        if green_nbrs >= 3:
            # Replace with medium green
            mid_green = greens[len(greens)//2]
            result[y, x] = [mid_green[0], mid_green[1], mid_green[2], 255]
            fixed += 1

print(f"Fixed {fixed} cream pixels in green areas")

# Final color count and stats
final_colors = set()
for y in range(T):
    for x in range(T):
        if result[y, x, 3] > 0:
            final_colors.add(tuple(result[y, x, :3]))

n_px = int(np.sum(result[:,:,3] > 0))
print(f"\nFinal: {n_px}px, {len(final_colors)} colors")

# Save
Image.fromarray(result, 'RGBA').save(DST_BLOCK, 'PNG')
Image.fromarray(result, 'RGBA').save(DST_ITEM, 'PNG')

# Detailed stem check
print("\nStem detail (y=20 to 31):")
for y in range(20, 32):
    line = ''
    for x in range(10, 22):
        if result[y, x, 3] == 0:
            line += '.'
        else:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if g > r + 10 and g > b + 5:
                line += 'G'
            else:
                line += '#'
    print(f"  y={y:2d}: {line}")

# Full preview
print("\nFull preview:")
for y in range(T):
    line = ''
    for x in range(T):
        if result[y, x, 3] == 0:
            line += '.'
        else:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if g > r + 10 and g > b + 5:
                line += 'G'
            elif r > g + 10 and b > g + 5:
                line += 'P'
            elif r > 200 and g > 200:
                line += 'W'
            else:
                line += '#'
    print(f"  {y:2d}: {line}")

print("\nDone! Block and item textures saved.")
