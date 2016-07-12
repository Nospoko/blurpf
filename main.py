import pickle
import numpy as np
from mayavi import mlab
import multiprocessing as mp
from utils import amplitudes as ua

# Without this graphics must be shown on screen for some reason
# mlab.options.offscreen = True

def soliton(x, t):
    """ Sine-Gordon equation solutions """
    v = 0.9
    out = 4 * np.arctan(np.exp(-(x - v * t)/np.sqrt(1-v**2)))

    return out

def make_single(args):
    """ Mayavi tryouts """
    # De-serialize arguments
    phi = args['phi'] * 5
    tick = args['tick']

    # Make clear figure
    mlab.clf()

    res = 500

    x = np.linspace(-3.1399, 3.14, res)

    y = np.zeros_like(x)
    eye = np.ones_like(x)
    yo = np.linspace(-1, 1, res)

    t = np.linspace(0, 10, res)
    where = 2 + 6 * tick/100.0
    theta = soliton(t, where)

    where_b = 8 - 6 * tick/100.0
    theta += soliton(t, where_b)

    y_c = np.cos(theta)
    z_c = np.sin(theta)

    s = np.gradient(theta)

    # extent = [-1, 1, -1, 1, -1, 1]
    mlab.plot3d(1.2*x, y, 3*eye)
    mlab.plot3d(1.2*x, y, -3*eye)

    mlab.plot3d(-1.2*3.14*eye, y, 3*yo)
    mlab.plot3d(1.2*3.14*eye, y, 3*yo)

    mlab.plot3d(1.2*3.14*eye, 2*yo, 2*eye)
    mlab.plot3d(-1.2*3.14*eye, 2*yo, 2*eye)


    # mlab.plot3d(x, y_c, z_c, s, colormap='Blues')
    mlab.plot3d(x, y_c, z_c, s, colormap='Greens', tube_radius=0.02)
    # mlab.plot3d(x, y_c + 2, z_d, s, colormap='Reds')

    savepath = 'imgs/frame_{}.png'.format(1000000 + tick)
    mlab.savefig(savepath)

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
    args = ua.score2args(scores)[:100]

    # Not parallel
    # FIXME how to make hd aspect-ratio?
    mlab.figure(fgcolor=(1, 1, 1), bgcolor=(0, 0, 0), size=(600, 600))
    # Camera angle?
    mlab.view(80.0, 70.0, 16.0)

    for arg in args:
        print arg['tick']
        make_single(arg)

    # Parallel
    # pool = mp.Pool(processes = 1)
    # pool.map(make_single, args)

if __name__ == '__main__':
    main()
