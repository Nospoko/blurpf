"""
    Set of functions that may be used as basic 2D shapes for
    cymatic constructions from the blompf project note-sets
"""

import numpy as np

class FunkyFunction(object):
    """ Abstract function creating pretty 2D plots """
    def __init__(self, m = 2, n = 2, k = 7, r = 50):
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

    def get(self, x, y, tick):
        """ Call this to get the matrix """
        # Apply shifts
        x += self.x_shift
        y += self.y_shift

        return self.make(x, y, tick)

    def make(self, x, y, tick):
        """ Implement this with some funky functions """
        print 'major fuckup'

class Hahn(FunkyFunction):
    """
    Otto Hahn was a German chemist and pioneer in the fields
    of radioactivity and radiochemistry who won the Nobel Prize
    in Chemistry in 1944 for the discovery and the radiochemical
    proof of nuclear fission.
    """
    def make(self, x, y, tick):
        """ Gets the shape at time tick """
        # Simplify notation
        mm = self._m
        nn = self._n
        kk = self._k
        rr = self._r
        out = np.sin(kk * (x**mm + y**nn) + tick/rr)
        # out = np.sin(kk * (x**mm + y**nn) + np.sin(tick/rr))
        return out

class Fritz(FunkyFunction):
    """
    Friedrich Wilhelm "Fritz" Strassmann was a German chemist
    who, with Otto Hahn in 1938, identified barium in the
    residue after bombarding uranium with neutrons, results
    which, when confirmed, demonstrated the previously unknown
    phenomenon of nuclear fission.
    """
    def make(self, x, y, tick):
        """ Get it """
        # Simplify notation
        mm = self._m
        nn = self._n
        out = (x**2 + y**2) * np.cos(1. * tick/nn + mm * np.arctan2(x, y))
        return out

class Meitner(FunkyFunction):
    """
    Lise Meitner was an Austrian physicist who worked on
    radioactivity and nuclear physics. Otto Hahn and Meitner
    led the small group of scientists who first discovered
    nuclear fission of uranium when it absorbed an extra neutron;
    the results were published in early 1939.
    """
    def make(self, x, y, tick):
        """ yo """
        # Simplify notation
        mm = self._m
        nn = self._n
        out = np.cos(tick/nn + mm * np.arctan2(x, y))
        return out
