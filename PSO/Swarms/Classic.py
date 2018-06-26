from numpy import array
from Swarms.Swarm import Swarm

class Classic(Swarm):
    """Classic representation of PSO"""

    _omega = 0
    _inertion = 0
    _local = 0

    def __init__(self, omega, inertion, local):
        self._omega = omega;
        self._inertion = inertion
        self._local = local

    def optimize(self, particle_swarm, best):
        omega = array([self._omega] * len(particle_swarm[0].parameters_vector))
        inertion = array([self._inertion] * len(particle_swarm[0].parameters_vector))
        best_vector = array(best.parameters_vector)
        local_speed_factor = array([self._inertion] * len(particle_swarm[0].parameters_vector))

        print("Best vector: ", best_vector)
        print("Fitness value: ", best.fitness)

        for p in particle_swarm:
            np_param_vector = array(p.parameters_vector)
            goal_vector = np_param_vector - best_vector
            step_vector = goal_vector * omega

            speed_vector = array(p._speed)
            intertion_vector = speed_vector * inertion

            local_vector_distance = np_param_vector - array(p.best_local_params)
            local_speed = local_vector_distance * local_speed_factor

            final_vector = step_vector + intertion_vector + local_speed
            p.move(final_vector, self._lower_constraints, self._upper_constraints)

        return particle_swarm