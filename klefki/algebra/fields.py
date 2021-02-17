from abc import abstractproperty
from .abstract import Field
from klefki.algorithms import extended_euclidean_algorithm
from klefki.algorithms import complex_truediv_algorithm
from klefki.algorithms import deg, poly_rounded_div


class FiniteField(Field):

    P = abstractproperty()

    def craft(self, o):
        value = getattr(o, 'value', o)
        if isinstance(value, complex):
            return complex((value.real % self.P), (value.imag % self.P))
        return value % self.P

    def inverse(self):
        return self.__class__(self.P - self.value)

    def mod(self, a, b):
        if isinstance(a, complex):
            return complex((a.real % b), (a.imag % b))
        return a % b

    def sec_inverse(self):
        if isinstance(self.value, complex):
            return complex_truediv_algorithm(complex(1), self.value, self.__class__)

        gcd, x, y = extended_euclidean_algorithm(self.value, self.P)
        assert (self.value * x + self.P * y) == gcd
        # if gcd != 1:
        #     # Either n is 0, or p is not prime number
        #     raise ValueError(
        #         '{} has no multiplicate inverse '
        #         'modulo {}'.format(self.value, self.P)
        #     )
        return self.__class__(x % self.P)

    def op(self, g):
        if isinstance(g, int):
            g = self.type(g)
        return self.__class__(
            self.mod(
                (self.value + g.value), self.P
            )
        )

    def sec_op(self, g):
        if isinstance(g, int):
            g = self.type(g)
        return self.__class__(
            self.mod(
                (self.value * g.value), self.P
            )
        )


class PolyExtField(Field):
    # field
    F = abstractproperty()
    P = abstractproperty()

    def craft(self, value):
        # map Maybe<int> top Field
        if value == 0:
            return self.zero().id
        if value == 1:
            return self.one().id
        if isinstance(value, list):
            assert len(value) == len(self.P)
            return [self.F(p) for p in value]
        # support inner field
        return self.F(value)

    def op(self, rhs):
        if isinstance(rhs, int):
            rhs = self.F(rhs)
        if isinstance(rhs, self.F):
            return self.type([x + rhs for x in self.id])
        return self.type([x + y for x, y in zip(self.id, rhs.id)])

    @classmethod
    def sec_identity(cls):
        return cls([cls.F.one()] + [cls.F.zero()] * (len(cls.P) - 1))

    @classmethod
    def identity(cls):
        return cls([cls.F.zero()] * len(cls.P))

    def inverse(self):
        return self.type([-x for x in self.id])

    def sec_inverse(self):
        field = self.F
        lm, hm = [self.F.one()] + [self.F.zero()] * \
            len(self.P), [self.F.zero()] * (len(self.P) + 1)
        low, high = self.id + [self.F.zero()], [self.F(m)
                                                for m in self.P] + [field(1)]
        while deg(low):
            r = poly_rounded_div(high, low, field)
            r += [field.zero()] * (len(self.P) + 1 - len(r))
            nm = [field(x) for x in hm]
            new = [field(x) for x in high]
            assert len(lm) == len(hm) == len(low) == len(
                high) == len(nm) == len(new) == len(self.P) + 1
            # xt Euclidean alog.
            for i in range(len(self.P) + 1):
                for j in range(len(self.P) + 1 - i):
                    nm[i+j] -= lm[i] * r[j]
                    new[i+j] -= low[i] * r[j]
            lm, low, hm, high = nm, new, lm, low
        return self.type([i / field(low[0]) for i in lm[:len(self.P)]])

    def sec_op(self, rhs):
        if isinstance(rhs, int):
            rhs = self.F(rhs)
        if isinstance(rhs, self.F):
            return self.__class__([c * rhs for c in self.value])
        else:
            degree = len(self.P)
            b = [self.F.zero() for i in range(degree * 2 - 1)]
            inner_enumerate = list(enumerate(rhs.value))

            # mul
            for i, eli in enumerate(self.value):
                for j, elj in inner_enumerate:
                    b[i + j] += eli * elj
            # mod
            for exp in range(len(self.P) - 2, -1, -1):
                top = b.pop()
                for i, c in [(i, c) for i, c in enumerate(self.P) if c]:
                    b[exp + i] -= top * c
            return self.type(b)


PrimeField = FiniteField
Fq = FiniteField
