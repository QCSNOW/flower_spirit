"""Generate dye crafting recipes for all flowers."""
import json
import os

RECIPE_DIR = r"D:\mcmod\mytestmod\src\main\resources\data\firstmod\recipes"

# Flower ID -> dye color
FLOWER_DYE_MAP = {
    "lisianthus": "purple_dye",
    "carnation": "pink_dye",
    "hydrangea": "blue_dye",
    "lily": "white_dye",
    "dahlia": "pink_dye",
    "gerbera": "orange_dye",
    "ping_pong_chrysanthemum": "lime_dye",
    "firework_chrysanthemum": "red_dye",
    "violet": "purple_dye",
    "astilbe": "pink_dye",
    "trachymene": "light_blue_dye",
    "ranunculus": "orange_dye",
    "wintersweet": "yellow_dye",
    "waxflower": "pink_dye",
    "pincushion": "orange_dye",
    "king_protea": "pink_dye",
    "hypericum": "red_dye",
    "anemone": "blue_dye",
    "alstroemeria": "pink_dye",
    "chamomile": "white_dye",
    "baby_breath": "white_dye",
    "viburnum": "white_dye",
    "forget_me_not": "blue_dye",
    "gomphrena": "purple_dye",
    "celosia": "red_dye",
    "lupine": "purple_dye",
    "aster": "purple_dye",
    "clematis": "purple_dye",
    "bells_of_ireland": "green_dye",
    "gloriosa": "orange_dye",
    "oncidium": "yellow_dye",
    "dancing_lady": "yellow_dye",
    "phalaenopsis": "pink_dye",
    "dendrobium": "purple_dye",
}

for flower_id, dye in FLOWER_DYE_MAP.items():
    recipe = {
        "type": "minecraft:crafting_shapeless",
        "ingredients": [
            {"item": f"firstmod:{flower_id}"}
        ],
        "result": {
            "item": f"minecraft:{dye}",
            "count": 1
        }
    }
    filename = f"dye_from_{flower_id}.json"
    filepath = os.path.join(RECIPE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(recipe, f, indent=2, ensure_ascii=False)
    print(f"Created: {filename} -> {dye}")

print(f"\nTotal: {len(FLOWER_DYE_MAP)} recipes created")
