from abc import ABCMeta as abstract, abstractmethod
import numpy as np

class FitnessFunction(metaclass = abstract):
    """Abstract class, representing the fitness function. Is it being used by PSO to comput the fitness value."""

    _reference_image = []

    # TODO: jest jednolinijkowiec. To pewnie wolno działa
    # self niekonieczny, by działalo @staticmethod
    # 
    # https://stackoverflow.com/questions/8904694/how-to-normalize-a-2-dimensional-numpy-array-in-python-less-verbose

    @staticmethod
    def _normalize(binary_img):
        numpy_img = np.array(binary_img)
        normalized = numpy_img / numpy_img.max()

        normalized[normalized == np.inf] = 0
        normalized[np.isnan(normalized)] = 0

        return normalized

    @abstractmethod
    def __init__(self, reference_image):
        self._reference_image = reference_image
        # changing directory to the one with matlab functions  

    @abstractmethod
    def get_result(input_image):
        return