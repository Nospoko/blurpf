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
    timeshift = 0.3 + 0.3 * np.sin(7.*tick/500)
    phi = np.pi * 2 * tick/2500.0
    ax_shift = 2. * np.cos(phi)
    ay_shift = 2. * np.sin(phi)

    a_hahn = yo.Hahn()
    a_hahn.set_x_shift(ax_shift)
    a_hahn.set_y_shift(ay_shift)
    Za = a_hahn.get(XX, YY, tick)

    bx_shift = 2. * np.cos(phi - np.pi)
    by_shift = 2. * np.sin(phi - np.pi)

    b_hahn = yo.Hahn()
    b_hahn.set_x_shift(bx_shift)
    b_hahn.set_x_shift(by_shift)
    Zb = b_hahn.get(XX, YY, tick)

    Z = norm(Za) + norm(Zb)

    # le normalizatione
    Z -= Z.min()
    Z /= Z.max()
    Z *= 256.

    # OpenCV likes uint8
    return np.uint8(Z)

def main():
    """ blurp """
    if False:
        x_res = 1080
        y_res = 720
    else:
        x_res = 540
        y_res = 360

    span = 1
    x = np.linspace(-span, span, x_res)
    y = np.linspace(-span, span, y_res)
    XX, YY = np.meshgrid(x, y)

    for tick in range(500):
        print tick
        ZZ = funky_image(XX, YY, 5*tick)
        filename = 'imgs/{}.png'.format(1e7 + tick)
        img = cv.applyColorMap(ZZ, cv.COLORMAP_OCEAN)
        cv.imwrite(filename, img)

if __name__ == '__main__':
    main()
