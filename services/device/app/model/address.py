import re

from ..util.exceptions import RLException


class AddressException(RLException):
    def __init__(self, address_string):
        self.address_string = address_string


class AddressSyntaxError(AddressException):
    def __init__(self, address_string):
        super().__init__(address_string)


class Address():

    _RE_PROGRAMS = {
        'letter': re.compile(r"(?P<letter>[A-Za-z])"),
        'number': re.compile(r"([A-Za-z])(?P<number>[0-9]|(1[0-5]))(:|$)"),
        'range': re.compile(r"(:)(?P<range>[1-4])")
    }

    def __init__(self, address_string):
        self._address_string = address_string.lower()
        self._extract_components()
        self._validate_address()

    def _extract_components(self):
        letter_match = self._RE_PROGRAMS['letter'].search(self._address_string)
        number_match = self._RE_PROGRAMS['number'].search(self._address_string)
        range_match = self._RE_PROGRAMS['range'].search(self._address_string)

        if letter_match is None or number_match is None:
            raise AddressSyntaxError(self._address_string)

        self._letter = letter_match.group('letter').lower()
        self._number = int(number_match.group('number'))
        self._range = 1 if range_match is None \
            else int(range_match.group('range'))

    def _validate_address(self):
        ...  # TODO