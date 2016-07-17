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
    swing = 0.04 + 0.07* champ

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
    t = np.linspace(20, 90, res)
    # This is the visual span
    x = np.linspace(-5, 5, res)

    # One 
    for it in range(len(finger_amps)):
        # Unpack
        amp, pos = finger_amps[it], finger_poss[it]
        # Constant between fingers
        sigma = 0.4 - 0.35*champ

        # Position (note pitch)
        theta = soliton(t, pos, sigma)

        # Prepare stringy
        y, z = make_soliton(x, theta, amp)

        # Add swing in the middle
        y += swing * np.sin(5*x - 0.3*phi + it * 0*np.pi/5.0)
        z += swing * np.cos(5*x - 0.3*phi + it * 0*np.pi/5.0)

        # Rotation (note something else?)
        rot = tick/15.0 + it * 2*np.pi/5.0
        y, z = rotate_x(y, z, rot)

        # Color gradient (hand scale?)
        color = np.gradient(theta)
        colorpath = 'colormaps/greens.cmap'
        colors = uc.read_colormap(colorpath, True)

        # Change gradient into opacity
        colors[:, -1] = np.linspace(200, 100, 256)

        yo = mlab.plot3d(x, y, z, color,
                         colormap='Blues',
                         tube_radius=0.04)
        # opacity manipulation example
        # lut = yo.module_manager.scalar_lut_manager.lut.table.to_array()
        # shape = (256, 4) with last row of opacities
        yo.module_manager.scalar_lut_manager.lut.table = colors

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
