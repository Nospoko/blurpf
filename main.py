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
    res = 500
    eye = np.ones(res)

    # De-serialize arguments
    phi = args['phi'] * 5
    tick = args['tick']

    # Make clear figure
    mlab.clf()

    # Camera angle?
    mlab.view(90.0, 70 + 2*tick, 16.0)

    # Draw the 3d box to solve scaling problems
    box_span = np.linspace(-5, 5, res)
    # X-dir
    mlab.plot3d(box_span, 0 * eye, - 5 * eye, tube_radius=0.00001)
    mlab.plot3d(box_span, 0 * eye, + 5 * eye, tube_radius=0.00001)
    # Y-dir
    mlab.plot3d(- 5 * eye, box_span, 0 * eye, tube_radius=0.00001)
    mlab.plot3d(+ 5 * eye, box_span, 0 * eye, tube_radius=0.00001)
    # Z-dir
    mlab.plot3d(- 5 * eye, 0 * eye, box_span, tube_radius=0.00001)
    mlab.plot3d(+ 5 * eye, 0 * eye, box_span, tube_radius=0.00001)

    x = np.linspace(-5, 5, res)

    t = np.linspace(0, 10, res)
    where = 5 + 4 * np.cos(5*phi)
    theta = soliton(t, where)

    where_b = 5 - 4 * np.cos(5*phi)
    theta += soliton(t, where_b)

    y_c = 0.4*np.cos(theta) + 0.1 * np.sin(7*x - 3*phi)
    z_c = 0.5*np.sin(theta) + 0.1 * np.cos(5*x + 5*phi)

    s = np.gradient(theta)

    # mlab.plot3d(x, y_c, z_c, s, colormap='Blues')
    mlab.plot3d(x, y_c, z_c, s, colormap='Greens', tube_radius=0.02)
    mlab.plot3d(x, y_c -0.2, z_c+0.3, s, colormap='Reds', tube_radius=0.02)
    mlab.plot3d(x, y_c+0.2, z_c-0.3, s, colormap='Blues', tube_radius=0.02)
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
    args = ua.score2args(scores)[:60]

    # Not parallel
    # FIXME how to make hd aspect-ratio?
    mlab.figure(fgcolor=(1, 1, 1), bgcolor=(0, 0, 0), size=(700, 700))

    for arg in args:
        print arg['tick']
        make_single(arg)

    # Parallel
    # pool = mp.Pool(processes = 1)
    # pool.map(make_single, args)

if __name__ == '__main__':
    main()
