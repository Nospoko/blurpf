import numpy as np

def read_colormap(path):
    """ Read it """
    cmap = []
    with open(path) as fin:
        for line in fin:
            rgb = [int(val) for val in line.split()]
            cmap.append(rgb)

    return np.uint8(cmap)
