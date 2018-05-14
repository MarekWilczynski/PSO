import unittest
import imageio
import numpy as np
import time

from itertools import chain

from FitnessFunctions.CompareBinaryImages import CompareBinaryImages
from FitnessFunctions.MockDoingNothing import MockDoingNothing

from SegmentationFunctions.ThresholdMatlab import ThresholdMatlab
from SegmentationFunctions.KidneyCystSegmentation import KidneyCystSegmentation

import collections

from operator import mul, add

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

class Test_MatlabSegmentationFunctionTests(unittest.TestCase):

    def test_matlab_should_return_50_percent(self):
        # given
        ref_img = imageio.imread("..\\PSOTests\\TestImages\\ref.png")
        in_img = imageio.imread("..\\PSOTests\\TestImages\\input.png")
        fitness_fun = CompareBinaryImages(ref_img)
        segmentation_fun = ThresholdMatlab(in_img)
        treshhold = 0.5
        
        # when
        binary_image = segmentation_fun.get_result([treshhold], ref_img)
        fitness_val = fitness_fun.get_result(binary_image)

        # then
        self.assertEqual(fitness_val, 0.5)

    def test_matlab_3d_kidney_cysts_segmentation(self):
        # given        
        file_name = "104_12_c"
        img_name = file_name
        input_img = img_name  + ".mha"      

        segmentation_fun = KidneyCystSegmentation(file_name)
       
        fitness_fun = MockDoingNothing([])

        seg_result = segmentation_fun.get_result([40, 4.0, 0.15, 1.0, 0.02, 0.5, 1.0, 0.075, 1, 0, 2])
        fitness_val = fitness_fun.get_result(seg_result)
       
        # then
        expected_value = 0.7477
        self.assertAlmostEqual(fitness_val, expected_value, 3)
        
    def test_matlab_average_performance(self):
        perform = False
        if(perform):
            # given
            in_img = imageio.imread("..\\PSOTests\\TestImages\\input.png")
            ref_img = imageio.imread("..\\PSOTests\\TestImages\\ref.png")

            segmentation_fun = ThresholdMatlab(in_img)
            treshhold = 0.5
            for i in range(1,100):
                # when
                fitness_val = segmentation_fun.get_result([treshhold], ref_img)
        # then
        self.assertEqual(perform, True, "Nie przeprowadzono testu! Aby tego dokonać, zmienić flagę!")

if __name__ == '__main__':
    unittest.main()



