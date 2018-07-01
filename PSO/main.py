from PSO import PSO
from DataInitialization.PSONeighbourhoodBuilder import PSONeighbourhoodBuilder

from FitnessFunctions.BinaryImagesDiceIndex import BinaryImagesDiceIndex
from SegmentationFunctions.LungsSegmentationMatlab import LungsSegmentationMatlab
from Swarms.NeighbourhoodSwarm import NeighbourhoodSwarm
from Utilities.NumericalToObjectConverter import NumericalToObjectConverter

#from cv2 import imread
#from pydicom import dcmread
from time import time


import cv2
import pydicom
from numpy import array


def proper_thresholds(particles_vector):
    for particle in particles_vector:
        ind = 0
        if(particle.parameters_vector[ind] > particle.parameters_vector[ind+1]):
            tmp = particle.parameters_vector[ind]
            particle.parameters_vector[ind] = particle.parameters_vector[ind + 1]
            particle.parameters_vector[ind + 1] = tmp
        
    return particles_vector 


#files_with_extensions = ["105_12_c.mha", "104_12_c.mha","1112_10_c.mha","1259_10_c.mha","1472_11_c.mha","1480_10_c.mha","171_13_c.mha","2088_10_c.mha","2635_10_c.mha","2766_13_c.mha","597_11_c.mha","794_10_c.mha","833_13_c.mha","95_13_c.mha"]
#files = ["171_13_c.mha","2088_10_c.mha","2635_10_c.mha","2766_13_c.mha","597_11_c.mha","794_10_c.mha","833_13_c.mha","95_13_c.mha"]
#files = [file[:-4] for file in files_with_extensions]

ref_img = cv2.imread(".\\Images\\Referential\\Dicoms\\pluca_n1.png",0)
in_img = pydicom.dcmread(".\\Images\\Input\\Dicoms\\pluca_n1.dcm",0)

spacing = in_img.PixelSpacing
in_img = in_img.pixel_array

builder = PSONeighbourhoodBuilder()

builder.segmentation_function = LungsSegmentationMatlab(in_img,spacing)
builder.fitness_function = BinaryImagesDiceIndex(ref_img)
inertia = 0.05
global_speed = 0.35 # speed towards global maximum
neighbourhood_factor = 0.15 # speed towards best particle in neigbourhood
local_factor = 0.15 # speed towards local maximum
builder.swarm = NeighbourhoodSwarm(global_speed, inertia, neighbourhood_factor, local_factor)
builder.minimal_change = 0.0001
builder.neighbourhood_size = 5
builder.no_change_iteration_constraint = 5


#img = builder.segmentation_function.get_result([57.994, 37.279, 14.479, 21.157, 97.576, 598.513])
#cv2.imshow("test",array(img))
#cv2.waitKey()

builder.constraint_callback = proper_thresholds

builder.particles_count = 150

builder.lower_constraints = [-400, 0, 0, 1,0, 1,0, 1,0, 1,0, 1]
builder.upper_constraints = [-100, 60, 1.9999999, 20,1.9999999, 20,1.9999999, 20,1.9999999, 20,1.9999999, 20]


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
       f.write("Upper constraints {}. \n".format(builder.upper_constraints))
       f.write("Lower constraints {}. \n".format(builder.lower_constraints))

       #f.write("\n Parameters constraints \n")
       #f.write("AD_N {} \n".format(AD_N))
       #f.write("AD_kappa {} \n".format(AD_kappa))
       #f.write("AD_lambda {} \n".format(AD_lambda))
       #f.write("GTstd {} \n".format(GTstd))
       #f.write("cAlpha {} \n".format(cAlpha))
       #f.write("cBeta {} \n".format(cBeta))
       #f.write("mu {} \n".format(mu))
       #f.write("G_alpha {} \n".format(G_alpha))
       #f.write("G_type {} \n".format(G_type))
       #f.write("G_kernel_dims {} \n \n".format(G_kernel_dims))



pso.start_optimization()

best_particle = pso.get_best_particle()
vector_string = ', '.join(format(x, "0.3f") for x in best_particle.parameters_vector)
best_fitness = best_particle.fitness

print("Best parameter vector:")
print(vector_string)
print("Best fitness:")
print(best_fitness)

with open("wyniki.txt", "a") as f:
    f.write("Najlepsza segmentacja o wartości przystosowania {} dzieki wektorowi {}. \n".format(best_fitness, vector_string))

img = builder.segmentation_function.get_result(best_particle.parameters_vector)
cv2.imshow("test",array(img))
cv2.waitKey()
