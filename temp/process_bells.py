"""Process Bells of Ireland texture."""
import sys
import os
sys.path.insert(0, r"D:\mcmod\mytestmod\temp")
from process_v3 import process_flower

SRC = r"D:\mcmod\mytestmod\temp\bells_of_ireland_ref2.jpg"
DST = r"D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block\bells_of_ireland.png"

if __name__ == '__main__':
    n = process_flower("bells_of_ireland", SRC, DST, fill_ratio=1.0)
    print(f"Done! {n} visible pixels")
