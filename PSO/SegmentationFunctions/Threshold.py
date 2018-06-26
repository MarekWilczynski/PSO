from SegmentationFunctions.SegmentationFunction import SegmentationFunction

import cv2 as cv

class Threshold(SegmentationFunction):
    """Function thresholding in python"""    
    
    def __init__(self, input_img):
        super().__init__(input_img)
        
    def get_result(self, parameters_vector):
        
        binary_image = cv.threshold(self._input_image, parameters_vector[0], 255, cv.THRESH_BINARY) 

        return binary_image[1]


