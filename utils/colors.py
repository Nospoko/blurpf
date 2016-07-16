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
