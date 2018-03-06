from abc import ABCMeta as abstract, abstractmethod
import numpy as np

class FitnessFunction(metaclass = abstract):
    """Abstract class, representing the fitness function. Is it being used by PSO to comput the fitness value."""

    _reference_image = []

    @abstractmethod
    def __init__(self, reference_image):
        self._reference_image = reference_image
        # changing directory to the one with matlab functions  

    @abstractmethod
    def get_result(input_image):
        return