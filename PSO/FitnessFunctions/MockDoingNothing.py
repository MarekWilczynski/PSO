from FitnessFunctions.FitnessFunction import FitnessFunction
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

class MockDoingNothing(FitnessFunction):
    """A mock that does nothing, but allows to calculate fitness in matlab"""

    def _normalize(self, binary_img):        
        return
    
    def __init__(self, ref_img):        
        return
        
    def get_result(self, value):
        return value

    

