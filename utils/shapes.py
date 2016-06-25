"""
    Set of functions that may be used as basic 2D shapes for
    cymatic constructions from the blompf project note-sets
"""

import numpy as np

class FunkyFunction(object):
    """ Abstract function creating pretty 2D plots """
    def __init__(self, m = 2, n = 2, k = 7, r = 20):
        """ Keep it up to 4 factors per function? """
        # Two ints
        self._m = m
        self._n = n
        # Two floats
        self._k = float(k)
        self._r = float(r)
        # Zero fucks

        # Also allow shifting
        self.x_shift = 0
        self.y_shift = 0

    def get(self, x, y):
        """ Call this to get the matrix """
        # x and y must be copied to apply shifts safely
        xx = np.empty_like(x)
        yy = np.empty_like(y)
        xx[:] = x
        yy[:] = y

        # Apply shifts
        xx += self.x_shift
        yy += self.y_shift

        return self.make(xx, yy)

    def make(self, x, y):
        """ Implement this with some funky functions """
        print 'major fuckup'

    def set_x_shift(self, howfar):
        """ Where to """
        self.x_shift = howfar

    def set_y_shift(self, howfar):
        """ Where to """
        self.y_shift = howfar

class Hahn(FunkyFunction):
    """
    Otto Hahn was a German chemist and pioneer in the fields
    of radioactivity and radiochemistry who won the Nobel Prize
    in Chemistry in 1944 for the discovery and the radiochemical
    proof of nuclear fission.
    """
    def make(self, x, y):
        """ Gets the shape """
        # Simplify notation
        mm = self._m
        nn = self._n
        kk = self._k * 0.3
        rr = self._r

        rad = np.sqrt(x**2 + y**2)

        phase_shift = nn
        out = np.zeros_like(rad)

        # evens = range(-mm, mm)[2::2]
        evens = range(-mm, mm)

        for it in evens:
            # out += 1.0/kk * np.cos(it/kk * rad + phase_shift)
            out += 1.0/kk * np.sin(it/kk * rad + phase_shift)

        return out**1

class Fritz(FunkyFunction):
    """
    Friedrich Wilhelm "Fritz" Strassmann was a German chemist
    who, with Otto Hahn in 1938, identified barium in the
    residue after bombarding uranium with neutrons, results
    which, when confirmed, demonstrated the previously unknown
    phenomenon of nuclear fission.
    """
    def make(self, x, y):
        """ Get it """
        # Simplify notation
        mm = self._m
        nn = self._n
        out = (x**2 + y**2) * np.cos(mm * np.arctan2(x, y))
        return out

class Meitner(FunkyFunction):
    """
    Lise Meitner was an Austrian physicist who worked on
    radioactivity and nuclear physics. Otto Hahn and Meitner
    led the small group of scientists who first discovered
    nuclear fission of uranium when it absorbed an extra neutron;
    the results were published in early 1939.
    """
    def make(self, x, y):
        """ yo """
        # Simplify notation
        mm = self._m
        nn = self._n
        out = np.sin(x*y) * np.cos(mm * np.arctan2(x, y))
        return out

