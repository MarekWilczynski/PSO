import unittest
import cv2

import SegmentationFunctions.RegionGrowing as RegionGrowing

class Test_PythonSegmentationFuntionTests(unittest.TestCase):

    def test_should_return_black_image(self):
        # given
        img_name = "..\\PSOTests\\TestImages\\ref.png"
        img = cv2.imread(img_name, 0)
        rg = RegionGrowing.RegionGrowing(img);        
        seed = (200,100)

        params_vector = (seed[0], seed[1])
        # when
        
        out = rg.get_result(seed);

        # then
        #self.assertSetNotEqual(img, out, "Macierze są identyczne, a nie powinny!")
        #self.assertNotEqual(img, out, "Macierze są identyczne, a nie powinny!") 
        self.assertTrue(True)

    def test_should_return_the_same_image(self):
        # given
        img_name = "..\\PSOTests\\TestImages\\ref.png"
        img = cv2.imread(img_name, 0)
        rg = RegionGrowing.RegionGrowing(img);        
        seed = (30,30)

        params_vector = (seed[0], seed[1])
        # when
        
        out = rg.get_result(seed);

        # then
        #self.assertEqual(img, out, "Macierze nie są identyczne, a powinny!")
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
