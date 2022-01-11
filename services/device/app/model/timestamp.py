from dateutil import parser

from ..util.exceptions import RLException


class InvalidTimestamp(RLException):
    def __init__(self, h, m, s, ds):
        self.h = h
        self.m = m
        self.s = s
        self.ds = ds


class Timestamp():

    @classmethod
    def from_components(cls, h, m, s, ds):
        if (
            not (0 <= h)
            or not (0 <= m <= 59)
            or not (0 <= s <= 59)
            or not (0 <= ds <= 9)
        ):
            raise InvalidTimestamp(h, m, s, ds)
        total_seconds = h * 3600 + m * 60 + s + ds * 0.1
        return cls(total_seconds)

    @classmethod
    def from_datetime_delta(cls, datetime1, datetime2):
        return Timestamp((datetime1 - datetime2).total_seconds())

    @classmethod
    def from_isostring_delta(cls, isostring1, isostring2):
        return Timestamp.from_datetime_delta(
            parser.parse(isostring1),
            parser.parse(isostring2)
        )

    @classmethod
    def evenly_spaced(cls, n, interval):
        for i in range(n):
            yield cls(i * interval)

    def __init__(self, total_seconds):
        self._total_seconds = total_seconds

    def __lt__(self, other):
        return self._total_seconds < other._total_seconds

    def __eq__(self, other):
        return self._total_seconds == other._total_seconds

    def __le__(self, other):
        return self < other or self == other

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __add__(self, other):
        return Timestamp(self._total_seconds + other._total_seconds)

    def __sub__(self, other):
        return Timestamp(self._total_seconds - other._total_seconds)

    @property
    def h(self):
        return int(
            self._total_seconds / 3600
        )

    @property
    def m(self):
        return int(
            (self._total_seconds - self.h * 3600) / 60
        )

    @property
    def s(self):
        return int(
            self._total_seconds - self.m * 60 - self.h * 3600
        )

    @property
    def ds(self):
        return int(
            (self._total_seconds - self.s - self.m * 60 - self.h * 3600) * 10
        )

    @property
    def datetime(self):
        ...

    @property
    def isostring(self):
        ...

    def __repr__(self):
        return f"{self.h}:{self.m:02d}:{self.s:02d}.{self.ds}"
