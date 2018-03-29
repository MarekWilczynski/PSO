import unittest

import Utilities.SegmentationThreader as Threader

from Classic import Classic as Swarm
from Particles.Particle import Particle

import cv2 as cv
from Swarms.Classic import Classic
from DataInitialization.ParticleFactory import ParticleFactory
from DataInitialization.PSObuilder import PSObuilder
from SegmentationFunctions.Threshold import Threshold
from FitnessFunctions.BinaryImagesDiceIndex import BinaryImagesDiceIndex
from numpy import array


class Test_UtilitiesTests(unittest.TestCase):
    def test_should_update_values(self):
         # given
        img = cv.imread("..\\PSOTests\\TestImages\\threshold_test.jpg", 0)
        lower_threshold = 130
        upper_threhshold = 255
        thresholded = cv.threshold(img, lower_threshold, upper_threhshold, cv.THRESH_BINARY)
        thresholded = thresholded[1] # strange value on index #1
        fitness_fun = BinaryImagesDiceIndex(thresholded)

        # when        
        particles = [Particle([120 + (15 * x), 150 + (x * 15)]) for x in range(5)]

        threaders = [Threader.SegmentationThreader(Threshold(img), p) for p in particles]

        for t in threaders:
            t.start()

        for t in threaders:
            t.join()

        for t in threaders:
            t._particle.fitness = fitness_fun.get_result(t.segmentation_result)
        # then

        particle_changed = [p.fitness != 0 for p in particles]

        self.assertTrue(all( particle_changed))

if __name__ == '__main__':
    unittest.main()
