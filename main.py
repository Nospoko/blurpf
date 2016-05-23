import numpy as np
import scipy.io.wavfile as io
from matplotlib import pyplot as plt

def main():
    """ blurp """
    filepath = 'wavs/PIANO_23_04.wav'
    fs, x = io.read(filepath)

    plt.plot(x[0:1000])
    plt.show()

if __name__ == '__main__':
    main()
