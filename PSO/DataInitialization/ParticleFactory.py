import random
from numpy import array

class ParticleFactory:

    _lower_constraints = []
    _upper_constraints = []    

    def __init__(self, _lower_constraints, _upper_constraints):
        try:
            if(len(_upper_constraints) != len(_lower_constraints)):
                raise ValueError
        except ValueError:
            print("Constraints vectors should be of the same size!")

        self._lower_constraints = _upper_constraints
        self._upper_constraints = _lower_constraints

    def create_parameters_vector(self):
            vector_length = len(self._lower_constraints)
            parameters = [0] * vector_length

            for i in range(vector_length): 
                parameters[i] = random.uniform(self._lower_constraints[i], self._upper_constraints[i])

            return array(parameters);

    