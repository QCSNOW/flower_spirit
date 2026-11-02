from PIL import Image
import numpy as np
import os

tex_dir = r'D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block'

all_flowers = [
    'lisianthus','carnation','hydrangea','lily',
    'dahlia','gerbera','ping_pong_chrysanthemum','firework_chrysanthemum',
    'violet','astilbe','trachymene','ranunculus','wintersweet','waxflower',
    'pincushion','king_protea','hypericum','anemone','alstroemeria',
    'chamomile','baby_breath','viburnum','wisteria','forget_me_not',
    'gomphrena','celosia','lupine','aster','clematis','bells_of_ireland',
    'gloriosa','oncidium','dancing_lady','phalaenopsis','dendrobium'
]

print('Flower | Pixels | HasStem | BottomContent')
print('-' * 60)
for name in all_flowers:
    path = os.path.join(tex_dir, name + '.png')
    img = Image.open(path)
    arr = np.array(img)
    alpha = arr[:,:,3]
    n_vis = int(np.sum(alpha > 0))

    has_stem = False
    bottom_content = 0
    for y in range(31, 23, -1):
        row_vis = int(np.sum(alpha[y] > 0))
        if row_vis > 0:
            bottom_content += 1
            for x in range(32):
                if alpha[y, x] > 0:
                    r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
                    if g > r and g > b and g > 50:
                        has_stem = True
                        break

    stem_str = 'YES' if has_stem else 'NO'
    print(f'{name:30s} | {n_vis:5d} | {stem_str:3s} | {bottom_content}')
