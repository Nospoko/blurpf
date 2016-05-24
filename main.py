import cv2 as cv
import numpy as np
from utils import signal as us
from matplotlib import pyplot as plt

def funky_image(XX, YY, tick):
    """ Generate some funk """
    Z = np.sin(13.*(XX**3 + YY**2) + np.sin(tick/80.0)) *\
        np.cos(tick/30. + 3 * np.arctan2(XX**2, YY**3)) *\
        np.cos(tick/44. + 7 * np.arctan2(XX, YY))

    Z -= Z.min()
    Z /= Z.max()
    Z *= 256.

    # OpenCV likes uint8
    return np.uint8(Z)

def main():
    """ blurp """
    x = np.linspace(-1, 1, 401)
    y = np.linspace(-1, 1, 301)
    XX, YY = np.meshgrid(x, y)

    for tick in range(1000):
        print tick
        ZZ = funky_image(XX, YY, 8*tick)
        filename = 'imgs/{}.png'.format(1e7 + tick)
        img = cv.applyColorMap(ZZ, cv.COLORMAP_AUTUMN)
        cv.imwrite(filename, img)

if __name__ == '__main__':
    main()
