import operator


class Vector:
    def __init__(self, components):
        self._comp = components

    def __len__(self):
        return len(self._comp)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self):
            value = self._comp[self.n]
            self.n += 1
            return value
        else:
            raise StopIteration

    def __getitem__(self, item):
        return self._comp[item]

    def __setitem__(self, key, value):
        try:
            self._comp[key] = value
        except IndexError:
            self._comp.append(value)

    def __str__(self):
        return str(self._comp)

    def __repr__(self):
        return str(self._comp)

    def __hash__(self):
        return hash(repr(self))

    def _operator(self, other, comparator):
        if len(self) == len(other):
            return Vector([comparator(x, y) for x, y in zip(self, other)])
        else:
            raise IndexError

    def __eq__(self, other):
        return all([x == y for x, y in zip(self, other)])

    def __add__(self, other):
        return self._operator(other, operator.add)

    def __sub__(self, other):
        return self._operator(other, operator.sub)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self._operator(other, operator.mul)
        elif isinstance(other, int):
            return Vector(list(map(lambda x: x * other, self)))
        elif isinstance(other, float):
            return Vector(list(map(lambda x: x * other, self)))

    def __truediv__(self, other):
        return self._operator(other, operator.truediv)

    def __mod__(self, other):
        return (self + other) * (self ^ other)

    def __xor__(self, other):
        """ Shitty cross product """
        if len(self) == 2 and len(other) == 2:
            return (self[0] * other[1]) - (other[0] * self[1])
        else:
            raise NotImplementedError


def main(iterations):
    from random import sample
    e1, e2 = Vector([0, 1]), Vector([1, 0])
    space = [e1, e2]
    n = 0
    while n < iterations:
        a, b = sample(range(0, len(space)), 2)
        c = space[a] % space[b]
        space.append(c)
        n += 1

    space = list(set(space))
    print(space)

    import matplotlib.pyplot as plt
    plt.scatter([v[0] for v in space], [v[1] for v in space])
    plt.plot(0, 0, 'ok')  # <-- plot a black point at the origin
    plt.axis('equal')  # <-- set the axes to the same scale
    plt.grid(b=True, which='major')
    plt.show()


if __name__ == '__main__':
    main(20)
