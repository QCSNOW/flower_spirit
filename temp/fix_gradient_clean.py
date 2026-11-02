"""Fix chamomile and hypericum stem gradient + edge cleanup."""
import numpy as np
from PIL import Image

DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
T = 32

G1 = (160, 215, 70)
G2 = (130, 190, 40)
G3 = (95, 155, 25)
G4 = (65, 115, 12)
G5 = (40, 75, 5)

def px(a, y, x, c):
    if 0 <= y < T and 0 <= x < T:
        a[y, x] = [c[0], c[1], c[2], 255]

def load(name):
    return np.array(Image.open(f"{DST}\\{name}.png").convert('RGBA'))

def save(arr, name):
    Image.fromarray(arr, 'RGBA').save(f"{DST}\\{name}.png", 'PNG')

def fix_stem_gradient(arr):
    """Ensure stem has proper left-light / right-dark gradient."""
    # Find stem center in bottom rows
    stem_cx = None
    for y in range(28, 31):
        green_xs = []
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    green_xs.append(x)
        if len(green_xs) >= 2:
            stem_cx = sum(green_xs) // len(green_xs)
            break
    
    if stem_cx is None:
        return arr
    
    # Walk up from bottom, fix each stem row
    result = arr.copy()
    for y in range(31, -1, -1):
        green_xs = []
        for x in range(T):
            if result[y, x, 3] > 0:
                r, g, b = int(result[y,x,0]), int(result[y,x,1]), int(result[y,x,2])
                if g > r + 5 and g > b + 5 and g > 40:
                    green_xs.append(x)
        
        if not green_xs:
            continue
        
        # Only fix if it looks like a stem (2-5 pixels wide)
        if 2 <= len(green_xs) <= 6:
            left = min(green_xs)
            right = max(green_xs)
            
            # Apply gradient: left=highlight, mid=mid, right=shadow
            px(result, y, left, G1)
            if right - left >= 1:
                px(result, y, left + 1, G3)
            if right - left >= 2:
                px(result, y, right - 1, G3)
            if right > left:
                px(result, y, right, G4)
            # Base thickening
            if y >= 28:
                if left - 1 >= 0:
                    px(result, y, left - 1, G4)
                if right + 1 < T:
                    px(result, y, right + 1, G5)
    
    return result

def clean_edges(arr):
    """Remove truly isolated pixels (0 neighbors), keep 1-neighbor tips."""
    result = arr.copy()
    # First pass: remove 0-neighbor pixels (true noise)
    to_remove = []
    for y in range(T):
        for x in range(T):
            if result[y, x, 3] == 0:
                continue
            nbr = 0
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < T and 0 <= nx < T and result[ny, nx, 3] > 0:
                    nbr += 1
            if nbr == 0:
                to_remove.append((y, x))
    
    for y, x in to_remove:
        result[y, x, 3] = 0
    
    return result


# Fix all flowers
flowers = [
    "waxflower", "aster", "dancing_lady", "chamomile",
    "oncidium", "anemone", "astilbe", "hydrangea",
    "bells_of_ireland", "hypericum", "lupine", "wintersweet"
]

print("Fixing stem gradients and cleaning edges...")
for name in flowers:
    arr = load(name)
    
    # Fix stem gradient
    arr = fix_stem_gradient(arr)
    
    # Clean true noise
    arr = clean_edges(arr)
    
    save(arr, name)
    
    n_px = int(np.sum(arr[:,:,3] > 0))
    n_c = len(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0))
    print(f"  {name:20s}: {n_px:4d}px, {n_c:2d}c")

print("\nDone!")
