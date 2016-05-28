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

    howmany = 9
    for it in range(howmany):
        phi += 2.0 * np.pi/howmany
        ax_shift = r_shift * np.cos(phi)
        ay_shift = r_shift * np.sin(phi)

        if it == 8:
            a_hahn._k = 2

        a_hahn.set_x_shift(ax_shift)
        a_hahn.set_y_shift(ay_shift)
        frames.append(a_hahn.get(XX, YY, tick))

    Z = np.zeros_like(frames[0])

    for frame in frames:
        Z += frame

    # le normalizatione
    Z -= Z.min()
    Z /= Z.max()
    Z *= 140 + 64 * np.cos(phi**2)

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

    xspan = 6.5 + 2*np.cos(2.0 * np.pi * tick/100)
    yspan = 6.5 + 2*np.cos(2.0 * np.pi * tick/100)
    x = np.linspace(-xspan, xspan, x_res)
    y = np.linspace(-yspan, yspan, y_res)
    XX, YY = np.meshgrid(x, y)

    ZZ = funky_image(XX, YY, tick)
    filename = 'imgs/{}.png'.format(int(1e7 + tick))
    img = cv.applyColorMap(ZZ, cv.COLORMAP_JET)
    cv.imwrite(filename, img)

def notes2amps(notes):
    """ Change blompfish notes into blurpish amps """
    # blurp frames per second
    fps = 24

    # blompf ticks per second (this was found empirically wtf)
    tps = 2**5

    # Make sure notes are properly arranged
    notes.sort(key = lambda x: x[1] + x[2])

    # Prepare LO/MI/HI containers
    # Movie length in blompf ticks
    full_len = notes[-1][1] + notes[-1][2]
    # in seconds
    full_len /= 1.0 * tps

    # Finally frames
    full_len *= fps
    full_len = int(full_len)

    # For now we want to create a 3-range visualizer thing
    lo_amp = np.zeros(full_len)
    mi_amp = np.zeros(full_len)
    hi_amp = np.zeros(full_len)

    for note in notes:
        if note[0] < 45:
            sta, end = get_note_framespan(note)
            lo_amp[sta : end] += funfunfun(note)
        elif note[0] < 75:
            sta, end = get_note_framespan(note)
            mi_amp[sta : end] += funfunfun(note)
        else:
            sta, end = get_note_framespan(note)
            hi_amp[sta : end] += funfunfun(note)

    return lo_amp, mi_amp, hi_amp

def funfunfun(note):
    """ Change note into a 1d ADSR kind of function """
    sta, end = get_note_framespan(note)

    # Prepare x axis
    dziedzina = np.linspace(0, 1, end - sta)

    # Make y shape
    out = np.exp(-dziedzina)

    return out

def get_note_framespan(note):
    """ Go from ticks to frames """
    # TODO abstract this out
    tps = 2**5
    fps = 24
    # Ticks
    sta = note[1]
    end = sta + note[2]

    # Seconds .. Frames
    sta /= 1.0 * tps
    end /= 1.0 * tps
    sta *= fps
    end *= fps

    return int(sta), int(end-1)

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
