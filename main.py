import pickle
import multiprocessing as mp
from utils import amplitudes as ua
from tryouts import concentric as tc

def main():
    """ blurpf """
    # blompf notes sample PITCH | START | DURATION | VOLUME

    # Point the blompf data
    prefix = 'qb'
    blompf_path = prefix + '_blompf_data.pickle'

    # Get notes
    with open(blompf_path) as fin:
        scores = pickle.load(fin)

    # Generate movie factors
    args = ua.score2args(scores)[0:100]

    # Parallel
    pool = mp.Pool(processes = mp.cpu_count())
    pool.map(tc.make_single, args)

if __name__ == '__main__':
    main()
