from Particles.Particle import Particle
class NeighbourhoodParticle(Particle):
    """Class implementing particle with neighbood and local fitness max"""
        
    best_local_params = []
    best_neighbourhood_params = []
    neighbourhood_index = []

    def move(self, step_vector, lower_constraints, upper_constraints):    
        super().move(step_vector, lower_constraints, upper_constraints)

    def __init__(self, particle):
        self.best_local_params = particle.parameters_vector
        self.fitness = particle.fitness

        self._speed = particle._speed
        self.parameters_vector = particle.parameters_vector
        




