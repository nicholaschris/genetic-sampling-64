#!usr/bin/python
# refactor genetic-sampling
# created 20130816

import datetime
import numpy as np
import make_population
import make_gene_map
import matplotlib
import ga_class
import matplotlib.pyplot as plt
from numpy import ma
from scipy.interpolate import Rbf
from matplotlib import cm
import cPickle
import os
from scipy.io.netcdf import netcdf_file

output_dir = os.getcwd() + '/output/plots/august2013/'

### Some stuff to save time and date on plot and filenames
dt = str(datetime.datetime.now())
date = dt[:10]
time = dt[11:16]
print time

genetic = ga_class.GeneticAlgorithm() 		
genetic.get_array_attributes()
genetic.make_gene_map_3()
genetic.get_gene_size(genetic.string_length)
genetic.set_up_new_pop()
print "The time axis has length: ",genetic.time_len
print "The chromosome size is: ", genetic.chromosome_size
genetic.get_mask()

fittest_list = []		# Use the fittest list to plot evolution of algorithm DOES IT WORK?
least_fit_list = []	    # likewise for least fit list

print datetime.datetime.now()
'''
user_input = raw_input("The GA is set up, press y to continue.")
if user_input == 'y':
	print "Continuing"
'''
	
# Set number of generations here:
NUM_GEN = 100
print "Running Genetic Algorithm for %d generations." % NUM_GEN
gen_count = 0
while gen_count < NUM_GEN:
    #genetic.add_fitness_key()
    genetic.add_fitness_fast()
    #~ genetic.add_fitness_rmse_stdev()
    fittest_list = np.append(fittest_list, genetic.fittest_fitness)
    least_fit_list = np.append(least_fit_list, genetic.least_fitness)
    genetic.sort_pop()
    genetic.make_new_pop()
    genetic.elitism()
    #~ print genetic.population[0]['fitness']
    #~ print genetic.new_pop[0]['fitness']
    genetic.population = genetic.new_pop
    print "There are %g generations left" %(NUM_GEN-gen_count) 
    gen_count+=1

print datetime.datetime.now()
plt.close('all')

### A plot to visualise how the GA evolved ###
# ymax depends on fitness function and no of locations
plt.ylim(ymin=0, ymax = 0.1)
plt.plot(fittest_list, label='Fittest Individuals')
plt.plot(least_fit_list, label='Least Fit Individuals')
plt.title('Genetic Algorithm - ' + date + time)
plt.xlabel('Generation')
plt.ylabel('fitness')
plt.legend(loc=7)
plt.savefig(output_dir + 'GA' + date + '_' + time + '-'+str(NUM_GEN)+'.png')
### End plotting ###
 
genetic.add_fitness_fast()
genetic.sort_pop() 
solution = genetic.population[0]['chrom_list']

the_fittest_fitness = genetic.population[0]['fitness']

### This saves the coordinate tuples in a list ###
def calc_chrom(chromosome, dictionary):
    '''
    This saves the coordinate tuples in a list.
    '''
    gene_stepper = 0
    values_list = []
    coord_list = [(0, 0, 1)]
    gene_length = genetic.string_length
    while gene_stepper < len(chromosome) - gene_length:
        gene_list = chromosome[gene_stepper:gene_stepper+genetic.string_length]
        current_gene = ''
        bit_stepper = 0
        while bit_stepper < gene_length:
            current_gene = current_gene + gene_list[bit_stepper]
            bit_stepper += 1
        values_list = np.append(values_list, dictionary[current_gene]['value'])
        coord_tuple = dictionary[current_gene]['coordinate']
	coord_list.append(coord_tuple)
	gene_stepper += gene_length
    coord_list.pop(0)
    print "Size of Coord_list: ", np.size(coord_list) # DEBUG
    return coord_list, values_list



coord_list, values_list = calc_chrom(solution, genetic.gene_map)
coords_vals = dict(zip(coord_list, values_list))
no_of_locations = np.size(coords_vals.keys())
print "Coords_vals.keys() has length: ", no_of_locations
if coords_vals.has_key((999, 999, 999)):
    print "Popping invalid location!"	
    coords_vals.pop((999,999,999))
    


# Print the list of coordinates to a file!
pop_size = str(np.size(values_list))
data_used = genetic.what_data
fitness_function_used = 'stats' # 'rbf' or 'stats'
filename = os.getcwd() +'/output/coords/august2013/'+data_used+'/'+str(genetic.chromosome_size)+'/coords-'+str(the_fittest_fitness)+'.pkl'
f= open(filename, 'wb')
cPickle.dump(coords_vals, f)
f.close()

print 'Coordinates saved to ' + filename
print genetic.array_shape
