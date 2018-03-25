from copy import deepcopy # koniecznie do stworzenia kopii głębokiej

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

    # Ze względu na szas obliczeń ususięto dodatkowe funkcje
    
    def start_optimization(self):
        change = 1
        best_particle = deepcopy(max(self.particle_swarm, key = lambda p:p.fitness,))

        segmentation = self._segmentation_function.get_result
        get_fitness = self._fitness_function.get_result        
        it = 0

        #while(change > self._minimal_change):
        while(it < 120):
            previousBest = best_particle.fitness

            self._swarm.optimize(self.particle_swarm, best_particle)
            start = time()
            for p in self.particle_swarm:
                segmented_image = segmentation(p.parameters_vector)
                p.fitness = get_fitness(segmented_image)
            end = time()
            print("Segmentation time: ", end-start, " sekund")

            new_best_particle = deepcopy(max(self.particle_swarm, key = lambda p:p.fitness,))
            best_particle = deepcopy(max([best_particle, new_best_particle], key = lambda p:p.fitness,))
            change = best_particle.fitness - previousBest
            it = it + 1

    def iterate(self):
        self._swarm.optimize(self.particle_swarm, get_best_particle())

    def get_best_particle(self):
        best_particle = max(self.particle_swarm, key = lambda p:p.fitness,)
        return best_particle

    def update_fitness_values(self):
        for p in self.particle_swarm:
            segmented_image = self._segmentation_function.get_result(p.parameters_vector)
            p.fitness = self._fitness_function.get_result(self._reference_image, segmented_image)