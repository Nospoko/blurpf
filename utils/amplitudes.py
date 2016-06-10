import numpy as np

def notes2amps(notes):
    """ Change blompfish notes into blurpish amps """
    # FIXME from here to the full_len usage everything is shit
    # blurp frames per second
    fps = 30

    # blompf ticks per second (this was found empirically wtf)
    tps = 2**5

    # Make sure notes are properly arranged
    notes.sort(key = lambda x: x[1] + x[2])

    # Prepare LO/MI/HI containers
    # Movie length in blompf ticks
    full_len = notes[-1][1] + notes[-1][2]
    # in seconds
    full_len /= 1.0 * tps

    # Finally frames
    full_len *= fps
    full_len = int(full_len)

    # For now we want to create a 3-range visualizer thing
    lo_amp = np.zeros(full_len)
    mi_amp = np.zeros(full_len)
    hi_amp = np.zeros(full_len)

    for note in notes:
        if note[0] < 45:
            sta, end = get_note_framespan(note)
            lo_amp[sta : end] += funfunfun(note)
        elif note[0] < 65:
            sta, end = get_note_framespan(note)
            mi_amp[sta : end] += funfunfun(note)
        else:
            sta, end = get_note_framespan(note)
            hi_amp[sta : end] += funfunfun(note)

    return lo_amp, mi_amp, hi_amp

def chords2angle(chords):
    """ Prepare lenght of some kind of cunt-down-ish line """
    # Calculate total number of frames in this blurpf animation
    full_len = tick2frame(chords[-1][1] + chords[-1][2])
    full_len = int(full_len)

    # Prepare output
    chord_p = np.zeros(full_len)

    for chord in chords:
        sta, end = get_note_framespan(chord)
        # Make it countdown from one to whatever
        curv = funfunfun(chord)
        curv /= curv.max()

        chord_p[sta : end] = curv

    return chord_p

def scales2words(scales):
    """ Change blompf scale data into view-able information """
    # Calculate total number of frames in this blurpf animation
    full_len = tick2frame(scales[-1][1] + scales[-1][2])
    full_len = int(full_len)

    # Prepare lyrics
    scale_names = {
                60 : 'C',
                61 : 'Cis',
                62 : 'D',
                63 : 'Dis',
                64 : 'E',
                65 : 'F',
                66 : 'Fis',
                67 : 'G',
                68 : 'Gis',
                69 : 'A',
                70 : 'Ais',
                71 : 'H',
                72 : 'C'
                }

    # Pre-alocate 
    scale_numbers = np.chararray(full_len)

    for scale in scales:
        sta, end = get_note_framespan(scale)
        scale_numbers[sta : end] = scale_names[scale[0]]

    return scale_numbers

def notes2angles(notes):
    """ Create 2 dimensional parametrization from the blompf hand-notes"""
    lo, mi, hi = notes2amps(notes)

    # In the simplest variant you can just use one band:
    full = lo + mi + hi
    full = np.cumsum(full)

    # But multiple are prefered
    lom = lo + mi
    lom = np.cumsum(lom)

    mih = mi + hi
    mih = np.cumsum(mih)

    # Make it go from 0 to 1
    phi = 4*np.pi * lom/lom[-1]
    the = 4*np.pi * mih/mih[-1]

    return phi, the

def score2args(score):
    """ Take notes make args lol """
    # Deserialize blompf data
    notes   = score['hand']
    scales  = score['scale']
    chords  = score['chord']

    # Main movement generators
    phi, the = notes2angles(notes)

    # Print scales on the image for debug agility
    scale_numbers = scales2words(scales)

    # Prepare chord powers
    chord_powers = chords2angle(chords)

    # Per-frame arguments
    out = []
    for it in range(len(the)):
        c_dict = {'phi'     : phi[it],
                  'theta'   : the[it],
                  'scale'   : scale_numbers[it],
                  'ch_pow'  : chord_powers[it],
                  'tick'    : it}
        out.append(c_dict)

    return out

def funfunfun(note):
    """ Change note into a 1d ADSR kind of function """
    sta, end = get_note_framespan(note)
    lon = end - sta

    # Prepare x axis
    dziedzina = np.linspace(0, 1, lon)

    # Make y shape
    # out = 0.2 * np.exp(-3.0 * dziedzina)

    do_me = (dziedzina - 0.1) / 0.5
    out = 0.1 + 0.2 * np.exp(-do_me**2)**2

    # Velocity related renormalization
    if note[3] < 90:
        out *= 0.5

    # FIXME why is this here?
    out *= 32.0 / lon

    return out

def get_note_framespan(note):
    """ Go from ticks to frames """
    # Ticks
    sta = tick2frame(note[1])
    end = sta + tick2frame(note[2])

    return int(sta), int(end)

def tick2frame(tick):
    """ Change time base """
    # Those are constants
    tps = 2**5
    fps = 30

    out = 1.0 * tick / tps
    out *= fps

    return int(out)

