from PSO import PSO
from DataInitialization.ParticleFactory import ParticleFactory
from Particles.Particle import Particle
from numpy import array

import sys

class PSObuilder:
    """Class required to initialize an instance of PSO algorithm. Each property is required to be set."""
    
    # swarm properties
    minimal_change = 0
    no_change_iteration_constraint = 1
    swarm = []
    segmentation_function = []
    fitness_function = []   

    # particles properties
    particles_count = 0
    upper_constraints = []
    lower_constraints = []
    # callback
    constraint_callback = []
    
    def build(self):
        pso = PSO()

        self.swarm._lower_constraints = array(self.lower_constraints)
        self.swarm._upper_constraints = array(self.upper_constraints)

        pso._swarm = self.swarm
        pso._minimal_change = self.minimal_change
        pso._segmentation_function = self.segmentation_function
        pso._fitness_function = self.fitness_function
        pso._no_change_iteration_constraint = self.no_change_iteration_constraint

        factory = ParticleFactory(self.lower_constraints, self.upper_constraints)

        #for _ in range(particles_count):
        #    random_vector_within_constraints = factory.create_parameters_vector()
        #    random_particle = Particle(random_vector_within_constraints)
            
        #    pso.particle_swarm.append(random_particle)
        
        particle_swarm = [Particle(factory.create_parameters_vector()) for x in range(self.particles_count)]          
        el_count = 0
        particles_count = len(particle_swarm)
        for p in particle_swarm:
            el_count = el_count + 1
            sys.stdout.write("\rParticle {0} of out {1}".format(el_count, particles_count))
            sys.stdout.flush()
            p.fitness = self.fitness_function.get_result( self.segmentation_function.get_result( p.parameters_vector ) )
            
            

        if(self.constraint_callback != []):
            new_particle_swarm = self.constraint_callback(particle_swarm)
        else:
            new_particle_swarm = particle_swarm

        pso.particle_swarm = new_particle_swarm
        sys.stdout.write("\n")
        return pso

        
    #def build(self):
    #    try:
    #        if(type(self.particles_count) != 'int' and self.particles_count != 0):
    #            raise TypeError("Particles count must be an int!")

    #        if(type(self.minimal_change) == 'float' and self.minimal_change != 0):
    #            raise TypeError("Minimal change must be a float!")

    #        if(type(self.pso_algorithm) != 'method' and self.pso_algorithm != []):
    #            raise TypeError("PSO algorithm must be a method!")

    #        if(type(self.segmantation_function) != 'method' and self.segmantation_function != []):
    #            raise TypeError("Segmantation method must be a method!")

    #        if(type(self.fitness_function) != 'method' and self.fitness_function != []):
    #            raise TypeError("Fitness function must be a method!")


    #    except TypeError as e:
    #        print(e)
    #    return 

