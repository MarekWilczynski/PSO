from SegmentationFunctions.MatlabSegmentationFunction import MatlabSegmentationFunction
import matlab
from cv2 import getStructuringElement
from matlab.engine import start_matlab

from math import floor

from Utilities.NumericalToObjectConverter import NumericalToObjectConverter

class KidneyCystSegmentationMultipleImages(KidneyCystSegmentationMultipleImages):
    
    def __init__(self, input_img):
        """input image is a list of file names in RenCystSegmentation"""
        super().__init__(input_img)
        
    def get_result(self, parameters_vector):
        dice_sum = 0;

        for path in self._input_image:                     
            dice_sum = dice_sum + super().get_result(parameters_vector)
        return dice_sum