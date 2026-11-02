"""Process waxflower and aster with BoP style."""
import sys, os
sys.path.insert(0, r"D:\mcmod\mytestmod\temp")
from process_v3 import process_flower

DST_DIR = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

# Waxflower: dense cluster of small pink flowers, fill high to get more pixels
waxflower_src = r"D:\mcmod\mytestmod\temp\waxflower_bop.jpg"
waxflower_dst = os.path.join(DST_DIR, "waxflower.png")
n1 = process_flower("waxflower", waxflower_src, waxflower_dst, fill_ratio=1.0)
print(f"\nWaxflower: {n1} pixels")

# Aster: radial flower with yellow center + purple petals, fill high
aster_src = r"D:\mcmod\mytestmod\temp\aster_bop.jpg"
aster_dst = os.path.join(DST_DIR, "aster.png")
n2 = process_flower("aster", aster_src, aster_dst, fill_ratio=1.0)
print(f"\nAster: {n2} pixels")
