from numpy import array

class Particle:
    """Base class representing a particle moving in multi-dimensional space"""
    parameters_vector = []
    fitness = 0

    _speed = []
        
    def move(self, step_vector, lower_constraints, upper_constraints):
        self._speed = step_vector;
        parameters_vector = self.parameters_vector + step_vector

        # Bringing values out of constraints into constraints
        upper_boundaries_exceeded = (parameters_vector > upper_constraints)
        lower_boundaries_exceeded = (parameters_vector < lower_constraints)

        parameters_vector[upper_boundaries_exceeded] = upper_constraints[upper_boundaries_exceeded]
        parameters_vector[lower_boundaries_exceeded] = lower_constraints[lower_boundaries_exceeded]

        self.parameters_vector = parameters_vector

    def __init__(self, parameters_vector):
        self._speed = array([0] * len(parameters_vector))
        self.parameters_vector = array(parameters_vector)