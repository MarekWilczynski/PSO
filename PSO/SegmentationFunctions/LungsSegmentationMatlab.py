from SegmentationFunctions.MatlabSegmentationFunction import MatlabSegmentationFunction
import matlab
from cv2 import getStructuringElement

from math import floor

from Utilities.NumericalToObjectConverter import NumericalToObjectConverter

class LungsSegmentationMatlab(MatlabSegmentationFunction):
    """Lungs segmentation by Pawel Badura"""

    _spacing = []
    _converter = []
    _segmentation = []
    _to_matlab_double = matlab.double
    
    def __init__(self, input_img, spacing, se_types):
        self._spacing = matlab.double(list(map(float, spacing)))
        self._converter = NumericalToObjectConverter(se_types)
        super().__init__(input_img)        
        self._segmentation = self._matlab_eng.Fun_SMP_SegmentacjaPluc
        
    def get_result(self, parameters_vector):

        params_rounded = map(floor, parameters_vector)
        params_rounded = list(map(int, params_rounded))

        threshhold = params_rounded[0]
        object_to_remove_size = params_rounded[1]  # square object of size a^2, where a is the parameter value
        #se_1 = getStructuringElement(self._converter.get_object(params_rounded[2]),(params_rounded[3],params_rounded[4]))
        #se_2 = getStructuringElement(self._converter.get_object(params_rounded[5]),(params_rounded[6],params_rounded[7]))
        #se_3 = getStructuringElement(self._converter.get_object(params_rounded[8]),(params_rounded[9],params_rounded[10]))
        #se_4 = getStructuringElement(self._converter.get_object(params_rounded[11]),(params_rounded[12],params_rounded[13]))
        #se_5 = getStructuringElement(self._converter.get_object(params_rounded[14]),(params_rounded[15],params_rounded[16]))

        se_1 = [self._converter.get_object(params_rounded[2]), params_rounded[3]]
        se_2 = [self._converter.get_object(params_rounded[4]), params_rounded[5]]
        se_3 = [self._converter.get_object(params_rounded[6]), params_rounded[7]]
        se_4 = [self._converter.get_object(params_rounded[8]), params_rounded[9]]
        se_5 = [self._converter.get_object(params_rounded[10]), params_rounded[11]]

        binary_image = self._segmentation(self._spacing, threshhold, object_to_remove_size, se_1, se_2, se_3, se_4, se_5)
        return binary_image