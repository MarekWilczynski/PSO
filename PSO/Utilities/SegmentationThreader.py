import threading
import queue
import time

queue_lock = threading.Lock()

class SegmentationThreader(threading.Thread):
    """Class allowing asynchronous segmentation, increasing speed of computation"""
        
    _segmentation_fun = []
    _fitness_fun = []
    _particle = []
    segmentation_result = []

    def __init__(self, segmentation_fun, particle):
        self._segmentation_fun = segmentation_fun
        self._particle = particle
        threading.Thread.__init__(self)

    def run(self):
        queue_lock.acquire()
        self.segmentation_result = self._segmentation_fun.get_result(self._particle.parameters_vector)       
        queue_lock.release()


# WITH MULTIPROCESSING

#import multiprocessing as mp
#lock = mp.Lock()

#class SegmentationThreader():
#    """Class allowing asynchronous segmentation, increasing speed of computation"""
        
#    _segmentation_fun = []
#    _fitness_fun = []
#    _particle = []

#    def __init__(self, segmentation_fun, fitness_fun, particle):
#        self._segmentation_fun = segmentation_fun
#        self._particle = particle
#        self._fitness_fun = fitness_fun

#    def run(self):
#        lock.acquire()
#        segmentation_result = self._segmentation_fun.get_result(self._particle.parameters_vector)
#        fitness = self._fitness_fun.get_result(segmentation_result)
#        self._particle.fitness = fitness
#        lock.release()

#    def start(self):
#        proc = mp.Process(target = self.run)
#        proc.start()
#        r