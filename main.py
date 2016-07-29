import os
import cv2
import sys
import pickle
import numpy as np
from glob import glob
from mayavi import mlab
import multiprocessing as mp
from utils import colors as uc
from utils import amplitudes as ua

# Work off-screen
mlab.options.offscreen = True

def crop_images():
    """ Utility for movie creation """
    paths = glob('imgs/*.png')
    for path in paths:
        img = cv2.imread(path)
        # Negotiate with resolution
        frame = img[250 : 650, 50 : 850, :]
        savepath = 'imgs/cropped/' + os.path.split(path)[1]
        cv2.imwrite(savepath, frame)
        # Show progress
        print savepath

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
            amp[sta : end] = ua.fade_down(note) * note[3]/130.0
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
            dance = note[0] + 8*ua.fade_down(note)
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
        # FIXME pls, maybe some switch statement?
        if len(fade) > 32:
            fade = fade**4
        chord_amps[sta : end] = fade

    return chord_amps

def scores2args(scores):
    """ Change notes into animation defining arguments """
    # Unpack
    scales = scores['scale']
    chords = scores['chord']
    fingers = scores['fingers']
    # FIXME make sure all the fingers notes end at the same tick!
    # First finger, last note, start + length
    last = fingers[0][-1][1] + fingers[0][-1][2]
    full_len = ua.tick2frame(last)

    amps = fingers2amps(fingers)
    champs = chords2champs(chords)
    positions = fingers2poss(fingers)
    color_a, color_b = ua.scales2colors(scales)
    proportions = ua.scales2color_proportions(scales)

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
                  'color_a'     : color_a[it],
                  'color_b'     : color_b[it],
                  'c_prop'      : proportions[it],
                  'tick'        : it}

        out.append(c_dict)

    return out

def rotate_x(y, z, theta):
    """ Rotate around the x-axis """
    y_out = np.cos(theta) * y - np.sin(theta) * z
    z_out = np.sin(theta) * y + np.cos(theta) * z

    return y_out, z_out

def soliton(x, where, sigma = 0.5):
    """ Sine-Gordon equation solutions """
    # This sigma thing does not seem to be doing very much
    out = 4 * np.arctan(np.exp(-(x - where)/np.sqrt(1-sigma)))

    return out

def make_soliton(theta, amp):
    """ Draw soliton, 'multiple-pendulum' style """
    # This makes them rotate arount the x-axis
    y_out = amp * (np.cos(theta) - 1.0)
    z_out = amp * np.sin(theta)

    return y_out, z_out

def make_box():
    """ Needed as axes range setter, due to tha lack of such """
    # Define helpers
    res = 20
    width = 5
    height = 2.1
    depth = 1 * height
    eye = np.ones(res)

    # Draw the 3d box to solve scaling problems
    width_span = np.linspace(-width, width, res)
    height_span = np.linspace(-height, height, res)
    depth_span = np.linspace(-depth, depth, res)

    # TODO Make them black! genius
    r_tube = 1e-9
    # X-dir
    mlab.plot3d(width_span, 0 * eye, - height * eye, tube_radius=r_tube)
    mlab.plot3d(width_span, 0 * eye, + height * eye, tube_radius=r_tube)
    # Y-dir
    mlab.plot3d(- width * eye, depth_span, 0 * eye, tube_radius=r_tube)
    mlab.plot3d(+ width * eye, depth_span, 0 * eye, tube_radius=r_tube)
    # Z-dir
    mlab.plot3d(- width * eye, 0 * eye, height_span, tube_radius=r_tube)
    mlab.plot3d(+ width * eye, 0 * eye, height_span, tube_radius=r_tube)

def make_real_frame(filepath):
    """ Changes raw plots into final movie frame """
    # Create final HD image container
    out = np.zeros((1080, 1920, 3))

    # Load plots
    img = cv2.imread(filepath)

    # Cut what is interesting
    solitons = img[300:480, 370:800, :]

    # Add to frame
    out[900 : 1080, 830 : 1260, :] = solitons

    # FIXME This will not work
    # External video editor will be needed :(
    # Add some text
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_size = 6.0
    font_thickness = 18
    font_color = (255, 255, 255)
    readme = 'AI trying to learn'
    cv2.putText(out,
                readme,
                (0, 160),
                font,
                font_size,
                font_color,
                font_thickness)
    readme = 'progressive metal'
    cv2.putText(out,
                readme,
                (0, 420),
                font,
                font_size,
                font_color,
                font_thickness)

    cv2.imwrite('dupa.png', out)

    return img

def set_camera_position(args):
    """ Filming angles, pro-shot illusions """
    # Extract values
    tick = args['tick']

    # Camera movements improve the 3d feelings
    phi = np.pi * tick / 100.0
    hori = 10 * np.sin(phi/6.66)
    verti = 40 + 18 * np.sin(phi/12.4)

    # Camera settings
    # Horizontal angle [0 : 360]
    azimuth = 66 + hori
    # Zenith angle [0-180]
    elevation = 40 + verti
    mlab.view(azimuth, elevation, 3.0)

def make_single(args):
    """ Mayavi tryouts """
    # De-serialize arguments
    tick = args['tick']
    champ = args['chord_amp']
    finger_amps = args['finger_amps']
    finger_poss = args['finger_poss']
    howmany     = len(finger_amps)

    # Color setup
    proportion  = args['c_prop']
    color_a     = args['color_a']
    color_b     = args['color_b']

    # Generalize
    swing = 0.06 + 0.12* champ

    # Thing angularly about the tick
    phi = np.pi * tick / 6.0

    # Make clear figure
    mlab.clf()

    # Adjust camera position
    set_camera_position(args)
    # Control visual span
    make_box()

    # Create angular solitons
    # This space need to cover the whole piano span
    # TODO Automate range detection
    res = 800
    t = np.linspace(20, 90, res)
    # This is the visual span
    x = np.linspace(-5, 5, res)

    # One 
    for it in range(howmany):
        # Unpack
        amp, pos = finger_amps[it], finger_poss[it]

        # Position (note pitch)
        theta = soliton(t, pos)

        # Prepare stringy
        y, z = make_soliton(theta, amp)

        # Add swing in the middle
        y += swing * np.sin(5*x - 0.2*phi) * np.cos(x - 0.1*phi)
        z += swing * np.cos(5*x - 0.1*phi) * np.cos(x - 0.1*phi)

        # Rotation (note something else?)
        rot = tick/15.0 + it * 2*np.pi/howmany
        y, z = rotate_x(y, z, rot)

        # Color gradient (hand scale?)
        color = np.gradient(theta)

        # Draw a line
        yo = mlab.plot3d(x, y, z, color,
                         # extent = (0, 10, 0, 4, 0, 4),
                         # colormap = 'Blues',
                         vmax = 0.50,
                         vmin = -0.4266,
                         tube_radius=0.04)

        # Make colors scale-dependant
        colors = uc.mixed_colormap(color_a, color_b, proportion)

        # Add opacity
        colors[:, -1] = np.linspace(180, 100, 256)

        # Set customized colors
        yo.module_manager.scalar_lut_manager.lut.table = colors

    # Check for vmax/vmin tuning
    # print max(color), min(color)

    savepath = 'imgs/frame_{}.png'.format(1000000 + tick)
    mlab.savefig(savepath, resolution())

def resolution():
    """ Clever constant """
    # Mayavi performs best when generating squares
    side = 420

    return (side, side)

def main(sector):
    """ blurpf """
    # blompf notes sample PITCH | START | DURATION | VOLUME

    # Point the blompf data
    prefix = 'xc'
    blompf_path = prefix + '_blompf_data.pickle'

    # Get notes
    with open(blompf_path) as fin:
        scores = pickle.load(fin)

    width = 800
    # Generate movie factors
    args = scores2args(scores)[sector * width: (sector+1) * width]

    # One figure is enough for one run?
    # This does not seem like a fine design
    fig = mlab.figure(fgcolor = (1, 1, 1),
                      bgcolor = (0.0, 0.0, 0.0))

    # TODO Make intro
    # simply construct special arglike dictionary
    # to perform some introduction with the same code
    # intro_args = make_intro(args[0])
    # for arg in intro_args:
    #     make_single(arg)

    for arg in args:
        print arg['tick']
        make_single(arg)

if __name__ == '__main__':
    # This is a very not professional paralellization system
    if len(sys.argv) < 2:
        sector = 0
    else:
        sector = int(sys.argv[1])

    print 'Animating sector:', sector
    main(sector)
