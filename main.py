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

def make_box():
    """ Needed as axes range setter, due to tha lack of such """
    # Define helpers
    res = 20
    width = 5
    eye = np.ones(res)

    # Draw the 3d box to solve scaling problems
    box_span = np.linspace(-width, width, res)

    # TODO Make them black! genius
    r_tube = 1e-8
    # X-dir
    mlab.plot3d(box_span, 0 * eye, - width * eye, tube_radius=r_tube)
    mlab.plot3d(box_span, 0 * eye, + width * eye, tube_radius=r_tube)
    # Y-dir
    mlab.plot3d(- width * eye, box_span, 0 * eye, tube_radius=r_tube)
    mlab.plot3d(+ width * eye, box_span, 0 * eye, tube_radius=r_tube)
    # Z-dir
    mlab.plot3d(- width * eye, 0 * eye, box_span, tube_radius=r_tube)
    mlab.plot3d(+ width * eye, 0 * eye, box_span, tube_radius=r_tube)

def set_camera_position(args):
    """ Filming angles, pro-shot illusions """
    # Extract values
    tick = args['tick']
    tick = 119
    phi = args['phi'] * 5

    # Camera settings
    # Horizontal angle [0 : 360]
    azimuth = 69 + 3 * tick % 360
    # Zenith angle [0-180]
    elevation = 90 + 0 * np.sin(phi)
    mlab.view(azimuth, elevation, 16.0)

def make_single(args):
    """ Mayavi tryouts """
    res = 500

    # De-serialize arguments
    phi = args['phi'] * 5
    tick = args['tick']

    # Make clear figure
    mlab.clf()

    # Adjust camera position
    set_camera_position(args)
    # Control visual span
    make_box()

    # Create angular solitons
    t = np.linspace(0, 20, res)
    x = np.linspace(-5, 5, res)

    where_a = 10 + 4 * np.cos(5*phi)
    theta_a = soliton(t, where_a)
    # TODO add rotations of given lines and we're golden
    y_red = 1.2*np.cos(theta_a)-1 + 0.09 * np.sin(7*x - 3*phi)
    z_red = 1.2*np.sin(theta_a) + 0.01 * np.cos(5*x + 5*phi)
    y_red, z_red = rotate_x(y_red, z_red, tick/17.0)

    where_b = 10 - 4 * np.cos(5*phi)
    theta_b = soliton(t, where_b)

    y_blue = 1.4*np.cos(theta_b)-1.2 + 0.03 * np.cos(6*x + 4*phi)
    z_blue = np.sin(theta_b) + 0.02 * np.sin(6*x + 4*phi)
    y_blue, z_blue = rotate_x(y_blue, z_blue, 2*np.pi/5 + tick/13.0)

    where_c = 8 + 7 * np.sin(6*phi)
    theta_c = soliton(t, where_c) + 0*np.pi/3

    y_green = 1.5*np.cos(theta_c)-1.3 + 0.02 * np.sin(8*x + 3*phi)
    z_green = 1.5*np.sin(theta_c) + 0.01 * np.cos(2*x - 4*phi)
    y_green, z_green = rotate_x(y_green, z_green, 4*np.pi/5 + tick/15.0)

    where_d = 12 + 6 * np.sin(8*phi)
    theta_d = soliton(t, where_d) + 0*np.pi/3

    y_pink = 1.3*np.cos(theta_d)-1.1 + 0.02 * np.sin(8*x + 3*phi)
    z_pink = 1.3*np.sin(theta_d) + 0.04 * np.cos(2*x - 4*phi)
    y_pink, z_pink = rotate_x(y_pink, z_pink, 6*np.pi/5 + tick/20.0)

    s_a = np.gradient(theta_a)
    s_b = np.gradient(theta_b)
    s_c = np.gradient(theta_c)
    s_d = np.gradient(theta_d)

    # One
    mlab.plot3d(x, y_green, z_green, s_c,
                colormap='Blues',
                tube_radius=0.04)
    # Two
    mlab.plot3d(x, y_red, z_red, s_a,
                colormap='Blues',
                tube_radius=0.034)
    # Three
    mlab.plot3d(x, y_blue, z_blue, s_b,
                colormap='Blues',
                tube_radius=0.039)
    # 4 
    mlab.plot3d(x, y_pink, z_pink, s_d,
                colormap='Blues',
                tube_radius=0.035)

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
    args = ua.score2args(scores)[:]

    # Not parallel
    # FIXME how to make full-hd
    mlab.figure(fgcolor=(1, 1, 1), bgcolor=(0, 0, 0), size=(700, 700))

    for arg in args:
        print arg['tick']
        make_single(arg)

    # Parallel
    # pool = mp.Pool(processes = 1)
    # pool.map(make_single, args)

if __name__ == '__main__':
    main()
