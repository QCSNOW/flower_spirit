"""Detailed pixel grid analysis for all 12 textures."""
import numpy as np
from PIL import Image
import os

TEX_DIR = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"
flowers = ["waxflower","aster","dancing_lady","chamomile","oncidium",
           "anemone","astilbe","hydrangea","bells_of_ireland","hypericum",
           "lupine","wintersweet"]

for fname in flowers:
    path = os.path.join(TEX_DIR, f"{fname}.png")
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    
    print(f"\n=== {fname} ===")
    for y in range(32):
        row = ""
        for x in range(32):
            a = arr[y, x, 3]
            if a == 0:
                row += "..."
            else:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                # Classify pixel type
                if g > r + 20 and g > b + 20:
                    row += "GGG"  # green
                elif r > g + 20 and r > b + 20:
                    row += "RRR"  # red
                elif b > r + 20 and b > g + 20:
                    row += "BBB"  # blue
                elif r > 200 and g > 200 and b > 200:
                    row += "WWW"  # white
                elif r > 200 and g > 150:
                    row += "YYY"  # yellow
                elif r > 150 and g < 100:
                    row += "PPp"  # pink/purple
                elif r > 100 and g > 50 and b < 50:
                    row += "OOO"  # orange/brown
                else:
                    row += f"{r:02x}{g:02x}{b:02x}"
        if row.strip('.'):
            print(f"  {y:2d}: {row}")
