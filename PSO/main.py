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


files_with_extensions = ["105_12_c.mha", "104_12_c.mha","1112_10_c.mha","1259_10_c.mha","1472_11_c.mha","1480_10_c.mha","171_13_c.mha","2088_10_c.mha","2635_10_c.mha","2766_13_c.mha","597_11_c.mha","794_10_c.mha","833_13_c.mha","95_13_c.mha"]
#files = ["171_13_c.mha","2088_10_c.mha","2635_10_c.mha","2766_13_c.mha","597_11_c.mha","794_10_c.mha","833_13_c.mha","95_13_c.mha"]
files = [file[:-4] for file in files_with_extensions]

builder = PSONeighbourhoodBuilder()

builder.segmentation_function = KidneyCystSegmentation(files)
builder.fitness_function = MockDoingNothing([])
inertia = 0.05
global_speed = 0.2 # speed towards global maximum
neighbourhood_factor = 0.1 # speed towards best particle in neigbourhood
local_factor = 0.1 # speed towards local maximum
builder.swarm = NeighbourhoodSwarm(global_speed, inertia, neighbourhood_factor, local_factor)
builder.minimal_change = 0.0001
builder.neighbourhood_size = 5
builder.no_change_iteration_constraint = 3


    #builder.constraint_callback = proper_thresholds

builder.particles_count = 45


AD_N = [1, 200]
AD_kappa = [1, 20]
AD_lambda = [0, 0.05]
GTstd = [0.25, 5]
cAlpha = [0, 1]                                                  
cBeta = [0, 1]
dt = [0, 3]
mu = [0, 0.5]
G_alpha = [0.1, 3]   
G_type = [0, 7]
G_kernel_dims = [1, 80]     

builder.lower_constraints = [AD_N[0], AD_kappa[0], AD_lambda[0], GTstd[0], cAlpha[0], cBeta[0], dt[0], mu[0], G_alpha[0], G_type[0], G_kernel_dims[0]]
builder.upper_constraints = [AD_N[1], AD_kappa[1], AD_lambda[1], GTstd[1], cAlpha[1], cBeta[1], dt[1], mu[1], G_alpha[1], G_type[1], G_kernel_dims[1]]


print("Initialization started")
build_time = time()
pso = builder.build()
print("Initialization Finished. Elapsed time: ", str(time() - build_time ))

with open("wyniki.txt", "a") as f:
       f.write("Swarm parameters \n")
       f.write("Inetria {} \n".format(inertia))
       f.write("global_speed {} \n".format(global_speed))
       f.write("neighbourhood_factor {} \n".format(neighbourhood_factor))
       f.write("neighbourhood_size {} \n".format(builder.neighbourhood_size))
       f.write("no_change_iteration_constraint {} \n".format(builder.no_change_iteration_constraint))
       f.write("particles_count {} \n".format(builder.particles_count))
       f.write("Fitness Function {} \n".format(builder.fitness_function.__class__.__name__))
       f.write("Segmentation function {}. \n".format(builder.segmentation_function.__class__.__name__))

       f.write("\n Parameters constraints \n")
       f.write("AD_N {} \n".format(AD_N))
       f.write("AD_kappa {} \n".format(AD_kappa))
       f.write("AD_lambda {} \n".format(AD_lambda))
       f.write("GTstd {} \n".format(GTstd))
       f.write("cAlpha {} \n".format(cAlpha))
       f.write("cBeta {} \n".format(cBeta))
       f.write("mu {} \n".format(mu))
       f.write("G_alpha {} \n".format(G_alpha))
       f.write("G_type {} \n".format(G_type))
       f.write("G_kernel_dims {} \n \n".format(G_kernel_dims))



pso.start_optimization()

best_particle = pso.get_best_particle()
vector_string = ', '.join(format(x, "0.3f") for x in best_particle.parameters_vector)
best_fitness = best_particle.fitness

print("Best parameter vector:")
print(vector_string)
print("Best fitness:")
print(best_fitness)

with open("wyniki.txt", "a") as f:
    f.write("Najlepsza segmentacja dzieki wektorowi {}. \n".format(vector_string, best_fitness/len(files)))