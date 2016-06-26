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
    phi = args['phi'] * 10
    tick = args['tick']

    # Make clear figure
    mlab.clf()

    x = np.linspace(-3, 3, 500)

    y = 2*np.cos(x + 2*phi)
    z = np.sin( 3*x + 3*phi) + np.sin(2*x  + phi)
    s = np.abs(x)/3 + 1

    # extent = [-10, 10, -1, 1, -1, 1]
    mlab.plot3d(x, y, z, s)

    savepath = 'imgs/frame_{}.png'.format(1000000 + tick)
    mlab.savefig(savepath)

def main():
    """ blurpf """
    # blompf notes sample PITCH | START | DURATION | VOLUME

    # Point the blompf data
    prefix = 'jx'
    blompf_path = prefix + '_blompf_data.pickle'

    # Get notes
    with open(blompf_path) as fin:
        scores = pickle.load(fin)

    # Generate movie factors
    args = ua.score2args(scores)[0:500]

    # Not parallel
    mlab.figure(fgcolor=(1, 1, 1), bgcolor=(0, 0, 0), size=(600, 600))
    mlab.view(80.0, 70.0, 16.0)
    for arg in args:
        print arg['tick']
        make_single(arg)

    # Parallel
    # pool = mp.Pool(processes = 1)
    # pool.map(make_single, args)

if __name__ == '__main__':
    main()
