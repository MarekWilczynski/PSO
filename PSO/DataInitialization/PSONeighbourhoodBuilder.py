from DataInitialization.PSObuilder import PSObuilder
from Particles.NeighbourhoodParticle import NeighbourhoodParticle
from Swarms.NeighbourhoodSwarm import NeighbourhoodSwarm
from Swarms.NeighbourhoodSwarm import _update_neighbourhood_data

class PSONeighbourhoodBuilder(PSObuilder):
    """Builder initializing particles with given neighbourhood"""

    neighbourhood_size = 0
    
    def build(self):
        pso = super().build()

        if(not(isinstance(self.swarm, NeighbourhoodSwarm))):
           raise TypeError("Incorrect swarm type!")

        neighbourhood_counter = 0
        new_particle_swarm = []
        old_particle_swarm = pso.particle_swarm
        neighbourhood_size = self.neighbourhood_size

        while(pso.particle_swarm):
            p = NeighbourhoodParticle(old_particle_swarm.pop())
            p.neighbourhood_index = neighbourhood_counter
            new_particle_swarm.append(p)
            if(len(new_particle_swarm) % neighbourhood_size == neighbourhood_size - 1):
                _update_neighbourhood_data(new_particle_swarm, neighbourhood_counter)
                # switch to new neighbourhood
                neighbourhood_counter = neighbourhood_counter + 1

        # updating remaining values, after the end of the loop
        _update_neighbourhood_data(new_particle_swarm, neighbourhood_counter)

        pso.particle_swarm = new_particle_swarm
        return pso

 
