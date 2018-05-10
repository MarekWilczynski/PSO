import unittest
import imageio
import numpy as np
import time

from itertools import chain

from FitnessFunctions.CompareBinaryImages import CompareBinaryImages
from FitnessFunctions.BinaryImagesDiceIndex import BinaryImagesDiceIndex

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
        img_name = "Obrazy\\" + file_name
        input_img = img_name  + ".mha"       
        
        start = time.time()
        segmentation_fun = KidneyCystSegmentation(file_name)
        print('Initialization time: %5.3f s' % (time.time() - start))
        
        start = time.time()
       # ref_img = segmentation_fun._matlab_eng.python_load_ref_img(img_name + "_t.mha" )
        print('Loading ref image time: %5.3f s' % (time.time() - start))
        #s = ref_img.size

        start = time.time()
       # ref_img = list( chain.from_iterable( chain.from_iterable( ref_img)))
        #ref_img = [val for row in ref_img for col in row for val in col]
        # [val for row in chain.from_iterable(ref_img) for col in chain.from_iterable(row) for val in chain.from_iterable(col)]
        # 
        print('Flattening ref image time: %5.3f s' % (time.time() - start))

        start = time.time()
        #ref_img = np.array(ref_img)
        print('Reshaping ref image time: %5.3f s' % (time.time() - start))

        #start = time.time()
        #ref_img = ref_img.reshape(s)
        #print('Reshaping ref image time: %5.3f s' % (time.time() - start))
        # when

        start = time.time()
        binary_image = segmentation_fun.get_result([])
        print('Segmentation time: %5.3f s' % (time.time() - start))

        start = time.time()
        #binary_image = [val for row in binary_image for col in row for val in col]
        binary_image = list( chain.from_iterable( chain.from_iterable( binary_image)))
        print('Flattening bin image time: %5.3f s' % (time.time() - start))

        #start = time.time()
        #binary_image = np.array(binary_image)
        #print('Converting bin image to numpy array time: %5.3f s' % (time.time() - start))

        #start = time.time()
        #binary_image = binary_image.reshape(s)
        #print('Reshaping bin image time: %5.3f s' % (time.time() - start))
        
        input = binary_image
       # _reference_image = ref_img

        #intersection = input * _reference_image        
        #complementary = input * (1 - _reference_image)  

        #intersection_pixels = intersection.sum()
        #incorrect_pixels_number = complementary.sum()
        #correct_number_of_pixels = _reference_image.sum()
        test = sum(input)
        start = time.time()
        intersection = map(mul, input, _reference_image)        
        complementary = map(mul, input , [1 - x for x in _reference_image])
        test = sum(input)

        intersection_pixels = sum(intersection)
        incorrect_pixels_number = sum(complementary)
        correct_number_of_pixels = sum( _reference_image)

        fitness_val = (2 * intersection_pixels) / ( correct_number_of_pixels + incorrect_pixels_number + intersection_pixels) 
        print('Math time: %5.3f s' % (time.time() - start))

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



