from DataInitialization.PSObuilder import PSO
from DataInitialization.PSObuilder import PSObuilder

from FitnessFunctions.CompareBinaryImages import CompareBinaryImages
from SegmentationFunctions.BarcodeSegmentation import BarcodeSegmentation
from Swarms.Classic import Classic

from cv2 import imread


import cv2

def proper_thresholds(particles_vector):
    for particle in particles_vector:
        if(particle.parameters_vector[0] > particle.parameters_vector[1]):
            tmp = particle.parameters_vector[0]
            particle.parameters_vector[0] = particle.parameters_vector[1]
            particle.parameters_vector[1] = tmp

        if(particle.parameters_vector[2] > particle.parameters_vector[3]):
            tmp = particle.parameters_vector[2]
            particle.parameters_vector[2] = particle.parameters_vector[3]
            particle.parameters_vector[3] = tmp
            
        if(particle.parameters_vector[4] > particle.parameters_vector[5]):
            tmp = particle.parameters_vector[4]
            particle.parameters_vector[4] = particle.parameters_vector[5]
            particle.parameters_vector[5] = tmp

    return particles_vector 

# param 0 oznacza grayscale
ref_image = imread("..\\PSOTests\\TestImages\\barcodes_ref.png", 0)
input_image = imread("..\\PSOTests\\TestImages\\barcodes1.jpg", 0)

# TEST

#param = [ 96.21995294, 206.82290273 ,  9.87580136 , 15.40594355 , 12.52747395, 172.89246698]
#b = BarcodeSegmentation(input_image)
#t = b.get_result(param)

#cv2.imshow(" PUPUPU", t)
#cv2.waitKey(0)

#

#for i in range(15):
builder = PSObuilder()

builder.segmantation_function = BarcodeSegmentation(input_image)
builder.fitness_function = CompareBinaryImages(ref_image)
builder.minimal_change = 0.0001
builder.swarm = Classic(0.1, 0.2)

builder.constraint_callback = proper_thresholds

builder.particles_count = 1000

# lower_threshold, upper threshold, mask size, mask size, object heigth, object width

builder.lower_constraints = [0, 0, 3, 3, 1, 1]
builder.upper_constraints = [255, 255, 25, 25, 800, 800]

pso = builder.build()

pso.start_optimization()

print("Best parameter vector:")
print(', '.join(map(str, pso.get_best_particle().parameters_vector)))
print("Best fitness:")
print(pso.get_best_particle().fitness)