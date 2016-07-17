import numpy as np

def read_colormap(path, opaque = False):
    """ Read it """
    cmap = []
    with open(path) as fin:
        for line in fin:
            rgb = [int(val) for val in line.split()]
            if opaque:
                rgb.append(200)
            cmap.append(rgb)

    return np.uint8(cmap)

def mixed_colormap(color_a, color_b, proportions):
    """ Create a custom colormap """
    # List options
    cmaps = {
            0 : 'colormaps/blues.cmap',
            1 : 'colormaps/fire.cmap',
            2 : 'colormaps/reds.cmap',
            3 : 'colormaps/seashore.cmap',
            4 : 'colormaps/teals.cmap',
            5 : 'colormaps/purples.cmap',
            6 : 'colormaps/ice.cmap',
            7 : 'colormaps/dusk.cmap',
            8 : 'colormaps/dawn.cmap',
            9 : 'colormaps/greens.cmap',
            10 : 'colormaps/golds.cmap',
            11 : 'colormaps/redblue.cmap'
            }

    # Choose
    c_path_a = cmaps[color_a]
    c_path_b = cmaps[color_b]
    cmap_a = read_colormap(c_path_a, True)
    cmap_b = read_colormap(c_path_b, True)

    # Refactor
    asd = proportions
    cmap = cmap_a * (1.0 - asd) + cmap_b * asd
    cmap = cmap.astype(int)

    return cmap

