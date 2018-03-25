from math import floor

class NumericalToObjectConverter(object):
    """A class that allows convert numerical data to a string"""

    _strings = []

    def __init__(self, strings):
        self._strings = strings

    def get_object(self, index):
        i = floor(index)
        if(i < 0 or i > len(self._strings)):
            raise ValueError("Index out of bounds!")
        return self._strings[i]



