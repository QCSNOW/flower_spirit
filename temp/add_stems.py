"""
Add green stems to flower textures that are missing them.
For each flower, check if bottom 4 rows have green pixels.
If not, add a simple green stem (2px wide, 4-6px tall) at bottom center.
"""

from PIL import Image
import numpy as np
import os

TEX_DIR = r'D:\mcmod\mytestmod\src\main\resources\assets\firstmod\textures\block'

# Flowers that need stems (no green in bottom rows, and it makes sense to have a stem)
# Exclude: wisteria (hanging, stem at top), bells_of_ireland (already has green)
NEEDS_STEM = [
    'hydrangea',      # round ball, no stem
    'firework_chrysanthemum',  # has bottom content but no green
    'violet',         # has bottom content but maybe no stem
    'wintersweet',    # woody stem, should add brown/green
    'king_protea',    # thick stem
    'gloriosa',       # vine stem
    'dancing_lady',   # orchid stem
]

# Stem colors (MC vanilla green stem)
STEM_COLORS = [
    (58, 79, 35),    # dark green
    (77, 102, 46),   # medium green
    (96, 125, 58),   # light green
    (67, 90, 40),    # mid dark green
]

# For woody stems (wintersweet, king_protea)
WOODY_STEM_COLORS = [
    (74, 53, 30),    # dark brown
    (101, 74, 43),   # medium brown
    (124, 93, 58),   # light brown
]

WOODY_STEMS = ['wintersweet', 'king_protea']


def has_green_stem(arr):
    """Check if bottom 4 rows have green pixels."""
    alpha = arr[:, :, 3]
    for y in range(28, 32):
        for x in range(32):
            if alpha[y, x] > 0:
                r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
                if g > r and g > b and g > 50:
                    return True
    return False


def find_bottom_center(arr):
    """Find the center x of the bottom-most content."""
    alpha = arr[:, :, 3]
    # Find lowest row with content
    for y in range(31, -1, -1):
        xs = np.where(alpha[y] > 0)[0]
        if len(xs) > 0:
            center_x = (xs[0] + xs[-1]) // 2
            return center_x, y
    return 16, 31  # default center


def add_stem(arr, is_woody=False):
    """Add a green/brown stem at bottom center."""
    colors = WOODY_STEM_COLORS if is_woody else STEM_COLORS

    alpha = arr[:, :, 3]
    center_x, bottom_y = find_bottom_center(arr)

    # If content reaches very bottom, we need to shift things up
    # Otherwise, add stem below the content
    stem_top = bottom_y + 1 if bottom_y < 31 else 28
    stem_height = min(6, 32 - stem_top)

    if stem_height < 3:
        # Not enough room, extend stem from bottom
        stem_top = max(24, 32 - 6)
        stem_height = 32 - stem_top

    # Draw stem: 2px wide, slightly tapering
    for i in range(stem_height):
        y = stem_top + i
        if y >= 32:
            break
        # Width: 2-3 pixels
        w = 2 if i < stem_height - 2 else 1
        for dx in range(-w, w + 1):
            x = center_x + dx
            if 0 <= x < 32:
                # Alternate colors for texture
                color = colors[(i + dx) % len(colors)]
                arr[y, x, 0] = color[0]
                arr[y, x, 1] = color[1]
                arr[y, x, 2] = color[2]
                arr[y, x, 3] = 255

    # Also add a small leaf
    leaf_y = stem_top + stem_height // 2
    if leaf_y < 32:
        # Small leaf to the right
        for dy in range(-1, 2):
            for dx in range(1, 4):
                ly, lx = leaf_y + dy, center_x + dx
                if 0 <= ly < 32 and 0 <= lx < 32:
                    if arr[ly, lx, 3] == 0:  # only if empty
                        arr[ly, lx, :3] = colors[2]  # light green
                        arr[ly, lx, 3] = 255
        # Small leaf to the left
        for dy in range(-1, 2):
            for dx in range(-3, 0):
                ly, lx = leaf_y + dy, center_x + dx
                if 0 <= ly < 32 and 0 <= lx < 32:
                    if arr[ly, lx, 3] == 0:
                        arr[ly, lx, :3] = colors[1]  # medium green
                        arr[ly, lx, 3] = 255

    return arr


def main():
    for name in NEEDS_STEM:
        path = os.path.join(TEX_DIR, f'{name}.png')
        if not os.path.exists(path):
            print(f'SKIP: {name} not found')
            continue

        img = Image.open(path)
        arr = np.array(img).astype(np.uint8)

        if has_green_stem(arr):
            print(f'{name}: already has green stem, skip')
            continue

        is_woody = name in WOODY_STEMS
        arr = add_stem(arr, is_woody)

        img = Image.fromarray(arr, 'RGBA')
        img.save(path, 'PNG')

        n_vis = int(np.sum(arr[:, :, 3] > 0))
        has_stem = has_green_stem(arr)
        stem_type = 'woody' if is_woody else 'green'
        print(f'{name}: added {stem_type} stem, now {n_vis} pixels, has_stem={has_stem}')


if __name__ == '__main__':
    main()
