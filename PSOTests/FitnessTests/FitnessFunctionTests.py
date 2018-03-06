import unittest
import imageio
from FitnessFunctions.CompareBinaryImages import CompareBinaryImages

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

if __name__ == '__main__':
    unittest.main()
