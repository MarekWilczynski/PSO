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


    def test_should_move_particle_to_upper_boudaries(self):
        # given
        initial = array([1, 2.0, 3.0])
        step = array([11.2, 13, 7])
        final = array([0] * len(step))

        upper_constraints = array([9, 9, 9])
        lower_constraints = array([1, 1, 1])

        # when
        particle = Particle(initial);
        particle.move(step, lower_constraints, upper_constraints);
                   
        # then        
        
        self.assertEqual(list(particle.parameters_vector), [9, 9, 9],"Vector was moved by inpropropriate value")

    def test_should_move_particle_to_lower_boudaries(self):
        # given
        initial = array([1, 2.0, 3.0])
        step = array([-2.3, -5.5, -4.5])
        final = array([0] * len(step))

        upper_constraints = array([9, 9, 9])
        lower_constraints = array([-1, 0, 1])

        # when
        particle = Particle(initial);
        particle.move(step, lower_constraints, upper_constraints);

        # then
        
        f = final;
        p = particle.parameters_vector
        self.assertEqual(list(particle.parameters_vector), [-1, 0, 1],"Vector was moved by inpropropriate value")

    def test_should_move_particle_to_upper_from_lower(self):
        # given
        initial = array([1, 2.0, 3.0])
        step1 = array([-2.3, -5.5, -4.5])
        step2 = array([15, 11.2, 9])
        final = array([0] * len(step1))

        upper_constraints = array([9, 9, 9])
        lower_constraints = array([-1, 0, 1])

        # when
        particle = Particle(initial);
        particle.move(step1, lower_constraints, upper_constraints);
        particle.move(step2, lower_constraints, upper_constraints);
        # then

        self.assertEqual(list(particle.parameters_vector), [9, 9, 9],"Vector was moved by inpropropriate value")
        

if __name__ == '__main__':
    unittest.main()
