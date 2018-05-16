from SegmentationFunctions.MatlabSegmentationFunction import MatlabSegmentationFunction
import matlab
from cv2 import getStructuringElement
from matlab.engine import start_matlab

from math import floor

from Utilities.NumericalToObjectConverter import NumericalToObjectConverter

class KidneyCystSegmentation(MatlabSegmentationFunction):
    """Lungs segmentation by IiAM PolSl"""

    _spacing = []
    _segmentation_function = []
    _to_matlab_double = matlab.double
    
    def __init__(self, input_img):
        """Input image written in string. Sending 3d image through IO would take too long"""
        self._input_image = input_img
        print("Matlab engine initialization started")
        self._matlab_eng = start_matlab() 
        
        # changing directory to the one with matlab functions
        self._matlab_eng.cd("..\\PSO\\MatlabFiles\\RenCystSeg")       
        
        print("Matlab engine initialization finished")

        self._segmentation_function = self._matlab_eng.python_RenCystSeg
        
    def get_result(self, parameters_vector):      
        params_floored = list(parameters_vector)
        params_floored[9] = floor(params_floored[9])
        params_floored[10] = floor(params_floored[10])
        binary_image = self._segmentation_function(self._input_image, self._to_matlab_double(params_floored))
        return binary_image