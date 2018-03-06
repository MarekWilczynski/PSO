import unittest
import imageio
import numpy as np

from FitnessFunctions.CompareBinaryImages import CompareBinaryImages
from SegmentationFunctions.ThresholdMatlab import ThresholdMatlab

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
