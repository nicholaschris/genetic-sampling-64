#! usr/bin/python
# ~/Desktop/ga-session-2012-11-12/sample_seasonal_cycle.py

'''
This script takes the solution from from the genetic
algorithm that samples the seasonal cycle and tests
it on the data for each year.

It returns a fitness values for each year, as well as 
the mean value  and the standard
deviation from the sample as well as the model data.

Values get put into a csv or a tex table?

'''

#! usr/bin/python
#  sample_annual_means.py

#TO DO 
# Fix snapshot of data, why doesn't it get correct values??? FIXED

import cPickle
import numpy as np
from numpy import ma
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt
from matplotlib import cm
import sys
import os
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

# unit_changer = 60*60*24 * 1000 # micromol carbon per m per day (86400000)
#output_dir = os.getcwd() + '/output/plots/sample_seasonal_cycle/'
#coord_dir = "/output/coords/august2013/"
### 1000 coords
coord_dir = "/output/coords/august2013/AnnualCycle/1000/"
output_dir = os.getcwd() + '/output/plots/august2013/AnnualCycle/1000/'
tex_dir = '/output/tex/august2013/AnnualCycle/1000/'
# coords = "coords-0.00041323581551.pkl"
# coords = "coords-0.00067869024584.pkl"
# coords = "coords-0.00073813734676.pkl"
# coords = "coords-0.000200143673713.pkl"
# coords = "coords-0.000250325951072.pkl"
# coords = "coords-0.000397808751317.pkl"
# coords = "coords-0.000493543285265.pkl"
# coords = "coords-0.000508593872276.pkl"
# coords = "coords-0.000717352701317.pkl"
# coords = "coords-0.000867832208514.pkl"
# coords = "coords-0.00035014553492.pkl"
# coords = "coords-0.000437359810449.pkl"
# coords = "coords-0.00109731142971.pkl"
# coords = "coords-0.00115357517737.pkl"
# coords = "coords-0.000172093078951.pkl"
# coords = "coords-8.37944983929e-05.pkl"
# coords = "coords-0.000532355855383.pkl"
# coords = "coords-0.000356008490624.pkl"
# coords = "coords-0.000994677815819.pkl"
coords = "coords-0.000282933848919.pkl"
### 2000 coords
# coord_dir = "/output/coords/august2013/AnnualCycle/2000/"
# output_dir = os.getcwd() + '/output/plots/august2013/AnnualCycle/2000/'
# tex_dir = '/output/tex/august2013/AnnualCycle/2000/'
# coords = "coords-0.00047021950887.pkl"
# coords = "coords-0.000201010620604.pkl"
# coords = "coords-0.000251408535903.pkl"
# coords = "coords-0.000252357511537.pkl"
# coords = "coords-0.000254837508471.pkl"
# coords = "coords-0.000298549841805.pkl"
# coords = "coords-0.000842880167576.pkl"
# coords = "coords-5.06119547501e-05.pkl"
# coords = "coords-5.90189888672e-05.pkl"
# coords = "coords-9.63788802397e-05.pkl"
### 5000 coords
# coord_dir = "/output/coords/august2013/AnnualCycle/5000/"
# output_dir = os.getcwd() + '/output/plots/august2013/AnnualCycle/5000/'
# tex_dir = '/output/tex/august2013/AnnualCycle/5000/'
# coords = "coords-0.0004296199495.pkl"
# coords = "coords-0.000172566719318.pkl"
# coords = "coords-0.000228892069235.pkl"
# coords = "coords-0.000232211129108.pkl"
# coords = "coords-0.000428989577183.pkl"
# coords = "coords-0.000459187351613.pkl"
# coords = "coords-0.000514928822419.pkl"
# coords = "coords-0.000889473509061.pkl"
# coords = "coords-0.000902764260347.pkl"
# coords = "coords-8.49116406305e-05.pkl"
### 7000 coords
# coord_dir = "/output/coords/august2013/AnnualCycle/7000/"
# output_dir = os.getcwd() + '/output/plots/august2013/AnnualCycle/7000/'
# tex_dir = '/output/tex/august2013/AnnualCycle/7000/'
# coords = "coords-0.000137256314897.pkl"
# coords = "coords-0.000326907600134.pkl"
# coords = "coords-0.000403223308655.pkl"
# coords = "coords-0.000498314893726.pkl"
# coords = "coords-0.000538436147445.pkl"
# coords = "coords-0.000695093274947.pkl"
# coords = "coords-0.000779404202488.pkl"
# coords = "coords-0.000807563968982.pkl"
# coords = "coords-3.16753566074e-05.pkl"
#coords = "coords-9.84105232018e-05.pkl"
### Old coords
#coords = "coords-3.23861388782e-05AnnualCycle-2013-08-18_0021-6999-100-stats.pkl"
#coords = "coords-0.00142120207842AnnualCycle-2013-08-18_0010-4999-100-stats.pkl"
#coords = "coords-0.000376213650608AnnualCycle-2013-08-17_2334-1999-100-stats.pkl"
#coords = "coords-0.000243618610967AnnualCycle-2013-08-17_2031-999-100-stats.pkl"
coord_filename = os.getcwd() + coord_dir + coords
#coord_filename = os.getcwd() + "/output/coords/Coordinates_Values_2012-12-17-8h56.pkl"
#coord_filename = sys.argv[1]
#~ coord_filename = raw_input("Which cPickle file do you want to open?: \n")
f = open(coord_filename, 'rb')
coords_and_values = cPickle.load(f)
f.close()

data_cflux_5day_name = "data_cflux_5day" #"data_CFLX_5day_ave"
data_name = data_cflux_5day_name
with open('data/cflx_2000_2009_640x64x128.pkl') as f:
    data = cPickle.load(f)
    f.closed
year_stack = np.split(data, 10)
year_stack = ma.array(year_stack)
print "Year stack has shape: ", np.shape(year_stack)

seasonal_cycle =  np.mean(year_stack, 0)
seasonal_cycle_mean = np.mean(seasonal_cycle)
seasonal_cycle_stdev = np.std(seasonal_cycle)
samples = []
for item in coords_and_values:
    samples.append(seasonal_cycle[item[0], item[1], item[2]])

samples = np.array(samples)
samples_mean = np.mean(samples)
samples_stdev = np.std(samples)
#samples_range = np.abs(ma.max(samples) - ma.min(samples))
original_fitness = np.abs(seasonal_cycle_mean - samples_mean) + np.abs(seasonal_cycle_stdev - samples_stdev) 

if False:
    raw_input('press cntrl-c')

#~ x = 0
year_sample_dict_data = {}
#year_sample_list_data = {}
for x in np.arange(np.shape(year_stack)[0]):
    #year_value_list = []
    year_values_dict = {}
    x_nodes = []
    y_nodes = []
    z_nodes = []
    for item in coords_and_values:
        #print item #DEBUG
        x_nodes.append(item[0])
        y_nodes.append(item[1])
        z_nodes.append(item[2])
        year_values_dict[item] =  year_stack[x, item[0], item[1],item[2]]
        #year_value_list = np.append(year_value_list, year_stack[x,item[0],item[1],item[2]])
    #year_sample_list_data[x] = year_value_list
    year_sample_dict_data[x] = year_values_dict
    
if False:
    raw_input('press cntrl-c')  

annual_sample_mean = np.ones(year_stack.shape)
annual_sample_mean = ma.masked_values(annual_sample_mean, 1)
### We have a values list and coordinates
def test_rbf(x, annual_sample_mean=annual_sample_mean):
    coords_vals = year_sample_dict_data[x]
    x_nodes = []    
    y_nodes = []
    z_nodes = []
    values_list = []
    for item in coords_vals:
        x_nodes.append(item[0])
        y_nodes.append(item[1])
        z_nodes.append(item[2])
        values_list.append(coords_vals[item])
    xs = x_nodes
    ys = y_nodes
    zs = z_nodes
    values_list = np.array(values_list)
    time_len = 64
    all_data = year_stack[x, :time_len, :lat_end, :lon_end]
    ### New and improved and faster!!!
    annual_mean = np.mean(all_data)
    sample_mean = np.mean(values_list)
    annual_stdev = np.std(all_data)
    sample_stdev = np.std(values_list)
    annual_sample_mean[x, :time_len, :lat_end, :lon_end]
    for item in year_sample_dict_data[x].keys():
        #print item
        annual_sample_mean[x,item[0], item[1], item[2]] = year_sample_dict_data[x][item]
    plt.close('all')
    plt.subplot(2, 1, 1)
    plt.pcolormesh(ma.mean(all_data, 0), vmin=-5, vmax=15); plt.colorbar(); plt.axis('tight')
    plt.subplot(2, 1, 2)
    plt.pcolormesh(ma.mean(annual_sample_mean[x, :, :, :], 0), vmin=-5, vmax=15); plt.colorbar(); plt.axis('tight')
    plt.savefig(output_dir+coords+'_year_'+str(x)+'.png')
    plt.close('all')
    fitness = np.abs(annual_mean-sample_mean) + np.abs(annual_stdev - sample_stdev)
    return fitness, annual_mean, sample_mean, annual_stdev, sample_stdev #, annual_sample_mean

if False:
    raw_input('press cntrl-c')

list_of_fitness=[]
for x in np.arange(10):
    list_of_fitness.append(test_rbf(x))

if False:
    raw_input('press cntrl-c')

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
# number_of_gens = str(5)
filename = os.getcwd() + tex_dir+'seasonal-cycle-' + coords[:-4] + \
data_cflux_5day_name +'.tex' # + number_of_gens + 'gens.tex'
#~ filename = raw_input("Enter filename to write table to: ")
fobj = open(filename, 'w')

prop_or_curr = "Proposed" # Change this depending on which sampling strategy is used...
text_start = " \
\\begin{center} \n \
\\begin{table}[h] \n \
\\centering \n \
\caption{Comparison of the total Simulated Uptake With the Uptake from the \n \
Sampling strategy using " +str(np.size(y_nodes))+ " locations with a \n \
fitness "+str(np.round(original_fitness, 2))+" and the Sampling Error Introduced for " + data_name + ".} \n \
\\begin{tabular}[tbp]{@{}lp{2.5cm}p{2.5cm}p{2.5cm}p{2.5cm}p{2.5cm}@{}} \n \
\\toprule \n \
\scriptsize{Year} & \scriptsize{Model Mean} \n \
& \scriptsize{Sample Mean} \n \
& \scriptsize{Model Standard Deviation} \n \
& \scriptsize{Sample Standard Deviation} \n \
& \scriptsize{Fitness} \\\ \n \
\hline \n \
"

fobj.write(text_start)

for year in range(10):
    fobj.write("\scriptsize{" +str(years[year] +2000)+ "} & \scriptsize{"+str(round(list_of_fitness[year][1], 2))+"} & \
    \scriptsize{"+str(round(list_of_fitness[year][2], 2))+"} & \scriptsize{"+str(round(list_of_fitness[year][3], 2))+"} & \
    \scriptsize{"+str(round(list_of_fitness[year][4], 2))+"} & \scriptsize{"+str(round(list_of_fitness[year][0], 2))+"} \\\\")
    fobj.write("\n")

text_end ="\hline \n \
\scriptsize{" +str(years[0] + 2000)+ "-" +str(years[9] + 2000)+ "}    &   \
\scriptsize{"+str(round(np.mean(mean_data), 2))+" $\pm$ "+str(round(np.std(mean_data), 2))+"} &  \
\scriptsize{"+str(round(np.mean(mean_interp_data), 2))+" $\pm$ "+str(round(np.std(mean_interp_data), 2))+"} &  \
\scriptsize{"+str(round(np.mean(stdev_data), 2))+" $\pm$ "+str(round(np.std(stdev_data), 2))+"} &  \
\scriptsize{"+str(round(np.mean(stdev_interp_data), 2))+" $\pm$ "+str(round(np.std(stdev_interp_data), 2))+"} & \
\scriptsize{"+str(round(np.mean(fitness), 2))+" $\pm$ "+str(round(np.std(fitness), 2))+"} \\\ \n \
\\bottomrule \n \
\end{tabular} \n \
\end{table} \n \
\end{center} \n \
"
'''
text_end ="\hline \n \
\scriptsize{" +str(years[0] + 2000)+ "-" +str(years[9] + 2000)+ "}    \
&   \scriptsize{"+str(np.mean(mean_data ))+"} &  \
\scriptsize{"+str(np.mean(mean_interp_data))+"} & \
\scriptsize{"+str(np.mean(stdev_data))+"} &  \
\scriptsize{"+str(np.mean(stdev_interp_data))+"} \\\ \n \
\\bottomrule \n \
\end{tabular} \n \
\end{table} \n \
\end{center} \n \
"
'''

fobj.write(text_end)
fobj.close()

print "Table printed to: ", filename
### OLD STUFF???


'''
\scriptsize{" +str(years[0])+ "}    &   \scriptsize{"+str(tot_sam_upt[0])"} &  \scriptsize{"str(sam_est_upt[0])"} &  \scriptsize{"str(sam_unc[0]"} \\ \n \"
\scriptsize{" +str(years[1])+ "}    &   \scriptsize{"+str(tot_sam_upt[1])"} &  \scriptsize{"str(sam_est_upt[1])"} &  \scriptsize{"str(sam_unc[1]"} \\ \n \
\scriptsize{" +str(years[2])+ "}    &   \scriptsize{"+str(tot_sam_upt[2])"} &  \scriptsize{"str(sam_est_upt[2])"} &  \scriptsize{"str(sam_unc[2]"} \\ \n \
\scriptsize{" +str(years[3])+ "}    &   \scriptsize{"+str(tot_sam_upt[3])"} &  \scriptsize{"str(sam_est_upt[3])"} &  \scriptsize{"str(sam_unc[3]"} \\ \n \
\scriptsize{" +str(years[4])+ "}    &   \scriptsize{"+str(tot_sam_upt[4])"} &  \scriptsize{"str(sam_est_upt[4])"} &  \scriptsize{"str(sam_unc[4]"} \\ \n \
\scriptsize{" +str(years[5])+ "}    &   \scriptsize{"+str(tot_sam_upt[5])"} &  \scriptsize{"str(sam_est_upt[5])"} &  \scriptsize{"str(sam_unc[5]"} \\ \n \
\scriptsize{" +str(years[6])+ "}    &   \scriptsize{"+str(tot_sam_upt[6])"} &  \scriptsize{"str(sam_est_upt[6])"} &  \scriptsize{"str(sam_unc[6]"} \\ \n \
\scriptsize{" +str(years[7])+ "}    &   \scriptsize{"+str(tot_sam_upt[7])"} &  \scriptsize{"str(sam_est_upt[7])"} &  \scriptsize{"str(sam_unc[7]"} \\ \n \
\scriptsize{" +str(years[8])+ "}    &   \scriptsize{"+str(tot_sam_upt[8])"} &  \scriptsize{"str(sam_est_upt[8])"} &  \scriptsize{"str(sam_unc[8]"} \\ \n \
\scriptsize{" +str(years[9])+ "}    &   \scriptsize{"+str(tot_sam_upt[9])"} &  \scriptsize{"str(sam_est_upt[9])"} &  \scriptsize{"str(sam_unc[9]"} \\ \n \
'''
'''
This script takes the solution from from the genetic
algorithm that samples the decadal mean and tests
it on the annual means.

It returns a fitness values for each year, as well as 
the mean value  and the standard
deviation from the sample as well as the model data.

Values get put into a csv or a tex table?


solution

coordinates

Need to get a list of values for those coordinates
for each year.

Have a list of coordinates
get a list of values

Do This:

for item in coords_vals:
    x_nodes.append(item[0])
    y_nodes.append(item[1])
    z_nodes.append(item[2])
    values_list.append(coords_vals[item])
    year_data = np.append(year_data, year(coords_vals[item]))
    
for item in coords_vals:
    values_list.append(coords_vals[item])
    year_data = np.append(year_data, year(coords_vals[item]))
    
Then have these 4 lists

x_nodes # time
y_nodes # lat
z_nodes #lon
values_list

Need meshgrid
lati, loni = np.meshgrid(ti_lat, ti_lon) #2D
OR
xxx, yyy, zzz = np.lib.index_tricks.mgrid[0:10, 0:40, 0:180] #3D

Use Rbf

rbf = Rbf(x_nodes, y_nodes, z_nodes, values_list, function='gaussian', epsilon=4)

interpolated_data = rbf(xxx, yyy, zzz)

fitness = np.sqrt(np.sum((GI - ZI)**2)) where GI is original data for the year and ZI is interpolated data

So for each year:


year    | model mean | model stdev | sample mean | sample stdev | fitness |
1998
1999
2000
    |
2007

'''
