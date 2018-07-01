import unittest
import imageio
from FitnessFunctions.CompareBinaryImages import CompareBinaryImages
from FitnessFunctions.BinaryImagesDiceIndex import BinaryImagesDiceIndex

class Test_FitnessFunctionTests(unittest.TestCase):

    def test_fitness_should_return_50_percent(self):
        # given
        ref_img = imageio.imread("..\\PSOTests\\TestImages\\ref.png")
        in_img = imageio.imread("..\\PSOTests\\TestImages\\input.png")
        fitness_fun = CompareBinaryImages(ref_img)

        # when
        result = fitness_fun.get_result(in_img)

        # then
        self.assertEqual(result, 0.5)

    def test_dice_index_different_equations(self):
        # given
        ref_img = imageio.imread("..\\PSOTests\\TestImages\\ref.png")
        in_img = imageio.imread("..\\PSOTests\\TestImages\\input.png")
        fitness_fun = BinaryImagesDiceIndex(ref_img)

        # when
        result = fitness_fun.get_result(in_img)
        in_img = BinaryImagesDiceIndex._normalize(in_img)
        ref_img = BinaryImagesDiceIndex._normalize(ref_img)
        intersection = in_img * ref_img     
        complementary = in_img * (1 - ref_img) 


        intersection_pixels = intersection.sum()
        complementary_pixels = complementary.sum()
        ref_sum = ref_img.sum()

        secondary_result = 2 * intersection_pixels / (intersection_pixels + complementary_pixels + ref_sum)
        # then
        self.assertEqual(result, secondary_result)


if __name__ == '__main__':
    unittest.main()
