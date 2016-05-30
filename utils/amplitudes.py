import numpy as np

def notes2amps(notes):
    """ Change blompfish notes into blurpish amps """
    # blurp frames per second
    fps = 40

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

def amps2pams(lo, mi, hi):
    """ Changes band amplitudes into per-frame parameters """
    # In the simplest variant just use one band:
    full = lo + mi + hi
    full = np.cumsum(full)

    # Make it go from 0 to 1
    phi = 4*np.pi * full/full[-1]
    the = 4*np.pi * full/full[-1]

    # Enumeration iterator
    its = range(len(full))

    # Make it so every row of output contains parameter
    # values for one frame of the movie
    out = np.column_stack((phi, the, its))

    return out

def notes2args(notes):
    """ Take notes make args lol """
    lo, mi, hi = notes2amps(notes)
    args = amps2pams(lo, mi, hi)

    return args

def funfunfun(note):
    """ Change note into a 1d ADSR kind of function """
    sta, end = get_note_framespan(note)

    # Prepare x axis
    dziedzina = np.linspace(0, 1, end - sta)

    # Make y shape
    out = 0.2 * np.exp(-3.0 * dziedzina)

    # Velocity related renormalization
    out *= note[3]/128.0

    return out

def get_note_framespan(note):
    """ Go from ticks to frames """
    # TODO abstract this out
    tps = 2**5
    fps = 40
    # Ticks
    sta = note[1]
    end = sta + note[2]

    # Seconds .. Frames
    sta /= 1.0 * tps
    end /= 1.0 * tps
    sta *= fps
    end *= fps

    return int(sta), int(end)

