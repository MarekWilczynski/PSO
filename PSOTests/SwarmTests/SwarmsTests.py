import unittest
from Classic import Classic as Swarm
from Particles.Particle import Particle

import cv2 as cv
from Swarms.Classic import Classic
from DataInitialization.ParticleFactory import ParticleFactory
from DataInitialization.PSObuilder import PSObuilder
from SegmentationFunctions.Threshold import Threshold
from FitnessFunctions.CompareBinaryImages import CompareBinaryImages
from numpy import array

def proper_thresholds(particles_vector):
        # function used for additional constraints
        for particle in particles_vector:
            if(particle.parameters_vector[0] > particle.parameters_vector[1]):
                tmp = particle.parameters_vector[0]
                particle.parameters_vector[0] = particle.parameters_vector[1]
                particle.parameters_vector[1] = tmp
        return particles_vector 

class Test_SwarmsTests(unittest.TestCase):
    

    def test_should_enter_given_coordinates(self):
        # given
        swarm = Swarm(omega = 0.5, intertion = 0.5)
        swarm._lower_constraints = array([0] * 3)
        swarm._upper_constraints = array([1000] * 3)

        initial_parameters = [[100, 200, 300], [50, 100, 150]]
        parameters_after_iteration = [[100, 200, 300], [25, 50, 75]]

        particles = [Particle(initial_parameters[0]), Particle(initial_parameters[1])]
        
        # when

        swarm.optimize(particle_swarm = particles, best = particles[0])

        # then
        self.assertTrue((particles[0].parameters_vector == parameters_after_iteration[0]).all())
        self.assertTrue((particles[1].parameters_vector == parameters_after_iteration[1]).all())        

    def test_should_have_given_speed(self):
        # given
        swarm = Swarm(omega = 0.5, intertion = 0.5)
        swarm._lower_constraints = array([0] * 3)
        swarm._upper_constraints = array([1000] * 3)
        initial_parameters = [[100, 200, 300], [50, 100, 150]]
        speed_after_iteration = [-25, -50, -75]

        particles = [Particle(initial_parameters[0]), Particle(initial_parameters[1])]
        
        # when

        swarm.optimize(particle_swarm = particles, best = particles[0])

        # then
        self.assertEqual(list(particles[1]._speed), speed_after_iteration)    

    def test_should_find_threshold_value(self):
        # given
        img = cv.imread("..\\PSOTests\\TestImages\\threshold_test.jpg", 0)
        lower_threshold = 130
        upper_threhshold = 255
        thresholded = cv.threshold(img, lower_threshold, upper_threhshold, cv.THRESH_BINARY)
        thresholded = thresholded[1] # strange value on index #1
        builder = PSObuilder()

        # when

        builder.segmentation_function = Threshold(img)
        builder.fitness_function = CompareBinaryImages(thresholded)
        builder.minimal_change = 0.0001
        builder.swarm = Classic(0.1, 0.2)

        builder.particles_count = 80

        builder.lower_constraints = [0, 0]
        builder.upper_constraints = [255, 255]

        builder.constraint_callback = proper_thresholds

        pso = builder.build()
        pso.start_optimization()

        # then
        result = pso.get_best_particle().parameters_vector
        result_lower = result[0]
        result_upper = result[1]
         
        # dark image - upper border not important 

        self.assertTrue(result_lower < lower_threshold + 1)
        self.assertTrue(result_lower > lower_threshold - 1)
        # self.assertEqual(result_upper, upper_threshold)


if __name__ == '__main__':
    unittest.main()