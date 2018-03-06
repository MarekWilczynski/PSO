from abc import ABCMeta as abstract, abstractmethod

class Swarm(metaclass = abstract):
    """Abstract class representing algorithm of optimization"""
    
    _upper_constraints = []
    _lower_constraints = []
         
    @abstractmethod
    def optimize(self, particle_swarm, best):
       
        return particle_swarm


