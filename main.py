import pickle
import numpy as np
from mayavi import mlab
import multiprocessing as mp
from utils import colors as uc
from utils import amplitudes as ua

# Work off-screen
# mlab.options.offscreen = True

def fingers2amps(fingers):
    """ Another esoteric transformator """
    amps = []
    # FIXME pls how not to load this everywhere
    last = fingers[0][-1][1] + fingers[0][-1][2]
    full_len = ua.tick2frame(last)

    for notes in fingers:
        amp = np.zeros(full_len)
        for note in notes:
            sta, end = ua.get_note_framespan(note)
            amp[sta : end] = ua.fade_down(note)
        amps.append(amp)

    return amps

def fingers2poss(fingers):
    """ More """
    positions = []
    # FIXME pls how not to load this everywhere
    last = fingers[0][-1][1] + fingers[0][-1][2]
    full_len = ua.tick2frame(last)

    for notes in fingers:
        # Prepare container for per-frame parameters
        pos = np.zeros(full_len)
        for note in notes:
            # TODO any kind of transition can be put in here ...
            sta, end = ua.get_note_framespan(note)
            dance = note[0] + 4*ua.fade_down(note)
            pos[sta : end] = dance

        positions.append(pos)

    return positions

def chords2champs(chords):
    """ Chord amps """
    # FIXME pls how not to load this everywhere
    last = chords[-1][1] + chords[-1][2]
    full_len = ua.tick2frame(last)

    chord_amps = np.zeros(full_len)
    for note in chords:
        sta, end = ua.get_note_framespan(note)
        fade = ua.fade_down(note)
        if len(fade) > 16:
            fade = fade**4
        chord_amps[sta : end] = fade

    return chord_amps

def scores2args(scores):
    """ Change notes into animation defining arguments """
    # Unpack
    chords = scores['chord']
    fingers = scores['fingers']
    # FIXME make sure all the fingers notes end at the same tick!
    # First finger, last note, start + length
    last = fingers[0][-1][1] + fingers[0][-1][2]
    full_len = ua.tick2frame(last)

    positions = fingers2poss(fingers)
    amps = fingers2amps(fingers)
    champs = chords2champs(chords)

    # Prepare dict to share
    out = []
    # Time tick loop
    for it in range(full_len):
        famps = []
        fposs = []
        # Finger loop
        for jt in range(len(fingers)):
            famps.append(amps[jt][it])
            fposs.append(positions[jt][it])

        c_dict = {'finger_amps' : famps,
                  'finger_poss' : fposs,
                  'chord_amp'   : champs[it],
                  'tick'        : it}

        out.append(c_dict)

    return out

def rotate_x(y, z, theta):
    """ Rotate around the x-axis """
    y_out = np.cos(theta) * y - np.sin(theta) * z
    z_out = np.sin(theta) * y + np.cos(theta) * z

    return y_out, z_out

def soliton(x, where, sigma = 0.2):
    """ Sine-Gordon equation solutions """
    out = 4 * np.arctan(np.exp(-(x - where)/np.sqrt(1-sigma)))

    return out

def make_soliton(x, theta, amp):
    """ Draw soliton, 'multiple-pendulum' style """
    y_out = amp * (np.cos(theta) - 1.0)
    z_out = amp * np.sin(theta)

    return y_out, z_out

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

    # Camera settings
    # Horizontal angle [0 : 360]
    azimuth = 69 + 3 * tick % 360
    # Zenith angle [0-180]
    elevation = 90
    mlab.view(azimuth, elevation, 16.0)

def make_single(args):
    """ Mayavi tryouts """
    res = 600

    # De-serialize arguments
    tick = args['tick']
    champ = args['chord_amp']
    finger_amps = args['finger_amps']
    finger_poss = args['finger_poss']

    # Generalize
    swing = 0.07 + 0.06* champ

    # This is fake phi
    phi = np.pi * tick / 4.0

    # Make clear figure
    mlab.clf()

    # Adjust camera position
    set_camera_position(args)
    # Control visual span
    make_box()

    # Create angular solitons
    # This space need to cover the whole piano span
    t = np.linspace(30, 80, res)
    # This is the visual span
    x = np.linspace(-5, 5, res)

    # One 
    # Position (note pitch)
    where_a = finger_poss[0]
    sigma_a = 0.4 - 0.35*champ
    theta_a = soliton(t, where_a, sigma_a)

    # Size (note volume)
    amp_a = 2 * finger_amps[0]

    # Prepare stringy
    y_a, z_a = make_soliton(x, theta_a, amp_a)

    # Add middle swing
    y_a += swing * np.sin(5*x - 0.3*phi)
    z_a += swing * np.cos(5*x - 0.3*phi)

    # Rotation (note something else?)
    rot_a = tick / 15.0
    y_a, z_a = rotate_x(y_a, z_a, rot_a)

    # Color gradient (hand scale?)
    color_a = np.gradient(theta_a)
    colorpath = 'colormaps/seashore.cmap'
    colors = uc.read_colormap(colorpath, True)

    yo = mlab.plot3d(x, y_a, z_a, color_a,
                     colormap='Blues',
                     tube_radius=0.04)
    # opacity manipulation example
    lut = yo.module_manager.scalar_lut_manager.lut.table.to_array()
    # shape = (256, 4) with last row of opacities
    lut[:, -1] = 120
    yo.module_manager.scalar_lut_manager.lut.table = colors


    # Two ...
    where_b = finger_poss[1]
    theta_b = soliton(t, where_b)

    amp_b = finger_amps[1]
    y_blue = amp_b * (np.cos(theta_b)-1.0) +\
              swing* np.sin(5*x - 0.3*phi - np.pi/3.0)

    z_blue = amp_b * np.sin(theta_b) +\
              swing* np.cos(5*x - 0.3*phi - np.pi/3.0)
    y_blue, z_blue = rotate_x(y_blue, z_blue, 2*np.pi/5 + tick/15.0)

    s_b = np.gradient(theta_b)

    mlab.plot3d(x, y_blue, z_blue, s_b,
                colormap='Blues',
                tube_radius=0.039)

    where_c = finger_poss[2]
    theta_c = soliton(t, where_c)

    amp_c = 1.5 * finger_amps[2]
    y_green = amp_c * (np.cos(theta_c)-1.0) +\
              swing* np.sin(5*x - 0.3*phi - 2*np.pi/3.0)

    z_green = amp_c * np.sin(theta_c) +\
              swing* np.cos(5*x - 0.3*phi - 2*np.pi/3.0)
    y_green, z_green = rotate_x(y_green, z_green, 4*np.pi/5 + tick/15.0)

    s_c = np.gradient(theta_c)

    mlab.plot3d(x, y_green, z_green, s_c,
                colormap='Blues',
                tube_radius=0.035)

    savepath = 'imgs/frame_{}.png'.format(1000000 + tick)
    mlab.savefig(savepath)

def main():
    """ blurpf """
    # blompf notes sample PITCH | START | DURATION | VOLUME

    # Point the blompf data
    prefix = 'xk'
    blompf_path = prefix + '_blompf_data.pickle'

    # Get notes
    with open(blompf_path) as fin:
        scores = pickle.load(fin)

    # Generate movie factors
    args = scores2args(scores)[:]

    # Not parallel
    # FIXME how to make full-hd
    mlab.figure(fgcolor=(1, 1, 1), bgcolor=(0, 0, 0), size=(700, 700))

    for arg in args:
        print arg['tick']
        make_single(arg)

if __name__ == '__main__':
    main()
