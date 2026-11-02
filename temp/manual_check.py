"""Manual quality check for all 12 flowers."""
import numpy as np
from PIL import Image

T = 32
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
flowers = ['waxflower','aster','dancing_lady','chamomile','oncidium',
           'anemone','astilbe','hydrangea','bells_of_ireland','hypericum',
           'lupine','wintersweet']

def check(name, arr):
    # Flower bottom (lowest non-green pixel)
    flower_bottom = -1
    for y in range(T-1, -1, -1):
        has_flower = False
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
                if not (g > r + 10 and g > b + 10):
                    has_flower = True
                    break
        if has_flower:
            flower_bottom = y
            break
    
    # Stem top (highest green pixel)
    stem_top = T
    for y in range(T):
        has_stem = False
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    has_stem = True
                    break
        if has_stem:
            stem_top = y
            break
    
    # Stem gradient (left lighter than right)
    has_grad = False
    for y in range(25, 31):
        greens = []
        for x in range(T):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    greens.append((x, g))
        if len(greens) >= 3:
            greens.sort()
            if greens[0][1] > greens[-1][1] + 15:
                has_grad = True
    
    # Isolated pixels
    isolated = 0
    for y in range(T):
        for x in range(T):
            if arr[y, x, 3] == 0:
                continue
            nbr = 0
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < T and 0 <= nx < T and arr[ny, nx, 3] > 0:
                    nbr += 1
            if nbr <= 1:
                isolated += 1
    
    # Leaves (side green pixels)
    leaves = 0
    for y in range(20, 31):
        for x in range(3, 14):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    leaves += 1
        for x in range(18, 29):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y,x,0]), int(arr[y,x,1]), int(arr[y,x,2])
                if g > r + 10 and g > b + 10:
                    leaves += 1
    
    n_px = int(np.sum(arr[:,:,3] > 0))
    n_c = len(set(tuple(arr[y,x,:3]) for y in range(T) for x in range(T) if arr[y,x,3] > 0))
    
    connected = stem_top <= flower_bottom + 2
    
    return n_px, n_c, flower_bottom, stem_top, connected, has_grad, isolated, leaves

print(f"{'Flower':20s} {'Px':>4s} {'Co':>2s} {'FB':>3s} {'ST':>3s} Conn  Grad  Iso Lvs Status")
print("-" * 70)

pass_count = 0
for name in flowers:
    arr = np.array(Image.open(f"{DST}\\{name}.png").convert('RGBA'))
    n_px, n_c, fb, st, conn, grad, iso, lvs = check(name, arr)
    
    issues = []
    if not conn: issues.append("disconnected")
    if not grad: issues.append("no-grad")
    if iso > 5: issues.append("noise")
    if lvs < 10: issues.append("few-leaves")
    
    status = "PASS" if not issues else "CHECK: " + ", ".join(issues)
    if not issues:
        pass_count += 1
    
    print(f"{name:20s} {n_px:4d} {n_c:2d} {fb:3d} {st:3d} {str(conn):5s} {str(grad):5s} {iso:3d} {lvs:3d}  {status}")

print(f"\nPass: {pass_count}/12")
