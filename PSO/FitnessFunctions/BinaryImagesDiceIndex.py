from FitnessFunctions.FitnessFunction import FitnessFunction
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

class BinaryImagesDiceIndex(FitnessFunction):
    """Fitness function that converts and compares given image to the refential image."""
    
    def __init__(self, ref_img):        
        super().__init__(self._normalize(ref_img))
        
    def get_result(self, input_image):
        input = self._normalize(input_image)

        # zgodność wymiarów zapewniona na poziomie tworzenia obiektu
        intersection = input * self._reference_image

        intersection_pixels = intersection.sum()
        input_pixels = input.sum()
        reference_pixels =  self._reference_image.sum()

        return (2 * intersection_pixels) / ( input_pixels + reference_pixels) 

    

