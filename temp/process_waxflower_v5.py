"""Waxflower v5: minor polish - clean up stem dark artifacts.
Shape unchanged, only fix dark pixels mixed in the stem area.
"""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
T = 32

arr = np.array(Image.open(DST).convert('RGBA'))

# Find dark pixels in the stem area (below flower, y >= 20)
# Replace dark pixels that are surrounded by green with appropriate green
result = arr.copy()

# First, get all green colors in the texture
green_colors = []
for y in range(T):
    for x in range(T):
        if result[y, x, 3] > 0:
            r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
            if g > r + 10 and g > b + 5:
                c = (r, g, b)
                if c not in green_colors:
                    green_colors.append(c)

# Sort greens by luminance
def lum(c):
    return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
green_colors.sort(key=lum)
print(f"Green shades ({len(green_colors)}):")
for i, c in enumerate(green_colors):
    print(f"  {i}: RGB{c} (lum={lum(c):.0f})")

# In stem area (y >= 18), replace dark pixels with nearest green
# Dark = not green, not cream/white, not pink
stem_fixes = 0
for y in range(18, T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        # Check if it's a dark pixel surrounded by greens
        is_dark = not (g > r + 5 and g > b + 5) and g < 150
        
        if is_dark:
            # Count green neighbors
            green_nbrs = 0
            neighbor_greens = []
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < T and 0 <= nx < T and result[ny, nx, 3] > 0:
                    nr, ng, nb = int(result[ny,nx,0]), int(result[ny,nx,1]), int(result[ny,nx,2])
                    if ng > nr + 10 and ng > nb + 5:
                        green_nbrs += 1
                        neighbor_greens.append((nr, ng, nb))
            
            # If most neighbors are green, replace with appropriate green
            if green_nbrs >= 2:
                # Find the closest green shade
                dists = [sum((a-c2)**2 for a,c2 in zip((r,g,b), gc)) for gc in green_colors]
                # Use a medium green (not too dark, not too light)
                # Pick based on position: left side = lighter, right side = darker
                stem_center = 14  # approximate
                if x <= stem_center:
                    # Left side: lighter green
                    new_c = green_colors[len(green_colors)//2 + 1] if len(green_colors) > 3 else green_colors[-1]
                else:
                    # Right side: darker green
                    new_c = green_colors[len(green_colors)//2 - 1] if len(green_colors) > 3 else green_colors[0]
                result[y, x] = [new_c[0], new_c[1], new_c[2], 255]
                stem_fixes += 1

print(f"\nFixed {stem_fixes} dark pixels in stem area")

# Also check for dark pixels inside the flower cluster that might be noise
# (but keep actual petal edges - only fix truly isolated dark pixels)
flower_fixes = 0
for y in range(3, 20):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        # Dark pixel check
        is_dark = g < 100 and r < 100 and b < 100
        if not is_dark:
            continue
        
        # Count light/cream neighbors
        light_nbrs = 0
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < T and 0 <= nx < T and result[ny, nx, 3] > 0:
                nr, ng, nb = int(result[ny,nx,0]), int(result[ny,nx,1]), int(result[ny,nx,2])
                if nr > 180 and ng > 180:  # cream/white neighbor
                    light_nbrs += 1
        
        # If surrounded by light pixels (3+), this dark pixel is noise
        if light_nbrs >= 3:
            # Replace with light cream color
            result[y, x] = [245, 230, 210, 255]
            flower_fixes += 1

if flower_fixes > 0:
    print(f"Fixed {flower_fixes} dark noise pixels in flower area")

# Save
Image.fromarray(result, 'RGBA').save(DST, 'PNG')
# Sync item
Image.fromarray(result, 'RGBA').save(r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\waxflower.png", 'PNG')

n_final = int(np.sum(result[:,:,3] > 0))
c_final = len(set(tuple(result[y,x,:3]) for y in range(T) for x in range(T) if result[y,x,3] > 0))
print(f"\nFinal: {n_final}px, {c_final} colors")

# Final preview
print("\nFinal preview:")
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

print("\nDone! Block and item textures updated.")
