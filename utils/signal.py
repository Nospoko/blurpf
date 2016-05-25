import numpy as np
import scipy.io.wavfile as io

def read_wav():
    fs, x = io.read(filepath)

    return fs, x

def get_stereo(filepath = 'wavs/PIANO_23_04.wav'):
    """ Read into 2 np.arrays (no mono) """
    fs, x = io.read(filepath)

    print 'sampling rate: ', fs

    return x[:, 0], x[:, 1]

