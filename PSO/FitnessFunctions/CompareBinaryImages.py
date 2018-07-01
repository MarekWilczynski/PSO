from FitnessFunctions.FitnessFunction import FitnessFunction
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

class CompareBinaryImages(FitnessFunction):
    """Fitness function that converts and compares given image to the refential image."""



    def __init__(self, ref_img):        
        super().__init__(self._normalize(ref_img))
        
    def get_result(self, input_image):
        input = self._normalize(input_image)

        # zgodność wymiarów zapewniona na poziomie tworzenia obiektu
        intersection = input * self._reference_image        
        complementary = input * (1 - self._reference_image)  

        intersection_pixels = intersection.sum()
        incorrect_pixels_number = complementary.sum()
        correct_number_of_pixels =  self._reference_image.sum()

        return (intersection_pixels - incorrect_pixels_number)  / correct_number_of_pixels

    