import pickle
import cv2 as cv
import numpy as np
import multiprocessing as mp
from utils import colors as uc
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
    # Speed-up useful for debug mode
    speedup = 3
    # De-serialize the arguments
    phi     = speedup * args['phi']
    the     = speedup * args['theta']
    tick    = args['tick']

    # Set resolution
    if False:
        # x_res = 1920
        # y_res = 1080
        x_res = 1280
        y_res = 720
    else:
        x_res = 390
        y_res = 280

    # TODO Add at least 2 sound related variables here
    # Manipulate the visibility span
    xspan = 7.5 - 0*np.sin(2*phi) * np.cos(the)
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

    a_hahn = yo.Hahn(k = 0.5, r = 5, m = 17)

    # Some factors
    freqs = [0.5  for it in range(20)]
    lmbds = [5 for it in range(20)]

    # Partial drawings container
    frames = []

    howmany = 23
    r_shift = 7
    for it in range(howmany):
        the += 2.0 * np.pi/howmany

        ax_shift = r_shift * np.cos(the)
        ay_shift = r_shift * np.sin(the)

        # This seem to be adding a nice twist
        # if it == 8:
        #     a_hahn._k = 2

        a_hahn.set_x_shift(ax_shift)
        a_hahn.set_y_shift(ay_shift)

        # More movements
        a_hahn._n = phi * 5

        # Cumulate
        frames.append(a_hahn.get(XX, YY, tick))

    Z = np.zeros_like(frames[0])

    for frame in frames:
        Z += frame

    # le normalizatione
    treshold = 255
    Z -= Z.min()
    Z /= Z.max()
    Z = np.sqrt(Z)
    Z *= treshold

    # Now when it is normalized to threshold we can adjust some intensities
    # Lets say we want the mean to oscillate around 60
    deficit = 120 - Z.mean()
    Z += deficit
    ids = Z > treshold
    Z[ids] -= deficit

    # OpenCV likes uint8
    return np.uint8(np.abs(Z))

def draw_chord(img, args):
    """ Add chord information """
    # Drawing parameters
    chord_power = args['ch_pow']
    width       = img.shape[1]
    heigh       = img.shape[0]

    l_start = (0,
               int(0.1 * heigh)
               )
    l_stop  = (int(chord_power * width),
               int(0.1 * heigh)
               )

    cv.line(img,
            l_start,
            l_stop,
            (92, 11, 44),
            thickness = 3)

    return img

def draw_scale(img, args):
    """ Add scale information to the image """
    # Extract txt parameters
    c_scale = args['scale']
    height = img.shape[0]

    # Prepare
    txt = 'Current scale is: {}'.format(c_scale)

    # Write
    cv.putText(img,
               txt,
               (10, height - 10),
               cv.FONT_HERSHEY_SIMPLEX,
               0.66,
               (0, 0, 0),
               thickness = 2)

    return img

def color_up(gray, args):
    """ Change flat image into a RGB array """
    # Unpack factors
    tick        = args['tick']
    # TODO Implement all of those!
    proportion  = args['c_prop']
    color_a     = args['color_a']
    color_b     = args['color_b']

    # Color-up to 3D
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

    c_path_a = cmaps[color_a]
    c_path_b = cmaps[color_b]
    cmap_a = uc.read_colormap(c_path_a)
    cmap_b = uc.read_colormap(c_path_b)

    asd = proportion
    cmap = cmap_a * (1.0 - asd) + cmap_b * asd
    cmap = cmap.astype(int)

    # Use colormaps as look-up-tables
    imr = cv.LUT(gray, cmap[:, 0])
    img = cv.LUT(gray, cmap[:, 1])
    imb = cv.LUT(gray, cmap[:, 2])

    out = np.dstack((imr, img, imb))

    return out

def make_single(args):
    """ Parallel ready single image generator """
    # We need this for proper file naming and clear logs
    tick = args['tick']
    print 'Current frame is :', tick

    # Create one frame (1D)
    ZZ = funky_image(args)

    # Add colors
    img = color_up(ZZ, args)

    # Add diagnostics
    DEBUG = not True
    if DEBUG:
        img = draw_scale(img, args)
        img = draw_chord(img, args)

    # Save
    filename = 'imgs/{}.png'.format(int(1e7 + tick))
    cv.imwrite(filename, img)

def main():
    """ blurpf """
    # blompf notes sample PITCH | START | DURATION | VOLUME

    # Point the blompf data
    prefix = 'qb'
    blompf_path = prefix + '_blompf_data.pickle'

    # Get notes
    with open(blompf_path) as fin:
        scores = pickle.load(fin)

    # Generate movie factors
    args = ua.score2args(scores)[0:1000]

    # Parallel
    pool = mp.Pool(processes = mp.cpu_count())
    pool.map(make_single, args)

if __name__ == '__main__':
    main()
