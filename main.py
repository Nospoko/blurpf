import pickle
import numpy as np
from mayavi import mlab
import multiprocessing as mp
from utils import amplitudes as ua

# Without this graphics must be shown on screen for some reason
# mlab.options.offscreen = True

def rotate_x(y, z, theta):
    """ Rotate around the x-axis """
    y_out = np.cos(theta) * y - np.sin(theta) * z
    z_out = np.sin(theta) * y + np.cos(theta) * z

    return y_out, z_out

def soliton(x, where):
    """ Sine-Gordon equation solutions """
    v = 0.9
    out = 4 * np.arctan(np.exp(-(x - v * where)/np.sqrt(1-v**2)))

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
    # Zenith angle [0-180]
    azimuth = 69
    elevation = 90 + 0 * np.sin(phi)
    mlab.view(azimuth, elevation, 16.0)

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

    # Create angular solitons
    t = np.linspace(0, 20, res)
    where_a = 10 + 4 * np.cos(5*phi)
    theta_a = soliton(t, where_a)

    where_b = 10 - 4 * np.cos(5*phi)
    theta_b = soliton(t, where_b) + 4*np.pi/3

    where_c = 8 + 7 * np.sin(6*phi)
    theta_c = soliton(t, where_c) + 2*np.pi/3

    x = np.linspace(-5, 5, res)
    # TODO add rotations of given lines and we're golden
    y_red = np.cos(theta_a) + 0.09 * np.sin(7*x - 3*phi)
    z_red = np.sin(theta_a) + 0.1 * np.cos(5*x + 5*phi)

    y_blue = np.cos(theta_b) + 0.13 * np.cos(6*x + 4*phi)
    z_blue = np.sin(theta_b) + 0.12 * np.sin(6*x + 4*phi)
    y_blue, z_blue = rotate_x(y_blue, z_blue, 4*np.pi/3)

    y_green = np.cos(theta_c) + 0.12 * np.sin(8*x + 3*phi)
    z_green = np.sin(theta_c) + 0.11 * np.cos(2*x - 4*phi)
    y_green, z_green = rotate_x(y_green, z_green, 2*np.pi/3)

    s_a = np.gradient(theta_a)
    s_b = np.gradient(theta_b)
    s_c = np.gradient(theta_c)

    # One
    mlab.plot3d(x, y_green, z_green, s_c,
                colormap='Greens',
                tube_radius=0.02)
    # Two
    mlab.plot3d(x, y_red, z_red, s_a,
                colormap='Reds',
                tube_radius=0.02)
    # Three
    mlab.plot3d(x, y_blue, z_blue, s_b,
                colormap='Blues',
                tube_radius=0.02)

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
    args = ua.score2args(scores)[:160]

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
