from copy import deepcopy # koniecznie do stworzenia kopii głębokiej

import sys

from cv2 import imshow
from cv2 import waitKey
from time import time
class PSO:
    """Class representing the program"""
    particle_swarm = [] 
    # object providing the algorithm of optimization
    _swarm = []
    # function use to calculate the fitnes
    _fitness_function = []
    # function used to do the segmentation
    _segmentation_function = []

    _minimal_change = 0
    _no_change_iteration_constraint = 0

    # Ze względu na szas obliczeń ususięto dodatkowe funkcje
    
    def start_optimization(self):
        change = 1
        best_particle = deepcopy(max(self.particle_swarm, key = lambda p:p.fitness,))

        segmentation = self._segmentation_function.get_result
        get_fitness = self._fitness_function.get_result        
        it = 0
        no_fitness_change_count = 0
        
        while(no_fitness_change_count < self._no_change_iteration_constraint):
            previousBest = best_particle.fitness

            self._swarm.optimize(self.particle_swarm, best_particle)
            start = time()
            el_count = 0
            particles_count = len(self.particle_swarm)
            for p in self.particle_swarm:
                el_count = el_count + 1
                sys.stdout.write("\rParticle {0} of out {1}".format(el_count, particles_count))
                sys.stdout.flush()
                segmented_image = segmentation(p.parameters_vector)
                p.fitness = get_fitness(segmented_image)
               
                
            end = time()
            sys.stdout.write("\n")
            print("Segmentation time: {0:.3f}".format(end-start), " seconds")

            new_best_particle = deepcopy(max(self.particle_swarm, key = lambda p:p.fitness,))
            best_particle = deepcopy(max([best_particle, new_best_particle], key = lambda p:p.fitness,))
            
            it = it + 1
            print("Current iteration: " + str(it))
            change = best_particle.fitness - previousBest

            if(change < self._minimal_change):
                print("No change detected")
                no_fitness_change_count = no_fitness_change_count + 1
            else:
                print("Change detected")
                no_fitness_change_count = 0

    def iterate(self):
        self._swarm.optimize(self.particle_swarm, get_best_particle())

    def get_best_particle(self):
        best_particle = max(self.particle_swarm, key = lambda p:p.fitness,)
        return best_particle

    def update_fitness_values(self):
        for p in self.particle_swarm:
            segmented_image = self._segmentation_function.get_result(p.parameters_vector)
            p.fitness = self._fitness_function.get_result(self._reference_image, segmented_image)