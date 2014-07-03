import os
import cPickle
import numpy as np
from numpy import ma
from scipy.io.netcdf import netcdf_file
import scipy.ndimage as ndimage
from matplotlib import pyplot as plt

cflux_5day = ''
cflux_daily = ''
dpco2_daily = ''
pco2_daily = ''


cflux_5day = '/data/netcdf_files/CFLX_2000_2009.nc'
cflux_dpco2_daily = '/data/netcdf_files/cflx_dpco2_1998_2007.nc'
### default values (These can be altered in make_gene_map.py)
file_name = os.getcwd() + '/../' + cflux_5day # cflux_dpco2_daily
time_start = 0
time_end = 730 #730 for 5day #3650 for daily
lat_start = 0
lat_end = 40 # for southern Ocean
lon_start = 0
lon_end = 180
masked_value = 1e+20

unit_changer = 60*60*24 * 1000 # micromol carbon per m per day (86400000)


def load_file(file_name = file_name, time_start = time_start, 
              time_end = time_end, lat_start = lat_start, lat_end = lat_end,
                  lon_start = lon_start, lon_end = lon_end, masked_value = masked_value):
    nc = netcdf_file(file_name, 'r')
    new_array = nc.variables['Cflx'][time_start:time_end, lat_start:lat_end, lon_start:lon_end]
    nc.close()
    new_array = ma.masked_values(new_array, masked_value)
    new_array = ma.array(new_array, dtype=np.float32)
    new_array = new_array * unit_changer
    return new_array    

array = load_file()

interp_factor_t = (640./730)
interp_factor_lat = 40./64
interp_factor_lon = 180./128
nt,nlat,nlon = 730, 40, 180

new_indicies = np.mgrid[0:730:(640./730)*730*1j, 0:40:(40./64), 0:180:(180./128)]
# new_indicies = np.mgrid[0:nt:interp_factor_t*nt*1j, 0:nlat:interp_factor_lat*nlon*1j, 0:nlon:interp_factor_lon*nlat*1j]
interp_array = ndimage.map_coordinates(array, new_indicies, 
                                       order=1, output=array.dtype)
# interp_array = interp_array.reshape((interp_factor * nt, nlat, nlon))
interp_array_m = ma.masked_values(interp_array, 0)
def load_file_64(interp_array=interp_array):
    return interp_array

if __name__ == "__main__":
    with open('data/cflx_2000_2009_640x64x128.pkl', 'w') as f:
        data = load_file_64()
        cPickle.dump(data, f)
        f.closed

def splot():
    plt.close('all')
    vmin,vmax=0, 14
    plt.subplot(2, 1, 1)
    plt.pcolormesh(ma.mean(array, 0), vmin=vmin, vmax=vmax); plt.colorbar(); plt.axis('tight')
    plt.subplot(2, 1, 2)
    plt.pcolormesh(ma.mean(interp_array_m, 0), vmin=vmin, vmax=vmax); plt.colorbar(); plt.axis('tight')
    # plt.show()
    plt.savefig('binary_remap.png')
    plt.close('all')
