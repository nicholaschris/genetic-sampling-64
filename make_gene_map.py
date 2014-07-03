# ~/Desktop/ga-session-2012-11-12/make_gene_map.py

'''Make a gene map that maps a binary string
to a coordinate of an array as well as a value 
for that coordinate.'''

import numpy as np
import itertools
import thepowerof2
from numpy import ma

class GeneMap(object):

    def __init__(self):
        self.gene_map = {}
        self.location_dict = {}
        self.actual_data_dict = {}
        self.location_dict_stdevs = {}
        self.array = []
        self.time_len = 0
        self.lat_len = 0
        self.lon_len = 0
        self.last_valid_binary_string = ''
        self.string_length = 0
        self.count = 0
        self.what_data = ''

    def get_array_attributes(self):
        lat_end = 64
        lon_end = 128
        ### Choose array (decadel mean, annual mean or all data)
        ### All Data
        # self.what_data = 'AllData'
        #self.array = load_cflux_masked.load_file(time_end = time_end, lat_end=lat_end, lon_end=lon_end)
        self.array = thepowerof2.load_file_64()
        # self.array = self.array[:512, :, :]
        ### decadel mean
        # self.what_data = 'DecadalMean'
        # self.array = ma.mean(self.array, axis=0)
        # print self.array.shape
        # self.array = np.reshape(self.array, (1, lat_end, lon_end))
        ### annual mean
        self.what_data = 'AnnualCycle'
        self.array =  ma.mean(np.split(self.array, 10, axis=0), axis=0)
        ###
        self.array_shape = np.shape(self.array)
        self.count = np.size(self.array) - 1
        self.time_len = self.array_shape[0] # need to set interpolated and masked array time_end to be equal NB!!!
        self.lat_len = self.array_shape[1]
        self.lon_len = self.array_shape[2]
        self.string_length = len(bin(self.count)[2:])
        for item in itertools.product(range(self.lat_len), range(self.lon_len)):
            self.actual_data_dict[item] = np.std(self.array[: , item[0], item[1]])
    
    def make_gene_map_3(self):
        counter=0
        self.iterator_three = itertools.product(range(self.time_len), range(64), range(128))
        for item in self.iterator_three:
            binary_string = bin(counter)[2:]
            while len(binary_string) < self.string_length: # hardcoded NB
                binary_string = '0' + binary_string
            self.gene_map[binary_string] = {}    
            self.gene_map[binary_string]['coordinate'] = item
            self.gene_map[binary_string]['value'] = self.array[item]
            counter+=1
        self.last_valid_binary_string = binary_string
        self.counter = counter
        print self.counter, self.last_valid_binary_string



			
