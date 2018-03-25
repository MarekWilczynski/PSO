from numpy import array
from Swarms.Swarm import Swarm

class Classic(Swarm):
    """Classic representation of PSO"""

    _omega = 0
    _inertion = 0

    def __init__(self, omega, intertion):
        self._omega = omega;
        self._inertion = intertion

    def optimize(self, particle_swarm, best):
        omega = array([self._omega] * len(particle_swarm[0].parameters_vector))
        intertion = array([self._inertion] * len(particle_swarm[0].parameters_vector))
        best_vector = array(best.parameters_vector)

        print("Best vector: ", best_vector)
        print("Fitness value: ", best.fitness)

        for p in particle_swarm:
            np_param_vector = array(p.parameters_vector)
            goal_vector = np_param_vector - best_vector
            step_vector = goal_vector * omega

            speed_vector = array(p._speed)
            intertion_vector = speed_vector * intertion

            final_vector = step_vector + intertion_vector
            p.move(final_vector, self._lower_constraints, self._upper_constraints)

        return particle_swarm