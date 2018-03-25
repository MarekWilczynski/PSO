from PSO import PSO
from DataInitialization.PSONeighbourhoodBuilder import PSONeighbourhoodBuilder

from FitnessFunctions.BinaryImagesDiceIndex import BinaryImagesDiceIndex
from SegmentationFunctions.LungsSegmentationMatlab import LungsSegmentationMatlab
from Swarms.NeighbourhoodSwarm import NeighbourhoodSwarm

from cv2 import imread
from pydicom import dcmread
from time import time


import cv2

#def proper_thresholds(particles_vector):
#    for particle in particles_vector:
#        if(particle.parameters_vector[0] > particle.parameters_vector[1]):
#            tmp = particle.parameters_vector[0]
#            particle.parameters_vector[0] = particle.parameters_vector[1]
#            particle.parameters_vector[1] = tmp

#    return particles_vector 

# param 0 oznacza grayscale
#ref_image = imread("..\\PSOTests\\TestImages\\barcodes_ref.png", 0)
#input_image = imread("..\\PSOTests\\TestImages\\barcodes1.jpg", 0)

dcm = dcmread(".\\Images\\Input\\Dicoms\\pluca_n1.dcm")
ref_image = imread(".\\Images\\Referential\\Dicoms\\pluca_n1.png", 0)
input_image = dcm.pixel_array
spacing = dcm.PixelSpacing

# TEST

#param = [ 96.21995294, 206.82290273 ,  9.87580136 , 15.40594355 , 12.52747395, 172.89246698]
#param = [112.34931339, 189.09854254,  16.66923429,   7.29969195,  57.26843701,   1.        ] # pierwszy wynik sasiedztwa
#b = BarcodeSegmentation(input_image)
#t = b.get_result(param)

#cv2.imshow(" PUPUPU", t)
#cv2.waitKey(0)

#

#for i in range(15):

se_types = [cv2.MORPH_RECT, cv2.MORPH_CROSS, cv2.MORPH_ELLIPSE]

builder = PSONeighbourhoodBuilder()

builder.segmentation_function = LungsSegmentationMatlab(input_image, spacing, se_types)
builder.fitness_function = BinaryImagesDiceIndex(ref_image)
interia = 0.3
speed = 0.05
neighbourhood_factor = 0.3
local_factor = 0.25
builder.swarm = NeighbourhoodSwarm(speed, interia, neighbourhood_factor, local_factor)
builder.minimal_change = 0.0001
builder.neighbourhood_size = 5


#builder.constraint_callback = proper_thresholds

builder.particles_count = 25

# threshold, objects to remove size, structural, (element type, structural element width, structural element height) x5

builder.lower_constraints = [-2048, 0, 0, 1, 1,0, 1, 1,0, 1, 1,0, 1, 1,0, 1, 1]
builder.upper_constraints = [2048, 200, 2.9999999, 20, 20,2.9999999, 20, 20,2.9999999, 20, 20,2.9999999, 20, 20,2.9999999, 20, 20]

print("Initialization started")
build_time = time()
pso = builder.build()
print("Initialization Finished. Elapsed time: ", str(time() - build_time ))

pso.start_optimization()

print("Best parameter vector:")
print(', '.join(map(str, pso.get_best_particle().parameters_vector)))
print("Best fitness:")
print(pso.get_best_particle().fitness)