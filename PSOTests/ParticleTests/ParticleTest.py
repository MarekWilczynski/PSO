import unittest
from Particles.Particle import Particle
from numpy import array

class Test_Particle(unittest.TestCase):
    def test_should_move_particle(self):
         # given
        initial = array([1, 2.0, 3.0])
        step = array([0.2, 1, 0.4])
        final = array([0] * len(step))

        upper_constraints = array([9, 9, 9])
        lower_constraints = array([1, 1, 1])

        # when
        particle = Particle(initial);
        particle.move(step, lower_constraints, upper_constraints);

        final = initial + step      

        # then
        
        f = final;
        p = particle.parameters_vector
        self.assertEqual(list(f), list(p),"Vector was moved by inpropropriate value")
        

if __name__ == '__main__':
    unittest.main()
