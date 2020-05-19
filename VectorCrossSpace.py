import matplotlib.pyplot as plt
from Vector import Vector
import itertools
import logging


# Logging: Simple format for displaying info for now
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
    )

logger = logging.getLogger(__name__)


def _plotter(space, dpi, name):
    """ Helper function to plot stuff """
    logger.info("Plotting image")
    plt.rcParams['axes.axisbelow'] = True
    plt.figure(dpi=dpi)
    plt.scatter([v[0] for v in space], [v[1] for v in space], s=(72./dpi)**2, marker='.')
    plt.plot(0, 0, 'ok', markersize=1)
    plt.grid(b=True, which='major')
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    plt.savefig(name)
    logger.info(f"Saved image at {name}")


def main(iterations, basis):
    """
    Basically iterates through each permutation of the space to create vectors using the mod product
    :param iterations: Number of iterations to run (BE CAREFUL!!!! STAY WITHIN 1-4)
    :param basis: Starting vector(s)
    """
    # TODO: Figure out a way to do this with threading, that way we can stop any time
    space = basis
    n = 0
    while n < iterations:
        temp = []
        for vec1, vec2 in itertools.combinations_with_replacement(space, 2):
            c1, c2 = vec1 % vec2, vec2 % vec1
            temp.extend([c1, c2])
        space.extend([v for v in temp if v not in space and len(v) == 2])
        temp.clear()
        n += 1
        logger.info(f"Iteration {n} finished: {len(space)} vectors in space")

    old_len = len(space)
    space = list(set(space))
    logger.info(f"Removed {old_len-len(space)} redundant vectors")
    logger.info(f"Current vector count: {len(space)}")
    _plotter(space, 150, 'vecspace.png')


if __name__ == '__main__':
    main(4, [Vector([1, 0]), Vector([0, 1])])
