import cv2 as cv
import numpy as np
from utils import signal as us
from utils import shapes as yo
from matplotlib import pyplot as plt

def norm(this):
    """ Squeeze to 0-1 """
    this -= this.min()
    this /= this.max()
    return this

def funky_image(XX, YY, tick):
    """ Generate some funk """
    a_hahn = yo.Hahn(4, 2, 8, 60.)
    Za = a_hahn.get(XX, YY, tick)

    fritz = yo.Fritz(1, 1)
    Zb = fritz.get(XX, YY, tick)

    meitner = yo.Meitner(2, 9)
    Zc = meitner.get(XX, YY, tick)

    Z = norm(Za) + norm(Zb) + norm(Zc)

    # le normalizatione
    Z -= Z.min()
    Z /= Z.max()
    Z *= 256.

    # OpenCV likes uint8
    return np.uint8(Z)

def main():
    """ blurp """
    x = np.linspace(-2, 0, 401)
    y = np.linspace(0, 2, 301)
    XX, YY = np.meshgrid(x, y)

    for tick in range(1000):
        print tick
        ZZ = funky_image(XX, YY, 3*tick)
        filename = 'imgs/{}.png'.format(1e7 + tick)
        img = cv.applyColorMap(ZZ, cv.COLORMAP_OCEAN)
        cv.imwrite(filename, img)

if __name__ == '__main__':
    main()
