import matplotlib.pyplot as plt
import operator
import itertools
import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
    )

logger = logging.getLogger(__name__)


class Vector:
    """
    Vector Class

    Supports:
    - Iteration
    - Hashing
    - Arithmetic
    - Dot and 'Cross' Products
    - Special 'Mod' Product
    """

    def __init__(self, components):
        self._comp = components

    def __len__(self):
        """ Number of components in vector """
        return len(self._comp)

    def __iter__(self):
        """ Makes the vector an iterable """
        self.n = 0
        return self

    def __next__(self):
        """ Allows for iteration """
        if self.n < len(self):
            value = self._comp[self.n]
            self.n += 1
            return value
        else:
            raise StopIteration

    def __getitem__(self, item):
        """ Allows component at index """
        return self._comp[item]

    def __setitem__(self, key, value):
        """ Allows setting component at index """
        try:
            self._comp[key] = value
        except IndexError:
            self._comp.append(value)

    def __str__(self):
        """ Pretty print """
        return str(self._comp)

    def __repr__(self):
        """ Useful print """
        return str(self._comp)

    def __hash__(self):
        """ Makes Vector unique """
        return hash(repr(self))

    def __abs__(self):
        """ Returns magnitude of vector"""
        return (sum([i**2 for i in self._comp]))**0.5

    def _operator(self, other, comparator):
        """ Helper function to reduce code in operations """
        if len(self) == len(other):
            return Vector([comparator(x, y) for x, y in zip(self, other)])
        else:
            logger.error(f"self and other have unequal length")
            raise IndexError

    def __eq__(self, other):
        """ Equality """
        return all([x == y for x, y in zip(self, other)])

    def __add__(self, other):
        """ Addition """
        return self._operator(other, operator.add)

    def __sub__(self, other):
        """ Subtraction """
        return self._operator(other, operator.sub)

    def __mul__(self, other):
        """ Dot product """
        if isinstance(other, Vector):
            return self._operator(other, operator.mul)
        elif isinstance(other, int):
            return Vector(list(map(lambda x: x * other, self)))
        elif isinstance(other, float):
            return Vector(list(map(lambda x: x * other, self)))

    def __truediv__(self, other):
        """ Component by component division """
        return self._operator(other, operator.truediv)

    def __mod__(self, other):
        """ Self defined mod product
            It makes a vector using addition, then scales it so that the vectors length is equal to the area subtended
            Basically 2D cross product
        """
        try:
            return (self + other) * ((self ^ other) / (abs(self + other)))
        except ZeroDivisionError:
            return self

    def __xor__(self, other):
        """ Xross product
        Essentially the determinant
        """
        if len(self) == 2 and len(other) == 2:
            return (self[0] * other[1]) - (other[0] * self[1])
        else:
            raise NotImplementedError


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

    olen = len(space)
    space = list(set(space))
    logger.info(f"Removed {olen-len(space)} redundant vectors")
    logger.info(f"Current vector count: {len(space)}")
    _plotter(space, 150, 'vecspace.png')


if __name__ == '__main__':
    main(4, [Vector([1, 0]), Vector([0, 1])])
