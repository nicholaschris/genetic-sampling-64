#! usr/bin/python
# ~/Desktop/ga-session-2012-11-12/sample_annual_means.py

#TO DO 
# Fix snapshot of data, why doesn't it get correct values??? FIXED

import os
import sys
import cPickle
import numpy as np
from numpy import ma
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.io.netcdf import netcdf_file

import datetime
### Some stuff to save time and date on plot and filenames
dt = datetime.datetime.now()
date_time_str = dt.ctime()
date_time_short = date_time_str[11:]
print date_time_short

# Set parameters
time_end = 640
lat_end = 64
lon_end = 128

# 50 coords
# coord_dir = "/output/coords/august2013/DecadalMean/50/"
# output_dir = os.getcwd() + '/output/plots/august2013/DecadalMean/50/'
# tex_dir = '/output/tex/august2013/DecadalMean/50/'
# coords = "coords-0.012995371924.pkl"
# coords = "coords-0.00126285342441.pkl"
# coords = "coords-0.00131694489403.pkl"
# coords = "coords-0.00172549930183.pkl"
# coords = "coords-0.00238943479983.pkl"
# coords = "coords-0.00405098538285.pkl"
# coords = "coords-0.00672224136859.pkl"
# coords = "coords-0.00826995459479.pkl"
# coords = "coords-0.00931124296169.pkl"
# coords = "coords-0.00946328708159.pkl"
# 100 coords
# coord_dir = "/output/coords/august2013/DecadalMean/100/"
# output_dir = os.getcwd() + '/output/plots/august2013/DecadalMean/100/'
# tex_dir = '/output/tex/august2013/DecadalMean/100/'
# coords = "coords-0.0019169560861.pkl"
# coords = "coords-0.00101939245887.pkl"
# coords = "coords-0.00187845372939.pkl"
# coords = "coords-0.00214088737286.pkl"
# coords = "coords-0.00214750918045.pkl"
# coords = "coords-0.00354129126376.pkl"
# coords = "coords-0.000388442393228.pkl"
# coords = "coords-0.00415794324852.pkl"
# coords = "coords-0.00508213431867.pkl"
# coords = "coords-0.000633392108423.pkl"
### 500 coords
coord_dir = "/output/coords/august2013/DecadalMean/500/"
output_dir = os.getcwd() + '/output/plots/august2013/DecadalMean/500/'
tex_dir = '/output/tex/august2013/DecadalMean/500/'
coords = "coords-0.00087781774631.pkl"
# coords = "coords-0.00102653934709.pkl"
# coords = "coords-0.00105490806158.pkl"
# coords = "coords-0.000163921915485.pkl"
# coords = "coords-0.000305732109722.pkl"
# coords = "coords-0.000341500488788.pkl"
# coords = "coords-0.000369977350966.pkl"
# coords = "coords-0.000377802861317.pkl"
# coords = "coords-0.000602939168913.pkl"
# coords = "coords-8.82093111154e-06.pkl"
### 1000 coords
# coord_dir = "/output/coords/august2013/DecadalMean/1000/"
# output_dir = os.getcwd() + '/output/plots/august2013/DecadalMean/1000/'
# tex_dir = '/output/tex/august2013/DecadalMean/1000/'
# coords = "coords-0.00083905397649.pkl"
# coords = "coords-0.000129872480308.pkl"
# coords = "coords-0.00156490277202.pkl"
# coords = "coords-0.000301607395787.pkl"
# coords = "coords-0.000444014425856.pkl"
# coords = "coords-0.000478339001043.pkl"
# coords = "coords-0.000599391112794.pkl"
# coords = "coords-0.000730977396797.pkl"
# coords = "coords-0.000972951291725.pkl"
# coords = "coords-4.04438360599e-05.pkl"

coord_filename = os.getcwd() + coord_dir + coords
f = open(coord_filename, 'rb')
coords_and_values = cPickle.load(f)
f.close()

data_cflux_5day_name = "data_cflux_5day" #"data_CFLX_5day_ave"
with open('data/cflx_2000_2009_640x64x128.pkl') as f:
    data = cPickle.load(f)
    f.closed

year_stack = np.split(data, 10)
year_stack = ma.array(year_stack)
print "Year stack has shape: ", np.shape(year_stack)

decadal_mean = ma.mean(data, 0)
dec_mean = ma.mean(decadal_mean)
dec_stdev = ma.std(decadal_mean)
dec_range = np.abs(ma.max(decadal_mean) - ma.min(decadal_mean))
samples = []
for item in coords_and_values:
    samples.append(decadal_mean[ item[1], item[2]])

samples = np.array(samples)
samples_mean = np.mean(samples)
samples_stdev = np.std(samples)
#samples_range = np.abs(ma.max(samples) - ma.min(samples))
original_fitness = np.abs(dec_mean - samples_mean) + np.abs(dec_stdev - samples_stdev) 
# + np.abs(dec_range - samples_range) 

if False:
	raw_input('Press cntrl-c')
	
year_stack_dec = np.mean(year_stack, 1)

#~ x = 0
year_sample_dict_data = {}
year_sample_list_data = {}
for x in np.arange(np.shape(year_stack_dec)[0]):
	#year_value_list = []
	year_values_dict = {}
	#x_nodes = []
	y_nodes = []
	z_nodes = []
	for item in coords_and_values:
		#x_nodes.append(item[0])
		y_nodes.append(item[1])
		z_nodes.append(item[2])
		year_values_dict[item] =  year_stack_dec[x,item[1],item[2]]
		#year_values_dict[item] =  ma.mean(year_stack, axis=1)[x,item[1],item[2]]
		#year_value_list = np.append(year_value_list, year_stack[x,item[0],item[1],item[2]])
	#year_sample_list_data[x] = year_value_list
	year_sample_dict_data[x] = year_values_dict
	print "Creating dictionary"
	#print year_sample_dict_data[x]
	
### We have a values list and coordinates
### If using 5day averages on daily data, the time (x_nodes) is multiplied by 5 #???
if False:
	raw_input('Press cntrl-c')

def test_stats(x):
	coords_vals = year_sample_dict_data[x]
		
	#x_nodes = []	
	y_nodes = []
	z_nodes = []
	values_list = []
	for item in coords_vals:
		values_list.append(coords_vals[item])
	values_list = np.array(values_list)
	#_time_end = 64
	all_data = year_stack_dec[x, :, :]
	#all_data = np.mean(year_stack[x, :_time_end, :lat_end, :lon_end], 1)
	### New and improved and faster!!!
	# but shouldnt it be stdev of annual mean?
	annual_mean = np.mean(all_data)
	sample_mean = np.mean(values_list)
	annual_stdev = np.std(all_data)
	sample_stdev = np.std(values_list)
	fitness = np.abs(annual_mean-sample_mean) + np.abs(annual_stdev - sample_stdev) #+ np.abs(annual_range - sample_range)
	return fitness, annual_mean, sample_mean, annual_stdev, sample_stdev 


list_of_fitness=[]
for x in np.arange(10):
    print x
    list_of_fitness.append(test_stats(x))

fitness = []
mean_data = []
mean_interp_data = []
stdev_data = []
stdev_interp_data = []

for item in list_of_fitness:
	fitness = np.append(fitness, item[0])
	mean_data = np.append(mean_data, item[1])
	mean_interp_data = np.append(mean_interp_data, item[2])
	stdev_data = np.append(stdev_data, item[3])
	stdev_interp_data = np.append(stdev_interp_data, item[4])
	
years = np.arange(10)

#number_of_gens = str(5)
filename = os.getcwd() + tex_dir+'annual_means-'+coords[:-4]+'-' +str(np.round(original_fitness, 2))+ '.tex'
#~ filename = raw_input("Enter filename to write table to: ")
fobj = open(filename, 'w')

data_name = "data_cflux_5day" #data_name #"CFLX5DAY"
prop_or_curr = "Proposed" # Change this depending on which sampling strategy is used...
text_start = " \
\\begin{center} \n \
\\begin{table}[h] \n \
\\centering \n \
\caption{Comparison of the total Simulated Uptake With the Uptake from the \n \
Sampling strategy using " +str(np.size(y_nodes))+ " locations with a \n \
fitness "+str(np.round(original_fitness, 2))+" and the Sampling Error Introduced for " + data_name + ".} \n \
\\begin{tabular}[tbp]{@{}llllll@{}} \n \
\\toprule \n \
\scriptsize{Year} & \
\scriptsize{\specialcell{Model\\Mean\\}} \n \
& \scriptsize{\specialcell{Sample\\Mean}} \n \
& \scriptsize{\specialcell{Model\\Standard\\Deviation}} \n \
& \scriptsize{\specialcell{Sample\\Standard\\Deviation}} \n \
& \scriptsize{Fitness} \\\ \n \
\hline \n \
"

fobj.write(text_start)
'''
for year in range(10):
	fobj.write("\scriptsize{" +str(years[year] +2000)+ "} & \scriptsize{"+str(round(list_of_fitness[year][1], 2))+"} & \scriptsize{"+str(round(list_of_fitness[year][2], 2))+"} & \scriptsize{"+str(round(list_of_fitness[year][3], 2))+"} & \scriptsize{"+str(round(list_of_fitness[year][4], 2))+"} & \scriptsize{"+str(round(list_of_fitness[year][0], 2))+"} \\\\")
	fobj.write("\n")
'''
for year in range(10):
	fobj.write("\scriptsize{" +str(years[year] +2000)+ "} & \scriptsize{"+str(round(mean_data[year], 2))+"} & \scriptsize{"+str(round(stdev_data[year], 2))+"} & \scriptsize{"+str(round(mean_interp_data[year], 2))+"} & \scriptsize{"+str(round(stdev_interp_data[year], 2))+"} & \scriptsize{"+str(round(fitness[year], 2))+"} \\\\")
	fobj.write("\n")

text_end ="\hline \n \
\scriptsize{" +str(years[0] + 2000)+ "-" +str(years[9] + 2000)+ "}    &   \
\scriptsize{"+str(round(np.mean(mean_data), 2))+" $\pm$ "+str(round(np.std(mean_data), 2))+"} &  \
\scriptsize{"+str(round(np.mean(stdev_data), 2))+" $\pm$ "+str(round(np.std(stdev_data), 2))+"} &  \
\scriptsize{"+str(round(np.mean(mean_interp_data), 2))+" $\pm$ "+str(round(np.std(mean_interp_data), 2))+"} &  \
\scriptsize{"+str(round(np.mean(stdev_interp_data), 2))+" $\pm$ "+str(round(np.std(stdev_interp_data), 2))+"} & \
\scriptsize{"+str(round(np.mean(fitness), 2))+" $\pm$ "+str(round(np.std(fitness), 2))+"} \\\ \n \
\\bottomrule \n \
\end{tabular} \n \
\end{table} \n \
\end{center} \n \
"

fobj.write(text_end)
fobj.close()

print "Output written to ", filename

