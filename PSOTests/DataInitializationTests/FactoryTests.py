import unittest
import DataInitialization.ParticleFactory as P
import numpy as np

class Test_test1(unittest.TestCase):
    def test_are_vectors_created_within_constraints(self):
        # given
        upper_constraint = [0.3, 15.0, 10.0]
        lower_constraint = [0.0, 2.0, 9.5]

        # when
        particleFactory = P.ParticleFactory(lower_constraint, upper_constraint)
        vector = particleFactory.create_parameters_vector()

        # then


        self.assertTrue(np.array(upper_constraint > vector).all(), "Values were too big!")
        self.assertTrue(np.array(lower_constraint < vector).all(),"Values were too small!")

if __name__ == '__main__':
    unittest.main()
