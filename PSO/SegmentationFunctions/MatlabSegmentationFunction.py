from abc import ABCMeta as abstract, abstractmethod

import matlab
from matlab.engine import start_matlab

import numpy
import os
import SegmentationFunctions.SegmentationFunction as base



class MatlabSegmentationFunction(base.SegmentationFunction, metaclass = base.abstract):
    """Abstract class, representing the fitness function. Is it being used by PSO to compute the fintess value using Matlab."""

    _input_image = []
    _matlab_eng = []

    @abstractmethod
    def __init__(self, input_image):
        super().__init__(matlab.double(input_image.tolist()))

        self._matlab_eng = start_matlab() 

        # changing directory to the one with matlab functions
        self._matlab_eng.cd("..\\PSO\\MatlabFiles")
        
    @abstractmethod
    def get_result(parameters_vector):
        return 0;