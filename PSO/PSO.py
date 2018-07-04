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

    fitness_record = []

    _minimal_change = 0
    _no_change_iteration_constraint = 0
    _min_iteration_number = 1
    _max_iteration_number = float("inf")

    best_particle = []
    # Ze względu na szas obliczeń ususięto dodatkowe funkcje
    
    def start_optimization(self):
        change = 1
        it = 0
        no_fitness_change_count = 0

        print("Initializing fitness values")
        self.update_fitness_values() 
        self.best_particle = deepcopy(max(self.particle_swarm, key = lambda p:p.fitness,))
        print("Initializing fitness values finished")

        print("Best vector before optimization: ")
        {print("{0:.3f}".format(val), end = ' ', sep = ' ', flush = True) for val in self.best_particle.parameters_vector}
        print("")
        print("Fitness: ", self.best_particle.fitness)
        if(hasattr(self.best_particle, 'neighbourhood_index')):
            print("Neighbourhood: ", self.best_particle.neighbourhood_index)
        
        while(((no_fitness_change_count < self._no_change_iteration_constraint) or (it < self._min_iteration_number)) and (it < self._max_iteration_number)):
            previousBest = self.best_particle.fitness

            self._swarm.optimize(self.particle_swarm, self.best_particle)   
                     
            start = time()  
            self.update_fitness_values() 
            end = time()
            
            print("Segmentation time: {0:.3f}".format(end-start), " seconds")

            new_best_particle = deepcopy(max(self.particle_swarm, key = lambda p:p.fitness,))
            self.best_particle = deepcopy(max([self.best_particle, new_best_particle], key = lambda p:p.fitness,))
            self.fitness_record.append(self.best_particle.fitness)
            
            it = it + 1
            print("Current iteration: " + str(it))
            change = self.best_particle.fitness - previousBest

            if(change < self._minimal_change):
                print("No change detected")
                no_fitness_change_count = no_fitness_change_count + 1
            else:
                print("Change detected")
                no_fitness_change_count = 0


    def get_best_particle(self):
        return self.best_particle

    def update_fitness_values(self):
        el_count = 0
        for p in self.particle_swarm:
            el_count = el_count + 1
            particles_count = len(self.particle_swarm)

            sys.stdout.write("\rParticle {0} of out {1}".format(el_count, particles_count))
            sys.stdout.flush()
            segmented_image = self._segmentation_function.get_result(p.parameters_vector)
            new_fitness = self._fitness_function.get_result(segmented_image)

            if(p.fitness < new_fitness):
                p.best_local_params = p.parameters_vector

            p.fitness = new_fitness
        sys.stdout.write("\n")