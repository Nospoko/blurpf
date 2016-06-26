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
    z_a = 2 * np.ones_like(t)
    z_b = -2 * np.ones_like(t)

    z_c = np.zeros_like(t)
    for it in range(10):
        # z_a += 1./(1+it) * np.sin( it*x + 2*phi)
        z_c += 1./(1+it) * np.cos( it*x + 2*phi)

    z_c *= np.exp(-t**2)
    z_c *= 2./max(abs(z_c))

    # z_a *= np.exp(-x**2)
    # z_b *= np.exp(-x**2)
    #
    # z_a /= max(z_a)
    # z_b /= max(z_b)

    s = t

    # extent = [-1, 1, -1, 1, -1, 1]
    mlab.plot3d(x, y, z_a, s)
    mlab.plot3d(x, y, z_b, s)
    mlab.plot3d(y, z_a, x, s)
    mlab.plot3d(y, z_b, x, s)

    mlab.plot3d(x, y, z_c, s)
    mlab.plot3d(x, z_c, y, s)

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
    args = ua.score2args(scores)[0:200]

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
