from PSO import PSO
from DataInitialization.PSONeighbourhoodBuilder import PSONeighbourhoodBuilder

from FitnessFunctions.MockDoingNothing import MockDoingNothing
from SegmentationFunctions.KidneyCystSegmentation import KidneyCystSegmentation
from Swarms.NeighbourhoodSwarm import NeighbourhoodSwarm

#from cv2 import imread
#from pydicom import dcmread
from time import time


import cv2

#def proper_thresholds(particles_vector):
#    for particle in particles_vector:
#        if(particle.parameters_vector[0] > particle.parameters_vector[1]):
#            tmp = particle.parameters_vector[0]
#            particle.parameters_vector[0] = particle.parameters_vector[1]
#            particle.parameters_vector[1] = tmp

#    return particles_vector 


files = ["104_12_c.mha","105_12_c.mha","1112_10_c.mha","1259_10_c.mha","1472_11_c.mha","1480_10_c.mha","171_13_c.mha","2088_10_c.mha","2635_10_c.mha","2766_13_c.mha","597_11_c.mha","794_10_c.mha","833_13_c.mha","95_13_c.mha"]
#files = ["171_13_c.mha","2088_10_c.mha","2635_10_c.mha","2766_13_c.mha","597_11_c.mha","794_10_c.mha","833_13_c.mha","95_13_c.mha"]


builder = PSONeighbourhoodBuilder()

builder.segmentation_function = KidneyCystSegmentation(files[0][:-4])
builder.fitness_function = MockDoingNothing([])
inertia = 0.1
global_speed = 0.2 # speed towards global maximum
neighbourhood_factor = 0.3 # speed towards best particle in neigbourhood
local_factor = 0.25 # speed towards local maximum
builder.swarm = NeighbourhoodSwarm(global_speed, inertia, neighbourhood_factor, local_factor)
builder.minimal_change = 0.0001
builder.neighbourhood_size = 5
builder.no_change_iteration_constraint = 5


    #builder.constraint_callback = proper_thresholds

builder.particles_count = 45


AD_N = [10, 80]
AD_kappa = [1, 8]
AD_lambda = [0, 0.05]
GTstd = [0.5, 1.5]
cAlpha = [0.005, 0.05]                                                  
cBeta = [0.25, 0.75]
dt = [0.5, 1.5]
mu = [0.025, 0.15]
G_alpha = [0.25, 1.5]   
G_type = [0, 7]
G_kernel_dims = [1, 20]


builder.lower_constraints = [AD_N[0], AD_kappa[0], AD_lambda[0], GTstd[0], cAlpha[0], cBeta[0], dt[0], mu[0], G_alpha[0], G_type[0], G_kernel_dims[0]]
builder.upper_constraints = [AD_N[1], AD_kappa[1], AD_lambda[1], GTstd[1], cAlpha[1], cBeta[1], dt[1], mu[1], G_alpha[1], G_type[1], G_kernel_dims[1]]


print("Initialization started")
build_time = time()
pso = builder.build()
print("Initialization Finished. Elapsed time: ", str(time() - build_time ))

for file in files:

    file_name = file[:-4]
    img_name = file_name

    pso._segmentation_function._input_image = img_name

    pso.start_optimization()


    vector_string = ', '.join(map(str, pso.get_best_particle().parameters_vector))
    best_fitness = pso.get_best_particle().fitness

    print("Best parameter vector:")
    print(vector_string)
    print("Best fitness:")
    print(best_fitness)

    with open("wyniki.txt", "a") as f:
        f.write("Obraz {} uzyskal wartosc przystosowania {} dzieki wektorowi {}. \n".format(file_name, best_fitness, vector_string))