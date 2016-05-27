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
    the = 8*np.pi * 2 * tick/1250.0

    r_shift = 16 + 3.0 * np.cos(the)

    ax_shift = r_shift * np.cos(phi)
    ay_shift = r_shift * np.sin(phi)

    a_hahn = yo.Hahn(k = 0.5, m = 12)
    a_hahn.set_x_shift(ax_shift)
    a_hahn.set_y_shift(ay_shift)
    Za = a_hahn.get(XX, YY, tick)

    bx_shift = r_shift * np.cos(phi - np.pi * 2./3)
    by_shift = r_shift * np.sin(phi - np.pi * 2./3)

    b_hahn = yo.Hahn(k = 0.5, m = 12)
    b_hahn.set_x_shift(bx_shift)
    b_hahn.set_y_shift(by_shift)
    Zb = b_hahn.get(XX, YY, tick)

    cx_shift = r_shift * np.cos(phi + np.pi * 2./3)
    cy_shift = r_shift * np.sin(phi + np.pi * 2./3)

    c_hahn = yo.Hahn(k = 0.5, m = 12)
    c_hahn.set_x_shift(cx_shift)
    c_hahn.set_y_shift(cy_shift)
    Zc = c_hahn.get(XX, YY, tick)

    dx_shift = r_shift * np.cos(phi + np.pi)
    dy_shift = r_shift * np.sin(phi + np.pi)

    d_hahn = yo.Hahn(k = 0.5, m = 12)
    d_hahn.set_x_shift(dx_shift)
    d_hahn.set_y_shift(dy_shift)
    Zd = d_hahn.get(XX, YY, tick)

    ex_shift = r_shift * np.cos(phi + np.pi/3)
    ey_shift = r_shift * np.sin(phi + np.pi/3)

    d_hahn.set_x_shift(ex_shift)
    d_hahn.set_y_shift(ey_shift)
    Ze = d_hahn.get(XX, YY, tick)

    fx_shift = r_shift * np.cos(phi - np.pi/3)
    fy_shift = r_shift * np.sin(phi - np.pi/3)

    d_hahn.set_x_shift(fx_shift)
    d_hahn.set_y_shift(fy_shift)
    Zf = d_hahn.get(XX, YY, tick)

    Z = norm(Za) + norm(Zb) + norm(Zc) + norm(Zd) + norm(Ze) + norm(Zf)

    # Z = 3 * norm(Za) + \
    #         norm(Zb) * 1.5 * (1 + 0.5 * np.cos(phi - np.pi/2)) + \
    #         norm(Zc) * 2 * np.cos(phi) ** 2

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

    xspan = 8.5 + 4*np.cos(2.0 * tick/100)
    yspan = 8.5 + 4*np.cos(2.0 * tick/100)
    x = np.linspace(-xspan, xspan, x_res)
    y = np.linspace(-yspan, yspan, y_res)
    XX, YY = np.meshgrid(x, y)

    ZZ = funky_image(XX, YY, tick)
    filename = 'imgs/{}.png'.format(int(1e7 + tick))
    img = cv.applyColorMap(ZZ, cv.COLORMAP_RAINBOW)
    cv.imwrite(filename, img)

def main():
    """ blurp """
    # blompf notes sample PITCH | START | DURATION | VOLUME
    notes = [[45, 0, 8, 70],
             [43, 8, 16, 69],
             [43, 24, 8, 70],
             [47, 32, 4, 70],
             [52, 36, 4, 69],
             [55, 40, 2, 69],
             [59, 42, 2, 67],
             [64, 44, 4, 69]]

    tick_range = range(1000)
    pool = mp.Pool(processes = mp.cpu_count())
    pool.map(make_single, tick_range)

if __name__ == '__main__':
    main()
