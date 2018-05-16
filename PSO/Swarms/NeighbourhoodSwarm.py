from Swarms.Swarm import Swarm
from numpy import array

class NeighbourhoodSwarm(Swarm):
    """Swarm optimazing particles including their neighbourhood"""
    
    _omega = 0
    _inertion = 0
    _neighbourhood_factor = 0
    _local_factor = 0

    def __init__(self, omega, intertion, neighbourhood_factor, local_factor):
        self._omega = omega;
        self._inertion = intertion
        self._neighbourhood_factor = neighbourhood_factor
        self._local_factor = local_factor


    def optimize(self, particle_swarm, best):
        omega = array([self._omega] * len(particle_swarm[0].parameters_vector))
        inertion = array([self._inertion] * len(particle_swarm[0].parameters_vector))
        best_vector = array(best.parameters_vector)
        print("Best vector before optimization: ")
        {print("{0:.3f}".format(val), end = ' ', sep = ' ', flush = True) for val in best_vector}
        print("")
        print("Fitness: ", best.fitness)
        print("Neighbourhood: ", best.neighbourhood_index)

        for p in particle_swarm:
            np_param_vector = array(p.parameters_vector)
            goal_vector = np_param_vector - best_vector
            step_vector = goal_vector * omega

            speed_vector = array(p._speed)
            intertion_vector = speed_vector * inertion

            # computing local and neighbour hood speed
            neighbourhood_speed = (np_param_vector - p.best_neighbourhood_params) * self._neighbourhood_factor
            local_speed = (np_param_vector - p.best_local_params) * self._local_factor
            
            # computing resulting speed
            final_vector = step_vector + intertion_vector + neighbourhood_speed + local_speed
            p.move(final_vector, self._lower_constraints, self._upper_constraints)

           
        neighbourhood_indexes = range(max(particle_swarm, key = lambda p: p.neighbourhood_index).neighbourhood_index)
        for neighbourhood in neighbourhood_indexes:
            _update_neighbourhood_data(particle_swarm, neighbourhood)

        return particle_swarm

def _update_neighbourhood_data(particle_swarm, neighbourhood):
    # finding neighbouring particles, and searching for best value
    particles = filter(lambda p: p.neighbourhood_index == neighbourhood, particle_swarm)
    particles = list(particles)
    best_vector = max(particles, key = lambda p: p.fitness).parameters_vector
                
    for np in particles:
        # updating neighbourhood data
        np.best_neighbourhood_params = best_vector  