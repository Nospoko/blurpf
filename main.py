import pickle
import numpy as np
from mayavi import mlab
import multiprocessing as mp
from utils import amplitudes as ua

# Without this graphics must be shown on screen for some reason
# mlab.options.offscreen = True

def make_single(args):
    """ Mayavi tryouts """
    # De-serialize arguments
    phi = args['phi'] * 5
    tick = args['tick']

    # Make clear figure
    mlab.clf()

    t = np.linspace(-3.14, 3.14, 500)

    x = t
    y = np.zeros_like(t)
    eye = np.ones_like(t)
    yo = np.linspace(-1, 1, 500)

    z_c = np.cos(0.7*t + 2*phi) * np.sin(1.4*t - 2*phi) / (1+np.sin(t)**2)
    y_c = np.sin(t + 3 * phi) * np.cos(0.5 *t - 2*phi) / (1+np.sin(t)**2)

    z_c *= np.exp(-t**2)
    z_c *= 1./max(abs(z_c))

    y_c *= np.exp(-t**2)
    y_c *= 1./max(abs(y_c))

    s = t

    # extent = [-1, 1, -1, 1, -1, 1]
    mlab.plot3d(x, y, 2*eye)
    mlab.plot3d(x, y, -2*eye)
    mlab.plot3d(-3.14*eye, y, 2*yo)
    mlab.plot3d(3.14*eye, y, 2*yo)
    mlab.plot3d(3.14*eye, 2*yo, 2*eye)
    mlab.plot3d(-3.14*eye, 2*yo, 2*eye)


    mlab.plot3d(x, y_c, z_c, s)
    mlab.plot3d(x, y_c, - z_c, np.cos(s))

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
    args = ua.score2args(scores)[:20]

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
