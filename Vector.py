import operator
import logging


# Logging: Simple format for displaying info for now
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

    def get_comp(self):
        return self._comp

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
        return self.get_comp()[item]

    def __setitem__(self, key, value):
        """ Allows setting component at index """
        try:
            self._comp[key] = value
        except IndexError:
            self._comp.append(value)

    def __str__(self):
        """ Pretty print """
        return str(self.get_comp())

    def __repr__(self):
        """ Useful print """
        return str(self.get_comp())

    def __hash__(self):
        """ Makes Vector unique """
        return hash(repr(self))

    def __abs__(self):
        """ Returns magnitude of vector"""
        return (sum([i**2 for i in self.get_comp()]))**0.5

    def _operator(self, other, comparator):
        """ Helper function to reduce code in operations """
        if len(self) == len(other):
            return Vector([comparator(x, y) for x, y in zip(self.get_comp(), other.get_comp())])
        else:
            logger.error(f"self and other have unequal length")
            raise IndexError

    def __eq__(self, other):
        """ Equality """
        if isinstance(other, Vector):
            return all([x == y for x, y in zip(self.get_comp(), other.get_comp())])
        elif isinstance(other, list):
            return all([x == y for x, y in zip(self.get_comp(), other)])
        else:
            return False

    def __neg__(self):
        return Vector([-x for x in self.get_comp()])

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
            return Vector(list(map(lambda x: x * other, self.get_comp())))
        elif isinstance(other, float):
            return Vector(list(map(lambda x: x * other, self.get_comp())))

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
