"""
Fix all flower item models to use block model as parent.
This ensures the item texture always matches the block texture.
"""
import json
import os

ITEM_DIR = r'D:\mcmod\mytestmod\src\main\resources\assets\firstmod\models\item'

FLOWERS = [
    "lisianthus", "carnation", "hydrangea", "lily",
    "dahlia", "gerbera", "ping_pong_chrysanthemum", "firework_chrysanthemum",
    "violet", "astilbe", "trachymene", "ranunculus", "wintersweet", "waxflower",
    "pincushion", "king_protea", "hypericum", "anemone", "alstroemeria",
    "chamomile", "baby_breath", "viburnum", "wisteria", "forget_me_not",
    "gomphrena", "celosia", "lupine", "aster", "clematis", "bells_of_ireland",
    "gloriosa", "oncidium", "dancing_lady", "phalaenopsis", "dendrobium"
]

for flower in FLOWERS:
    path = os.path.join(ITEM_DIR, f'{flower}.json')
    if not os.path.exists(path):
        print(f'SKIP: {flower}.json not found')
        continue

    data = {
        "parent": f"firstmod:block/{flower}"
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f'Fixed: {flower}.json -> parent: firstmod:block/{flower}')

print(f'\nFixed {len(FLOWERS)} item models')
