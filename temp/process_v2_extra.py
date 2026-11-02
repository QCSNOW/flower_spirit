import os, sys
sys.path.insert(0, r'D:\mcmod\mytestmod\temp')
from process_flowers_v2 import process_flower

SRC = r"D:\mcmod\mytestmod\temp\ai_source"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block"

extras = [
    ("hydrangea_v2", "hydrangea"),
    ("lily_v2", "lily"),
    ("waxflower_v2", "waxflower"),
    ("dancing_lady_v2", "dancing_lady"),
]

for src_name, dst_name in extras:
    src = os.path.join(SRC, f"{src_name}.jpg")
    dst = os.path.join(DST, f"{dst_name}.png")
    process_flower(dst_name, src, dst)
