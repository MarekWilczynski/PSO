from abc import ABCMeta as abstract, abstractmethod


class SegmentationFunction(metaclass = abstract):
    """Abstract class, representing the fitness function. Is it being used by PSO to comput the fintess value"""

    _input_image = []
    _matlab_eng = []

    @abstractmethod
    def __init__(self, input_image):
        self._input_image = input_image

    @abstractmethod
    def get_result(parameters_vector):
        return 0;