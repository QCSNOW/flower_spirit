import sys
sys.path.insert(0, r'D:\mcmod\mytestmod\temp')
from process_v3 import process_flower
import os

SRC = r'D:\mcmod\mytestmod\temp\ai_source'
DST = r'D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block'

# All flowers that need the v3 saturation boost and better processing
# Using existing v2 AI images but reprocessed with saturation boost
flowers_v2 = [
    "dahlia", "gerbera", "ping_pong_chrysanthemum", "firework_chrysanthemum",
    "astilbe", "trachymene", "ranunculus", "wintersweet", "waxflower",
    "hypericum", "anemone", "alstroemeria", "chamomile", "baby_breath",
    "viburnum", "forget_me_not", "gomphrena", "celosia", "aster",
    "clematis", "bells_of_ireland", "gloriosa", "oncidium", "dancing_lady",
    "phalaenopsis", "dendrobium"
]

# Flowers already re-processed with v3 AI
already_done = [
    "dahlia", "pincushion", "hypericum", "lupine", "oncidium",
    "dancing_lady", "phalaenopsis", "dendrobium", "violet",
    "king_protea", "wisteria", "astilbe"
]

to_process = [f for f in flowers_v2 if f not in already_done]

print(f"Processing {len(to_process)} flowers with saturation boost...")
for name in to_process:
    src = os.path.join(SRC, f"{name}.jpg")
    if not os.path.exists(src):
        src = os.path.join(SRC, f"{name}.png")
    dst = os.path.join(DST, f"{name}.png")
    if not os.path.exists(src):
        print(f"SKIP: {name} - no source")
        continue
    try:
        process_flower(name, src, dst, 0.92)
    except Exception as e:
        print(f"ERROR: {name}: {e}")

print(f"\nDone with {len(to_process)} flowers")
