import pickle
import numpy as np
from mayavi import mlab
import multiprocessing as mp
from utils import colors as uc
from utils import amplitudes as ua

# Without this graphics must be shown on screen for some reason
# mlab.options.offscreen = True

def scores2args(scores):
    """ Change notes into animation defining arguments """
    # Unpack
    fingers = scores['fingers']
    # FIXME make sure all the fingers notes end at the same tick!
    # First finger, last note, start + length
    last = fingers[0][-1][1] + fingers[0][-1][2]
    full_len = ua.tick2frame(last)

    # Create position parametrization
    positions = []
    for notes in fingers:
        # Prepare container for per-frame parameters
        pos = np.zeros(full_len)
        for note in notes:
            sta, end = ua.get_note_framespan(note)
            pos[sta : end] = note[0]

        positions.append(pos)

    amps = []
    for notes in fingers:
        amp = np.zeros(full_len)
        for note in notes:
            sta, end = ua.get_note_framespan(note)
            amp[sta : end] = ua.fade_down(note)
        amps.append(amp)

    return positions, amps

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
    # This space need to cover the whole piano span
    t = np.linspace(0, 20, res)
    # This is the visual span
    x = np.linspace(-5, 5, res)

    # make_soliton(pos, amp, phase, color)

    # One 
    # Position
    where_a = 10 + 4 * np.cos(5*phi)
    theta_a = soliton(t, where_a)

    y_a = 1.2*np.cos(theta_a)-1 + 0.09 * np.sin(7*x - 3*phi)
    z_a = 1.2*np.sin(theta_a) + 0.01 * np.cos(5*x + 5*phi)

    y_a, z_a = rotate_x(y_a, z_a, tick/17.0)

    # Color gradient
    s_c = np.linspace(0, 1, res)

    yo = mlab.plot3d(x, y_a, z_a, s_c,
                     colormap='Blues',
                     tube_radius=0.04)
    colorpath = 'colormaps/seashore.cmap'
    colors = uc.read_colormap(colorpath, True)
    # opacity manipulation example
    lut = yo.module_manager.scalar_lut_manager.lut.table.to_array()
    # shape = (256, 4) with last row of opacities
    lut[:, -1] = 120
    yo.module_manager.scalar_lut_manager.lut.table = colors

    # Two ...
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

    s_a = np.linspace(0, 1, res)
    s_b = np.linspace(0, 1, res)
    s_d = np.linspace(0, 1, res)

    # Two
    mlab.plot3d(x, y_a, z_a-1, s_a,
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
