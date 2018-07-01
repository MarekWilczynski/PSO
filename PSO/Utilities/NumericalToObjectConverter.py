from math import floor

class NumericalToObjectConverter(object):
    """A class that allows convert numerical data to a string"""

    _objects = []

    def __init__(self, objects):
        self._objects = objects

    def get_object(self, index):
        i = floor(index)
        if(i < 0 or i > len(self._objects)):
            raise ValueError("Index out of bounds!")
        return self._objects[i]



