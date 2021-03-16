# -*- coding: utf-8 -*-
from netCDF4 import Dataset
import numpy as np
from datetime import datetime, timedelta


#============================================================================
# Read the nc data 
#============================================================================
# INPUT: area_of_interest = {"lat_min_area":46,"lat_max_area":55,"lon_min_area":5,"lon_max_area":15}
# time = hours since 1900-01-01 00:00:00.0



def load_wind(path_to_file:str, area_of_interest:dict,date):
    
    nc_file = Dataset(path_to_file, mode='r')
    
    u10_scale_factor = 0.0009829425845
    v10_scale_factor = 0.0010392589789
    
    lat = np.array(nc_file.variables['latitude'])
    lon = np.array(nc_file.variables['longitude'])
    time = np.array(nc_file.variables['time'])
    u10 = np.array(nc_file.variables['u10'])
    v10 = np.array(nc_file.variables['v10'])
    
    # Get the possed ours from given date
    time1 = datetime(1900,1,1,0,0,0)
    diff = date - time1
    hours = int(divmod(diff.total_seconds(),3600)[0])

    index = int(np.where(time == hours)[0])
    
    u10 = u10[index,:,:] # time lat lon
    v10 = v10[index,:,:]
    
    # Get area of interest
    lat_indexes = np.where((lat>area_of_interest["lat_min_area"]) & (lat<area_of_interest["lat_max_area"]))[0]
    lat = lat[lat_indexes]
    lon_indexes = np.where((lon>area_of_interest["lon_min_area"]) & (lon<area_of_interest["lon_max_area"]))[0]
    lon = lon[lon_indexes]
    u10 = u10[lat_indexes,:]
    u10 = u10[:,lon_indexes]*u10_scale_factor
    v10 = v10[lat_indexes,:]
    v10 = v10[:,lon_indexes]*v10_scale_factor
    
    # close nc file
    nc_file.close()
    
    return lat,lon,time,u10,v10

