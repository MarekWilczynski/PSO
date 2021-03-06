from SegmentationFunctions.MatlabSegmentationFunction import MatlabSegmentationFunction
import matlab

class ThresholdMatlab(MatlabSegmentationFunction):
    """Fitness function that thresholds given image using matlab"""

    
    def __init__(self, input_img):
        super().__init__(input_img)
        
    def get_result(self, parameters_vector):
        params_converted = matlab.double(parameters_vector)

        input_converted = self._input_image

        binary_image = self._matlab_eng.Threshold(params_converted, input_converted)
        # TODO: przekazac matlab.engine.nazwa_funkcji bezposrednio do pola klasy CompareBinaryImages
        return binary_image