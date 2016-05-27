import cv2 as cv
import numpy as np
import multiprocessing as mp
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
    phi = 4*np.pi * 2 * tick/2500.0
    the = 2*np.pi * 2 * tick/1250.0

    r_shift = 16 + 3.0 * np.cos(the)

    a_hahn = yo.Hahn(k = 0.5, r = 5, m = 10)

    # Some factors
    freqs = [0.5  for it in range(20)]
    lmbds = [5 for it in range(20)]

    # Partial drawings container
    frames = []

    howmany = 15
    for it in range(howmany):
        phi += 2.0 * np.pi/howmany
        ax_shift = r_shift * np.cos(phi)
        ay_shift = r_shift * np.sin(phi)

        a_hahn.set_x_shift(ax_shift)
        a_hahn.set_y_shift(ay_shift)
        frames.append(a_hahn.get(XX, YY, tick))


    Z = np.empty_like(frames[0])

    for frame in frames:
        Z += frame

    # le normalizatione
    Z -= Z.min()
    Z /= Z.max()
    Z *= 140 + 64 * np.cos(phi)

    # OpenCV likes uint8
    return np.uint8(Z)

def make_single(tick):
    """ Parallel ready single image generator """
    print tick
    if False:
        x_res = 1920
        y_res = 1080
    else:
        x_res = 590
        y_res = 440

    xspan = 8.5 + 0*np.cos(2.0 * tick/100)
    yspan = 8.5 + 0*np.cos(2.0 * tick/100)
    x = np.linspace(-xspan, xspan, x_res)
    y = np.linspace(-yspan, yspan, y_res)
    XX, YY = np.meshgrid(x, y)

    ZZ = funky_image(XX, YY, tick)
    filename = 'imgs/{}.png'.format(int(1e7 + tick))
    img = cv.applyColorMap(ZZ, cv.COLORMAP_JET)
    cv.imwrite(filename, img)

def main():
    """ blurp """
    # blompf notes sample PITCH | START | DURATION | VOLUME
    notes = [[45, 0, 8, 70],
             [48, 0, 8, 69],
             [53, 0, 8, 69],
             [35, 0, 8, 72],
             [43, 8, 16, 69],
             [50, 8, 16, 68],
             [53, 8, 16, 68]]

    tick_range = range(100)
    pool = mp.Pool(processes = mp.cpu_count())
    pool.map(make_single, tick_range)

if __name__ == '__main__':
    main()
