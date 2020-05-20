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
    plt.scatter([v[0] for v in space],
                [v[1] for v in space],
                s=2,
                marker='.',
                alpha=0.4)
    plt.plot(0, 0, 'ok', markersize=1)
    plt.grid(b=True, which='major')
    plt.xlim(-1.01, 1.01)
    plt.ylim(-1.01, 1.01)
    plt.savefig(name)
    logger.info(f"Saved image at {name}")


def main(iterations, basis):
    """
    Basically iterates through each combination of the space to create vectors using the mod product
    :param iterations: Number of iterations to run (BE CAREFUL!!!! STAY WITHIN 1-4)
    :param basis: Starting vector(s)
    """
    space = basis
    n = 0
    while n < iterations:
        temp = []
        for vec1, vec2 in itertools.combinations_with_replacement(space, 2):
            if vec1 != vec2:
                c = vec1 % vec2
                if c not in space and c not in temp:
                    temp.append(c)
                    temp.append(-c)
        space.extend(temp)
        n += 1
        logger.info(f"Iteration {n} finished: {len(space)} vectors in space")

    logger.info(f"Current vector count: {len(space)}")
    _plotter(space, 150, 'vecspace.png')


if __name__ == '__main__':
    main(4, [Vector([1, 0]), Vector([0, 1])])
