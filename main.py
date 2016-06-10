import pickle
import cv2 as cv
import numpy as np
import multiprocessing as mp
from scipy import signal as ss
from utils import signal as us
from utils import shapes as yo
from utils import amplitudes as ua
from matplotlib import pyplot as plt

def norm(this):
    """ Squeeze to 0-1 """
    this -= this.min()
    this /= this.max()
    return this

def funky_image(args):
    """ Generate some funk """
    # De-serialize the arguments
    phi     = args['phi']/5.0
    the     = args['theta']/5.0
    tick    = args['tick']

    # Set resolution
    if False:
        x_res = 1920
        y_res = 1080
    else:
        x_res = 390
        y_res = 280

    # TODO Add at least 2 sound related variables here
    # Manipulate the visibility span
    xspan = 9.5 - 5*np.sin(2*phi) * np.cos(the)
    xleft = -xspan - 0*np.sin(2*phi)
    xright = xspan - 0*np.sin(2*phi)

    # yspan = 9.5 - 5*np.sin(2*phi) * np.cos(the)
    yspan = 1.0 * xspan * y_res/x_res
    yleft = -yspan - 0*np.sin(phi)*np.cos(2*phi)
    yright = yspan - 0*np.sin(phi)*np.cos(2*phi)

    x = np.linspace(xleft, xright, x_res)
    y = np.linspace(yleft, yright, y_res)
    XX, YY = np.meshgrid(x, y)

    # r_shift = 14 + 3 * np.cos(the)
    r_shift = 10 + 4 * abs(ss.sawtooth(the + phi))

    a_hahn = yo.Hahn(k = 0.5, r = 5, m = 25)

    # Some factors
    freqs = [0.5  for it in range(20)]
    lmbds = [5 for it in range(20)]

    # Partial drawings container
    frames = []

    howmany = 7
    for it in range(howmany):
        the += 2.0 * np.pi/howmany
        ax_shift = r_shift * np.cos(the)
        ay_shift = r_shift * np.sin(the)

        # This seem to be adding a nice twist
        # if it == 8:
        #     a_hahn._k = 2

        a_hahn.set_x_shift(ax_shift)
        a_hahn.set_y_shift(ay_shift)
        frames.append(a_hahn.get(XX, YY, tick))

    Z = np.zeros_like(frames[0])

    for frame in frames:
        Z += frame

    # le normalizatione
    Z -= Z.min()
    Z /= Z.max()
    Z = np.sqrt(Z)
    Z *= 110

    # Now when it is normalized to 110 we can adjust some intensities
    # Lets say we want the mean to oscillate around 60
    deficit = 60 - Z.mean()
    Z += deficit
    ids = Z > 110
    Z[ids] -= deficit

    # OpenCV likes uint8
    return np.uint8(np.abs(Z))

def make_single(args):
    """ Parallel ready single image generator """
    # We need this for proper file naming and clear logs
    tick = args['tick']
    print tick

    # Create one frame
    ZZ = funky_image(args)

    # Color it up
    img = cv.applyColorMap(ZZ, cv.COLORMAP_JET)

    # Add diagnostics
    # img = draw_scale(img, args)

    # Save
    filename = 'imgs/{}.png'.format(int(1e7 + tick))
    cv.imwrite(filename, img)

def main():
    """ blurp """
    # blompf notes sample PITCH | START | DURATION | VOLUME

    # Get notes
    with open('jq_blompf_data.pickle') as fin:
        scores = pickle.load(fin)

    notes = scores['hand']

    # Generate movie factors
    args = ua.notes2args(notes)[0:100]

    # Make only first howmany frames
    # args = args[0:200, :]

    pool = mp.Pool(processes = mp.cpu_count())
    pool.map(make_single, args)

if __name__ == '__main__':
    main()
