import numpy as np

def notes2amps(notes):
    """ Change blompfish notes into blurpish amps """
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

def notes2args(notes):
    """ Take notes make args lol """
    phi, the = notes2angles(notes)

    # Per-frame arguments
    out = []
    for it in range(len(the)):
        c_dict = {'phi' : phi[it], 'theta' : the[it], 'tick' : it}
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

