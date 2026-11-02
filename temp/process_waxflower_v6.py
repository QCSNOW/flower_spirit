"""Waxflower v6: fix gray pixels in stem that should be green.
These are artifacts from color quantization - gray pixels surrounded by green.
Shape unchanged.
"""
import numpy as np
from PIL import Image

DST_BLOCK = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\waxflower.png"
DST_ITEM = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\item\waxflower.png"
T = 32

arr = np.array(Image.open(DST_BLOCK).convert('RGBA'))
result = arr.copy()

# Find all green colors
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
print(f"Green shades: {len(greens)}")
for i, g in enumerate(greens):
    print(f"  {i}: RGB{g} (lum={lum(g):.0f})")

# Find gray/neutral pixels surrounded by green -> replace with appropriate green
fixed = 0
for y in range(T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        
        # Check if it's a neutral/gray pixel (r≈g≈b, not green, not cream, not pink)
        is_gray = abs(r - g) < 15 and abs(g - b) < 15 and not (g > r + 10 and g > b + 5) and r < 200
        if not is_gray:
            continue
        
        # Count green neighbors (4-directional)
        green_nbrs = []
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < T and 0 <= nx < T and result[ny, nx, 3] > 0:
                nr, ng, nb = int(result[ny,nx,0]), int(result[ny,nx,1]), int(result[ny,nx,2])
                if ng > nr + 10 and ng > nb + 5:
                    green_nbrs.append((nr, ng, nb))
        
        # If surrounded by 3+ green pixels, it should be green
        if len(green_nbrs) >= 2:
            # Determine what shade of green:
            # If left neighbor is light and right is dark, this is the mid-stem pixel
            # Find average luminance of green neighbors
            avg_lum = sum(lum(c) for c in green_nbrs) / len(green_nbrs)
            # Find closest green shade
            closest = min(greens, key=lambda gc: abs(lum(gc) - avg_lum))
            result[y, x] = [closest[0], closest[1], closest[2], 255]
            fixed += 1

print(f"\nFixed {fixed} gray pixels in green areas")

# Also: any dark pixel surrounded by greens in stem area -> green
# Check for dark non-green pixels in stem (y >= 18)
dark_fixed = 0
for y in range(18, T):
    for x in range(T):
        if result[y, x, 3] == 0:
            continue
        r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
        
        # Already green? skip
        if g > r + 10 and g > b + 5:
            continue
        
        # Count green neighbors
        green_count = 0
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < T and 0 <= nx < T and result[ny, nx, 3] > 0:
                nr, ng, nb = int(result[ny,nx,0]), int(result[ny,nx,1]), int(result[ny,nx,2])
                if ng > nr + 10 and ng > nb + 5:
                    green_count += 1
        
        if green_count >= 3:
            # Replace with dark green
            result[y, x] = [greens[0][0], greens[0][1], greens[0][2], 255]
            dark_fixed += 1

if dark_fixed > 0:
    print(f"Fixed {dark_fixed} dark pixels in stem area")

# Save
Image.fromarray(result, 'RGBA').save(DST_BLOCK, 'PNG')
Image.fromarray(result, 'RGBA').save(DST_ITEM, 'PNG')

n_final = int(np.sum(result[:,:,3] > 0))
c_final = len(set(tuple(result[y,x,:3]) for y in range(T) for x in range(T) if result[y,x,3] > 0))
print(f"\nFinal: {n_final}px, {c_final} colors")

# Preview
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

print("\nDone! Both textures saved.")
