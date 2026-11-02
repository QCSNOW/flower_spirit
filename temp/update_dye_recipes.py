"""Batch update all flower-to-dye recipes according to the new color mapping.

Mapping (flower -> dye):
白色 (white): baby_breath, lily, viburnum, waxflower, bells_of_ireland
淡灰色 (light_gray): chamomile, ping_pong_chrysanthemum
粉色 (pink): carnation, alstroemeria, ranunculus, astilbe, king_protea
红色 (red): dahlia, celosia, hypericum
品红色 (magenta): gomphrena, phalaenopsis
橙色 (orange): pincushion, firework_chrysanthemum, gerbera, gloriosa
黄色 (yellow): dancing_lady, oncidium, wintersweet, dendrobium
紫色 (purple): anemone, aster, clematis, lupine, violet, lisianthus
蓝色 (blue): hydrangea
淡蓝色 (light_blue): forget_me_not, trachymene
"""
import json
import os

RECIPES_DIR = r"D:\mcmod\mytestmod\src\main\resources\data\firstmod\recipes"

mapping = {
    # 白色 white_dye
    "baby_breath": "white_dye",
    "lily": "white_dye",
    "viburnum": "white_dye",
    "waxflower": "white_dye",
    "bells_of_ireland": "white_dye",
    # 淡灰色 light_gray_dye
    "chamomile": "light_gray_dye",
    "ping_pong_chrysanthemum": "light_gray_dye",
    # 粉色 pink_dye
    "carnation": "pink_dye",
    "alstroemeria": "pink_dye",
    "ranunculus": "pink_dye",
    "astilbe": "pink_dye",
    "king_protea": "pink_dye",
    # 红色 red_dye
    "dahlia": "red_dye",
    "celosia": "red_dye",
    "hypericum": "red_dye",
    # 品红色 magenta_dye
    "gomphrena": "magenta_dye",
    "phalaenopsis": "magenta_dye",
    # 橙色 orange_dye
    "pincushion": "orange_dye",
    "firework_chrysanthemum": "orange_dye",
    "gerbera": "orange_dye",
    "gloriosa": "orange_dye",
    # 黄色 yellow_dye
    "dancing_lady": "yellow_dye",
    "oncidium": "yellow_dye",
    "wintersweet": "yellow_dye",
    "dendrobium": "yellow_dye",
    # 紫色 purple_dye
    "anemone": "purple_dye",
    "aster": "purple_dye",
    "clematis": "purple_dye",
    "lupine": "purple_dye",
    "violet": "purple_dye",
    "lisianthus": "purple_dye",
    # 蓝色 blue_dye
    "hydrangea": "blue_dye",
    # 淡蓝色 light_blue_dye
    "forget_me_not": "light_blue_dye",
    "trachymene": "light_blue_dye",
}

print("Updating dye recipes...")
updated = 0
errors = []

for flower, dye in mapping.items():
    filename = f"dye_from_{flower}.json"
    filepath = os.path.join(RECIPES_DIR, filename)
    
    if not os.path.exists(filepath):
        errors.append(f"Missing: {filename}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        recipe = json.load(f)
    
    old_dye = recipe.get("result", {}).get("item", "")
    recipe["result"]["item"] = f"minecraft:{dye}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(recipe, f, indent=2, ensure_ascii=False)
        f.write('\n')
    
    old_name = old_dye.replace("minecraft:", "") if old_dye else "unknown"
    print(f"  {flower:30s}: {old_name:20s} -> {dye}")
    updated += 1

print(f"\nUpdated: {updated}/{len(mapping)} recipes")
if errors:
    print(f"Missing files ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
else:
    print("All files found and updated!")
