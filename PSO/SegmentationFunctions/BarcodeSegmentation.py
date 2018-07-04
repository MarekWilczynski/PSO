import SegmentationFunctions.SegmentationFunction as base

import numpy as np
import cv2

from math import floor

class BarcodeSegmentation(base.SegmentationFunction):
    """Class implementing barcode segmentation using python"""
    # https://hackernoon.com/barcode-image-segmentation-a36cdce69f03

    def __init__(self, input_image):
        return super().__init__(input_image)

    def get_result(self, parameters_vector):

        # functions def

        morphologyEx = cv2.morphologyEx

        # params def

        #lower_threshold = 10
        #upper_threshold = 255

        #blackhat_kernel_size = 3
        #morphology_kernel_size = 5

        #objects_to_remove_height = 21
        #objects_to_remove_width = 35

        threshhold = floor(parameters_vector[0])
        output_value = 255

        blackhat_kernel_size = floor(parameters_vector[1])
        morphology_kernel_size = floor(parameters_vector[2])

        objects_to_remove_height = floor(parameters_vector[3])
        objects_to_remove_width = floor(parameters_vector[4])
        
        # image loading
        im = self._input_image

        #blackhat
        kernel = np.ones((1, blackhat_kernel_size), np.uint8)
        im = morphologyEx(im, cv2.MORPH_BLACKHAT, kernel, anchor=(1, 0))

        #sogliatura
        thresh, im = cv2.threshold(im, threshhold, output_value, cv2.THRESH_BINARY)

        #operazioni  morfologiche
        kernel = np.ones((1, morphology_kernel_size), np.uint8)
        im = morphologyEx(im, cv2.MORPH_DILATE, kernel, anchor=(2, 0), iterations=2) #dilatazione
        im = morphologyEx(im, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=2)  #chiusura

        kernel = np.ones((objects_to_remove_height, objects_to_remove_width), np.uint8)
        im = morphologyEx(im, cv2.MORPH_OPEN, kernel, iterations=1)
        
        return im;

    # function definitions


    



